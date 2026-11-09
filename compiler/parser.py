from ast_nodes import (Projection, Selection, Condition, Relation, 
                       Rename, Product, JoinCondition, ThetaJoin, 
                       Union, Intersection, Difference, NaturalJoin)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position >= len(self.tokens):
            raise ValueError("Unexpected end of input. Check for missing parentheses or operands.")
        
        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def parse(self):
        if not self.tokens:
            raise ValueError("Input cannot be empty.")

        tree = self.parse_expression()

        if self.position < len(self.tokens):
            token_type, token_value = self.current_token()
            raise ValueError(f"Unexpected extra token: {token_value}")

        return tree

    def parse_expression(self):
        left = self.parse_primary()

        while self.position < len(self.tokens):
            if self.current_token()[0] == "CROSS_PRODUCT":
                self.advance()
                right = self.parse_primary()
                left = Product(left, right)

            elif self.current_token()[0] == "THETA_JOIN":
                self.advance()

                if self.current_token()[0] != "IDENTIFIER":
                    raise ValueError("Expected left attribute in join attribute after ⋈")

                first_identifier = self.current_token()[1]
                self.advance()

                if(
                    self.position < len(self.tokens) and self.current_token()[0] in [
                        "GREATER_THAN", "LESS_THAN", "EQUAL"
                    ]
                ):
                    operator_type, operator = self.current_token()
                    self.advance()

                    if self.current_token()[0] != "IDENTIFIER":
                        raise ValueError("Expected right attribute in join condition")

                    right_column = self.current_token()[1]
                    self.advance()

                    right = self.parse_primary()

                    condition = JoinCondition(first_identifier, operator, right_column)

                    left = ThetaJoin(left, condition, right)
                
                else:
                    right = Relation(first_identifier)
                    left = NaturalJoin(left, right)

            elif self.current_token()[0] == "UNION":
                self.advance()
                right = self.parse_primary()
                left = Union(left, right)

            elif self.current_token()[0] == "INTERSECTION":
                self.advance()
                right = self.parse_primary()
                left = Intersection(left, right)

            elif self.current_token()[0] == "DIFFERENCE":
                self.advance()
                right = self.parse_primary()
                left = Difference(left, right)

            else:
                break

        return left

    def parse_primary(self):
        token_type, token_value = self.current_token()

        if token_type == "PROJECTION":
            return self.parse_projection()
        elif token_type == "SELECTION":
            return self.parse_selection()
        elif token_type == "IDENTIFIER":
            return self.parse_relation()
        elif token_type == "RENAME":
            return self.parse_rename()
        else:
            raise ValueError(f"Unexpected token: {token_value}")

    def parse_projection(self):
        self.advance()
        columns = []

        while self.current_token()[0] == "IDENTIFIER":
            columns.append(self.current_token()[1])
            self.advance()

            if self.current_token()[0] == "COMMA":
                self.advance()
            else:
                break

        if self.current_token()[0] != "LPAREN":
            raise ValueError("Expected '(' after projection columns")

        self.advance()

        child = self.parse_expression()

        if self.current_token()[0] != "RPAREN":
            raise ValueError("Expected ')' after projection")

        self.advance()

        return Projection(columns, child)

    def parse_selection(self):
        self.advance()

        if self.current_token()[0] != "IDENTIFIER":
            raise ValueError("Expected column in selection condition")

        column = self.current_token()[1]
        self.advance()

        operator_type, operator = self.current_token()

        if operator_type not in ["GREATER_THAN", "LESS_THAN", "EQUAL"]:
            raise ValueError("Expected comparison operator")

        self.advance()

        if self.current_token()[0] != "NUMBER":
            raise ValueError("Exepected number after comparison operator")

        value = self.current_token()[1]
        self.advance()

        condition = Condition(column, operator, value)

        if self.current_token()[0] != "LPAREN":
            raise ValueError("Expected '(' after selection condition")

        self.advance()

        child = self.parse_expression()

        if self.current_token()[0] != "RPAREN":
            raise ValueError("Expected ')' after selection")

        self.advance()

        return Selection(condition, child)

    def parse_relation(self):
        token_type, token_value = self.current_token()

        if token_type != "IDENTIFIER":
            raise ValueError("Expected relation name")

        self.advance()

        return Relation(token_value)

    def parse_rename(self):
        self.advance()

        if self.current_token()[0] != "IDENTIFIER":
            raise ValueError("Expected alias after rename operator")

        alias = self.current_token()[1]
        self.advance()

        if self.current_token()[0] != "LPAREN":
            raise ValueError("Expected '(' after rename alias")

        self.advance()

        child = self.parse_expression()

        if self.current_token()[0] != "RPAREN":
            raise ValueError("Expected ')' after rename expression")

        self.advance()

        return Rename(alias, child)

# if __name__ == "__main__":
#     from lexer import tokenize

#     query = input("Enter RA query: ")

#     try: 
#         tokens = tokenize(query)
#         parser = Parser(tokens)
#         tree = parser.parse()

#         print("\nGenerated AST:")
#         print(tree)

#     except ValueError as error:
#         print("\nParser Error:", error)