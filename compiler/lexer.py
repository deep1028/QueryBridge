def tokenize(query):
    tokens = []
    i = 0
    while i < len(query):
        char = query[i]
        if char.isspace():
            i += 1
            continue

        if char == "π":
            tokens.append(("PROJECTION", char))
            i += 1
            continue

        if char == "σ":
            tokens.append(("SELECTION", char))
            i += 1
            continue

        if char == "ρ":
            tokens.append(("RENAME", char))
            i += 1
            continue

        if char == "×":
            tokens.append(("CROSS_PRODUCT", char))
            i += 1
            continue

        if char == "∪":
            tokens.append(("UNION", char))
            i += 1
            continue

        if char == "∩":
            tokens.append(("INTERSECTION", char))
            i += 1
            continue

        if char == "−":
            tokens.append(("DIFFERENCE", char))
            i += 1
            continue

        if char == "⋈":
            tokens.append(("THETA_JOIN", char))
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

        if char.isalpha() or char == "_":
            identifier = ""

            while i < len(query) and (
                query[i].isalnum() or query[i] in "_."
            ):
                identifier += query[i]
                i += 1

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