class Projection:
    def __init__(self, columns, child):
        self.columns = columns
        self.child = child

    def __repr__(self):
        return f"Projection(columns = {self.columns}, child = {self.child})"

class Selection:
    def __init__(self, condition, child):
        self.condition = condition
        self.child = child

    def __repr__(self):
        return f"Selection(condition = {self.condition}, child = {self.child})"

class Condition:
    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value

    def __repr__(self):
        return f"Condition({self.column} {self.operator} {self.value})"

class Relation:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Relation({self.name})"

class Rename:
    def __init__(self, alias, child):
        self.alias = alias
        self.child = child

    def __repr__(self):
        return f"Rename(alias = {self.alias}, child = {self.child})"

class Product:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Product(left = {self.left}, right = {self.right})"

class JoinCondition:
    def __init__(self, left_column, operator, right_column):
        self.left_column = left_column
        self.operator = operator
        self.right_column = right_column

    def __repr__(self):
        return (
            f"JoinCondition("
            f"{self.left_column} {self.operator} {self.right_column})"
        )

class ThetaJoin:
    def __init__(self, left, condition, right):
        self.left = left
        self.condition = condition
        self.right = right

    def __repr__(self):
        return (
            f"ThetaJoin("
            f"left = {self.left}, "
            f"condition = {self.condition}, "
            f"right = {self.right})"
        )

class Union:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Union(left = {self.left}, right = {self.right})"

class Intersection:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Intersection(left = {self.left}, right = {self.right})"

class Difference:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Difference(left = {self.left}, right = {self.right})"

class NaturalJoin:
    def __inti__(self, left, right):
        self.left = left
        self.right = right
     
    def __repr__(self):
        return f"NaturalJoin(left = {self.left}, right = {self.right})"