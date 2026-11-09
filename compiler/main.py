from lexer import tokenize
from parser import Parser
from sql_generator import generate_sql

def main():
    query = input("Enter Relational Algebra query: ")

    try:
        tokens = tokenize(query)
        parser = Parser(tokens)
        tree = parser.parse()
        sql = generate_sql(tree)

        print("\nGenerated SQL: ")
        print(sql + ";")
    except ValueError as error:
        print(f"\nCompiler Error: {error}")

if __name__ == "__main__":
    main()