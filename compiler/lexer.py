def tokenize(query):
    tokens = []
    i = 0

    while i < len(query):
        char = query[i]

        if char.isspace():
            i += 1
            continue

        operators = {
            "π": "PROJECTION",
            "σ": "SELECTION",
            "ρ": "RENAME",
            "×": "CROSS_PRODUCT",
            "∪": "UNION",
            "∩": "INTERSECTION",
            "−": "DIFFERENCE",
            "⋈": "THETA_JOIN"
        }

        if char in operators:
            tokens.append((operators[char], char))
            i += 1
            continue

        if char == "(":
            tokens.append(("LPAREN", char))
            i += 1
            continue

        if char == ")":
            tokens.append(("RPAREN", char))
            i += 1
            continue

        if char == ",":
            tokens.append(("COMMA", char))
            i += 1
            continue

        if i + 1 < len(query):
            pair = query[i:i + 2]

            if pair in [">=", "<=", "!="]:
                token_type = {
                    ">=": "GREATER_EQUAL",
                    "<=": "LESS_EQUAL",
                    "!=": "NOT_EQUAL"
                }[pair]

                tokens.append((token_type, pair))
                i += 2
                continue

        if char == ">":
            tokens.append(("GREATER_THAN", char))
            i += 1
            continue

        if char == "<":
            tokens.append(("LESS_THAN", char))
            i += 1
            continue

        if char == "=":
            tokens.append(("EQUAL", char))
            i += 1
            continue

        if char in ["'", '"']:
            quote = char
            i += 1
            string_value = ""

            while i < len(query):
                if query[i] == quote:
                    if i + 1 < len(query) and query[i + 1] == quote:
                        string_value += quote
                        i += 2
                        continue
                    break

                string_value += query[i]
                i += 1

            if i >= len(query):
                raise ValueError("Unterminated string literal")

            i += 1
            tokens.append(("STRING", string_value))
            continue

        if char.isalpha() or char == "_":
            identifier = ""

            while i < len(query) and (
                query[i].isalnum() or query[i] in "_."
            ):
                identifier += query[i]
                i += 1

            keyword = identifier.upper()

            if keyword == "AND":
                tokens.append(("AND", identifier))
            elif keyword == "OR":
                tokens.append(("OR", identifier))
            elif keyword == "NOT":
                tokens.append(("NOT", identifier))
            else:
                tokens.append(("IDENTIFIER", identifier))

            continue

        if char.isdigit():
            number = ""

            while i < len(query) and query[i].isdigit():
                number += query[i]
                i += 1

            tokens.append(("NUMBER", number))
            continue

        raise ValueError(f"Unknown character: {char}")

    return tokens

# if __name__ == "__main__":
#     query = input("Enter RA query: ")
#     tokens = tokenize(query)

#     print("\nGenerated Tokens:")
#     for token in tokens:
#         print(token)