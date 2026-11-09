# QueryBridge

**A Relational Algebra to SQL Compiler built using Python.**

QueryBridge is a DBMS project that translates Relational Algebra expressions into equivalent SQL queries. It demonstrates the fundamental stages of compiler design, including lexical analysis, parsing, Abstract Syntax Tree (AST) construction, and SQL generation.

## Features

### Currently Implemented

| Component | Description |
|---|---|
| Lexer | Converts Relational Algebra expressions into tokens |
| Parser | Parses tokens using recursive descent parsing |
| AST | Represents expressions using structured nodes |
| SQL Generator | Converts AST nodes into SQL queries |

### Supported Relational Algebra Operators

| Operator | Symbol | Description |
|---|---|---|
| Projection | π | Selects specific attributes |
| Selection | σ | Filters tuples based on conditions |
| Rename | ρ | Renames a relation using an alias |
| Cartesian Product | × | Combines tuples from two relations |
| Theta Join | ⋈ | Joins relations using a comparison condition |
| Union | ∪ | Combines tuples from compatible relations |
| Intersection | ∩ | Returns tuples common to both relations |
| Difference | − | Returns tuples present in the first relation but not the second |

## Technology Stack

- **Programming Language:** Python
- **Compiler Design:** Lexical Analysis, Recursive Descent Parsing, AST
- **Database Query Language:** SQL
- **Version Control:** Git and GitHub

## Project Structure

```text
QueryBridge/
│
├── compiler/
│   ├── lexer.py
│   ├── ast_nodes.py
│   ├── parser.py
│   ├── sql_generator.py
│   └── main.py
│
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/QueryBridge.git
```

### 2. Navigate into the project

```bash
cd QueryBridge
```

### 3. Run the compiler

```bash
python compiler/main.py
```

### 4. Enter a Relational Algebra expression

Example:

```text
π Name (σ Salary > 25000 (Faculty))
```

Expected SQL:

```sql
SELECT Name FROM Faculty WHERE Salary > 25000;
```

## More Examples

**Projection**

```text
π Name, Salary (Faculty)
```

**Selection**

```text
σ Salary > 25000 (Faculty)
```

**Cartesian Product**

```text
Faculty × Department
```

**Theta Join**

```text
Faculty ⋈ Faculty.Dept_ID = Department.Dept_ID Department
```

**Union**

```text
Faculty ∪ FormerFaculty
```

**Intersection**

```text
Faculty ∩ FormerFaculty
```

**Difference**

```text
Faculty − FormerFaculty
```

## Current Limitations

- Selection conditions currently support a limited comparison format.
- Rename currently supports direct relation renaming.
- Qualified attributes are supported in the lexer for join conditions, but broader attribute handling is still under development.
- Database schema validation is not yet implemented.
- SQL execution and database integration are planned.
- A graphical user interface is planned.
- SQL to Relational Algebra conversion is planned.

## Future Plans

- Improve grammar and operator precedence.
- Add Natural Join.
- Support more complex selection conditions.
- Add semantic and schema validation.
- Integrate a database engine.
- Build an interactive web interface using Flask, HTML, CSS, and JavaScript.
- Implement SQL to Relational Algebra conversion.

## Project Goal

The goal of QueryBridge is to demonstrate how a compiler translates high-level Relational Algebra expressions into executable SQL queries while providing an understandable representation of the compilation process.

## Author

Developed as an academic DBMS project.

---

**Project Status:** Under Development