from ast_nodes import Condition, LogicalCondition, NotCondition

class SQLQuery:
    def __init__(self, columns, source, conditions = None):
        self.columns = columns
        self.source = source
        self.conditions = conditions if conditions is not None else []

    def to_sql(self):
        sql = f"SELECT {', '.join(self.columns)} FROM {self.source}"

        if self.conditions:
            sql += " WHERE " + " AND ".join(self.conditions)

        return sql

def generate_condition_sql(condition):
    if isinstance(condition, Condition):
        if  condition.value_type == "STRING":
            value = "'" + condition.value.replace("'", "''") + "'"
        else:
            value = condition.value

        return (
            f"{condition.column} "
            f"{condition.operator} "
            f"{value}"
        )

    if isinstance(condition, LogicalCondition):
        left = generate_condition_sql(condition.left)
        right = generate_condition_sql(condition.right)

        return f"({left} {condition.operator} {right})"

    if isinstance(condition, NotCondition):
        inner = generate_condition_sql(condition.condition)

        return f"(NOT {inner})"

    raise ValueError("Unsupported condition type")

def build_query(node):
    if node.__class__.__name__ == "Relation":
        return SQLQuery(
            ["*"],
            node.name
        )

    if node.__class__.__name__ == "Product":
        left_query = build_query(node.left)
        right_query = build_query(node.right)

        source = (
            f"({left_query.to_sql()}) AS QB_LEFT "
            f"CROSS JOIN "
            f"({right_query.to_sql()}) AS QB_RIGHT"
        )

        return SQLQuery(["*"], source)

    if node.__class__.__name__ == "Rename":
        if node.child.__class__.__name__ != "Relation":
            raise ValueError("Rename currently supports direct relation renaming only")

        return SQLQuery(
            ["*"],
            f"{node.child.name} AS {node.alias}"
        )

    if node.__class__.__name__ == "Selection":
        query = build_query(node.child)
        sql_condition = generate_condition_sql(node.condition)
        query.conditions.append(sql_condition)

        return query

    if node.__class__.__name__ == "ThetaJoin":
        left_query = build_query(node.left)
        right_query = build_query(node.right)

        condition = node.condition

        source = (
            f"{left_query.source} "
            f"INNER JOIN "
            f"{right_query.source} "
            f"ON {condition.left_column} "
            f"{condition.operator} "
            f"{condition.right_column}"
        )

        return SQLQuery(["*"], source)

    if node.__class__.__name__ == "Union":
        left_query = build_query(node.left)
        right_query = build_query(node.right)

        union_source = (
            f"({left_query.to_sql()} "
            f"UNION "
            f"{right_query.to_sql()}) AS QB_UNION"
        )

        return SQLQuery(["*"], union_source)

    if node.__class__.__name__ == "Intersection":
        left_query = build_query(node.left)
        right_query = build_query(node.right)

        intersection_source = (
            f"({left_query.to_sql()} "
            f"INTERSECT "
            f"{right_query.to_sql()}) AS QB_INTERSECTION"
        )

        return SQLQuery(["*"], intersection_source)

    if node.__class__.__name__ == "Difference":
        left_query = build_query(node.left)
        right_query = build_query(node.right)
        
        difference_source = (
            f"({left_query.to_sql()} "
            f"EXCEPT "
            f"{right_query.to_sql()}) AS QB_DIFFERENCE"
        )

        return SQLQuery(["*"], difference_source)
        
    if node.__class__.__name__ == "Projection":
        query = build_query(node.child)
        query.columns = node.columns

        return query

    if node.__class__.__name__ == "NaturalJoin":
        left_query = build_query(node.left)
        right_query = build_query(node.right)

        source = (
            f"{left_query.source} "
            f"NATURAL JOIN "
            f"{right_query.source}"
        )

        return SQLQuery(["*"], source)


    raise ValueError("Unsupported AST node")

    

def generate_sql(node):
    query = build_query(node)
    return query.to_sql()