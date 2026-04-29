# Sprout

A small, bytecode-compiled programming language implemented in Python.

```
  ____                       _
 / ___| _ __  _ __ ___  _   _| |_
 \___ \| '_ \| '__/ _ \| | | | __|
  ___) | |_) | | | (_) | |_| | |_
 |____/| .__/|_|  \___/ \__,_|\__|
       |_|
```

## Features

- **Types**: integers, floats, strings, booleans, nil, arrays, dicts, functions
- **Variables**: `let` declarations with optional initializer
- **Functions**: first-class, closures, default parameters, anonymous functions
- **Control flow**: `if`/`else if`/`else`, `while`, `for … in`, `break`, `continue`
- **Operators**: arithmetic, comparison, logical (short-circuit), bitwise-free
- **Stdlib**: `print`, `println`, math, string, array, dict, type utilities
- **Modules**: `import math`, `import string`
- **REPL**: interactive shell with history, `.dis`, `.reset`

## Pipeline

```
source text
    │
    ▼ Lexer            (sprout/lexer.py)
token stream
    │
    ▼ Parser           (sprout/parser.py)  — recursive descent
AST (abstract syntax tree)
    │
    ▼ SemanticAnalyzer (sprout/semantic.py) — scope / arity checks
validated AST
    │
    ▼ Compiler         (sprout/compiler.py)
CodeObject (bytecode)
    │
    ▼ VM               (sprout/vm.py)  — stack-based
result
```

## Installation

```bash
cd sprout
pip install -e .
```

## Usage

```bash
# Run a file
sprout program.sp

# Evaluate a string
sprout -c 'println("Hello!")'

# Interactive REPL
sprout

# Show disassembled bytecode
sprout --dis program.sp
```

Or without installation:

```bash
python3 -m sprout program.sp
python3 -m sprout          # REPL
```

---

# Language Specification

## 1. Lexical Structure

### Comments

```sprout
# This is a line comment
// Also a line comment
/* This is a
   block comment */
```

### Identifiers

Start with a letter or `_`, followed by letters, digits, or `_`.

```sprout
my_var   _private   count2
```

### Keywords

```
let  fn  return  if  else  while  for  in  break  continue
and  or  not  true  false  nil  import
```

### Literals

| Kind     | Examples                          |
|----------|-----------------------------------|
| Integer  | `0`, `42`, `1000`                 |
| Float    | `3.14`, `2.5e-3`, `1e10`          |
| String   | `"hello"`, `'world'`, `"a\nb"`    |
| Bool     | `true`, `false`                   |
| Nil      | `nil`                             |

Escape sequences in strings: `\n`, `\t`, `\r`, `\\`, `\'`, `\"`, `\0`.

---

## 2. Types

| Type       | Description                              | Example                   |
|------------|------------------------------------------|---------------------------|
| `int`      | 64-bit integer                           | `42`, `-7`                |
| `float`    | 64-bit IEEE 754 double                   | `3.14`, `1.0e-5`          |
| `string`   | UTF-8 immutable sequence of characters   | `"hello"`                 |
| `bool`     | Boolean                                  | `true`, `false`           |
| `nil`      | Absence of value                         | `nil`                     |
| `array`    | Mutable ordered sequence                 | `[1, 2, 3]`               |
| `dict`     | Mutable key-value map                    | `{"a": 1, "b": 2}`        |
| `function` | First-class callable                     | `fn(x) { return x * 2 }` |

### Truthiness

`nil`, `false`, `0`, `0.0`, `""`, `[]`, `{}` are falsy. Everything else is truthy.

---

## 3. Variables

```sprout
let x = 42          # declare and initialise
let y               # declare with nil
x = 100             # reassign
x += 5              # compound assignment: +=  -=  *=  /=
```

Variables must be declared with `let` before use. Assignment to an undeclared name is a semantic error.

---

## 4. Operators

### Arithmetic

| Op  | Description             | Types                |
|-----|-------------------------|----------------------|
| `+` | addition / concat       | int, float, string, array |
| `-` | subtraction             | int, float           |
| `*` | multiplication / repeat | int, float, string×int |
| `/` | division (floor for int)| int, float           |
| `%` | modulo                  | int                  |
| `**`| exponentiation (right-assoc) | int, float      |
| `-x`| unary negation          | int, float           |

Integer division uses floor division (`7 / 2 == 3`). Use `float()` for true division.

### Comparison

`==`, `!=`, `<`, `<=`, `>`, `>=` — all return `bool`.

### Logical

| Op    | Description                | Short-circuit |
|-------|----------------------------|---------------|
| `and` | logical and                | yes           |
| `or`  | logical or                 | yes           |
| `not` | logical not (unary prefix) | —             |

### Operator Precedence (highest to lowest)

| Level | Operators                  |
|-------|----------------------------|
| 1     | `()` `[]` `.` (postfix)    |
| 2     | `-x` (unary)               |
| 3     | `**`                       |
| 4     | `*`  `/`  `%`              |
| 5     | `+`  `-`                   |
| 6     | `==`  `!=`  `<`  `<=`  `>`  `>=` |
| 7     | `not`                      |
| 8     | `and`                      |
| 9     | `or`                       |
| 10    | `=`  `+=`  `-=`  `*=`  `/=` (right-assoc) |

---

## 5. Statements

### Variable declaration

```sprout
let name = "Alice"
let counter          # initialised to nil
```

### Assignment

```sprout
x = value
arr[i] = value
dict["key"] = value
x += 5    # also -=  *=  /=
```

### If / else

```sprout
if condition {
    # ...
} else if other_condition {
    # ...
} else {
    # ...
}
```

### While loop

```sprout
while condition {
    # ...
}
```

### For loop

Iterates over arrays, strings, dicts (over keys), and ranges.

```sprout
for item in collection {
    # ...
}

for i in range(10) { }           # 0..9
for i in range(2, 7) { }         # 2..6
for i in range(0, 10, 2) { }     # 0, 2, 4, 6, 8
```

### Break and continue

`break` exits the nearest enclosing loop. `continue` skips to the next iteration.

### Return

```sprout
fn f(x) {
    if x < 0 { return nil }
    return x * 2
}
```

A function without an explicit `return` returns `nil`.

### Import

```sprout
import math
println(math["pi"])
println(math["sqrt"](16))
```

Available modules: `math`, `string`.

---

## 6. Functions

```sprout
fn add(a, b) {
    return a + b
}

# Default parameters
fn greet(name, greeting = "Hello") {
    return greeting + ", " + name + "!"
}

# Anonymous / first-class
let double = fn(x) { return x * 2 }

# Closures
fn make_counter() {
    let n = 0
    return fn() {
        n += 1
        return n
    }
}
let c = make_counter()
c()   # 1
c()   # 2
```

Functions are values and can be passed, returned, and stored.

---

## 7. Arrays

```sprout
let arr = [1, 2, 3]
arr[0]           # 1  (0-based)
arr[0] = 99      # mutation
len(arr)         # 3
append(arr, 4)   # in-place push
pop(arr)         # remove and return last element
arr + [4, 5]     # concatenation (new array)
"x" * 3          # "xxx"
```

---

## 8. Dicts

```sprout
let d = {"name": "Alice", "age": 30}
d["name"]           # "Alice"
d["email"] = "..."  # add key
has(d, "age")       # true
keys(d)             # ["name", "age", "email"]
values(d)           # ["Alice", 30, "..."]
```

---

## 9. Standard Library

### Output

| Function           | Description                                |
|--------------------|--------------------------------------------|
| `print(…)`         | Print without trailing newline             |
| `println(…)`       | Print with trailing newline                |

### Type

| Function    | Description                              |
|-------------|------------------------------------------|
| `type(v)`   | Return type name as string               |
| `str(v)`    | Convert value to string representation   |
| `int(v)`    | Convert to integer                       |
| `float(v)`  | Convert to float                         |
| `bool(v)`   | Convert to boolean (truthy test)         |

### Math

| Function         | Description                  |
|------------------|------------------------------|
| `sqrt(x)`        | Square root                  |
| `abs(x)`         | Absolute value               |
| `floor(x)`       | Floor                        |
| `ceil(x)`        | Ceiling                      |
| `round(x, n=0)`  | Round to `n` decimal places  |
| `min(a, b, …)`   | Minimum                      |
| `max(a, b, …)`   | Maximum                      |

### Strings

| Function                     | Description                          |
|------------------------------|--------------------------------------|
| `len(s)`                     | Length                               |
| `upper(s)`                   | Uppercase                            |
| `lower(s)`                   | Lowercase                            |
| `trim(s)`                    | Strip leading/trailing whitespace    |
| `split(s, sep)`              | Split into array                     |
| `join(arr, sep)`             | Join array into string               |
| `contains(s, sub)`           | Substring check                      |
| `starts_with(s, prefix)`     | Prefix check                         |
| `ends_with(s, suffix)`       | Suffix check                         |
| `replace(s, old, new)`       | Replace occurrences                  |
| `format(tmpl, …)`            | Python-style `{}` format             |

### Arrays

| Function          | Description                         |
|-------------------|-------------------------------------|
| `len(arr)`        | Number of elements                  |
| `append(arr, v)`  | Append in-place, returns arr        |
| `pop(arr)`        | Remove and return last element      |
| `pop(arr, i)`     | Remove and return element at index  |

### Dicts

| Function         | Description                   |
|------------------|-------------------------------|
| `keys(d)`        | Array of keys                 |
| `values(d)`      | Array of values               |
| `has(d, key)`    | Check key existence           |

### Iteration

| Function              | Description                                     |
|-----------------------|-------------------------------------------------|
| `range(n)`            | Integer range `[0, n)`                          |
| `range(start, stop)`  | Integer range `[start, stop)`                   |
| `range(start, stop, step)` | Integer range with step                  |

### Misc

| Function             | Description                               |
|----------------------|-------------------------------------------|
| `input(prompt="")`   | Read line from stdin                      |
| `assert(cond, msg?)` | Raise error if `cond` is falsy            |
| `exit(code=0)`       | Terminate the interpreter                 |

### Math module

```sprout
import math
math["pi"]          # 3.14159…
math["e"]           # 2.71828…
math["sin"](x)
math["cos"](x)
math["tan"](x)
math["log"](x)
math["log2"](x)
math["log10"](x)
math["floor"](x)
math["ceil"](x)
math["sqrt"](x)
math["pow"](x, y)
```

---

## 10. REPL

```
$ sprout
>>> let x = 10
>>> x * x
100
>>> fn fact(n) { if n <= 1 { return 1 } return n * fact(n - 1) }
>>> fact(5)
120
```

REPL commands:

| Command   | Action                          |
|-----------|---------------------------------|
| `.help`   | Show help                       |
| `.exit`   | Quit                            |
| `.dis`    | Disassemble last compiled input |
| `.clear`  | Clear multi-line buffer         |
| `.reset`  | Reset VM (clear all variables)  |
| `Ctrl-D`  | Quit                            |

Multi-line input is buffered automatically when braces are open.

---

## 11. Bytecode VM

Sprout compiles to a compact bytecode executed by a stack-based virtual machine.

### Instruction set (selected)

| Opcode           | Description                                     |
|------------------|-------------------------------------------------|
| `LOAD_CONST n`   | Push constant `constants[n]`                    |
| `LOAD_GLOBAL n`  | Push global variable `names[n]`                 |
| `STORE_GLOBAL n` | Pop and store to global `names[n]`              |
| `LOAD_VAR n`     | Push local variable `names[n]`                  |
| `STORE_VAR n`    | Pop and store to local `names[n]`               |
| `DEFINE_VAR n`   | Pop and define new local `names[n]`             |
| `ADD` / `SUB` / `MUL` / `DIV` / `MOD` / `POW` | Binary arithmetic |
| `NEG`            | Unary negation                                  |
| `EQ` / `NEQ` / `LT` / `LTE` / `GT` / `GTE` | Comparison → bool |
| `NOT`            | Logical not                                     |
| `JUMP n`         | Unconditional jump to offset `n`                |
| `JUMP_IF_FALSE n`| Pop TOS; jump if falsy                          |
| `JUMP_IF_FALSE_PEEK n` | Peek TOS; jump if falsy (for `and`)       |
| `JUMP_IF_TRUE_PEEK n`  | Peek TOS; jump if truthy (for `or`)       |
| `MAKE_FUNCTION n`| Build function from `nested[n]` + stack defaults |
| `CALL n`         | Call TOS with `n` args from stack               |
| `RETURN`         | Return TOS from current frame                   |
| `BUILD_ARRAY n`  | Build array from top `n` stack values           |
| `BUILD_DICT n`   | Build dict from top `2n` key/value pairs        |
| `GET_ITEM`       | `TOS1[TOS]`                                     |
| `SET_ITEM`       | `TOS2[TOS1] = TOS`                              |
| `GET_ITER`       | Wrap TOS in iterator                            |
| `FOR_ITER n`     | Advance iterator or jump to `n`                 |
| `POP`            | Pop and discard TOS                             |
| `DUP`            | Duplicate TOS                                   |
| `HALT`           | Stop execution                                  |

### Inspect bytecode

```bash
sprout --dis program.sp
```

Example output:

```
<CodeObject '<module>'>
  params:    []
  constants: [0, 10, 'i']
  names:     ['i', 'println']
  code:
    0000  LOAD_CONST                    0  ; 0
    0001  STORE_GLOBAL                  0  ; 'i'
    ...
```

---

## 12. Project Structure

```
sprout/
├── sprout/
│   ├── __init__.py        # Package version
│   ├── __main__.py        # CLI entry point
│   ├── tokens.py          # Token types and Token dataclass
│   ├── lexer.py           # Lexer / tokeniser
│   ├── ast_nodes.py       # AST node dataclasses
│   ├── parser.py          # Recursive descent parser
│   ├── semantic.py        # Semantic analyser (scope + checks)
│   ├── bytecode.py        # Opcode enum and CodeObject
│   ├── compiler.py        # AST → bytecode compiler
│   ├── vm.py              # Stack-based virtual machine
│   ├── interpreter.py     # High-level pipeline wrapper
│   └── repl.py            # Interactive REPL
├── examples/
│   ├── 01_hello_world.sp
│   ├── 02_variables.sp
│   ├── 03_arithmetic.sp
│   ├── 04_strings.sp
│   ├── 05_arrays.sp
│   ├── 06_dicts.sp
│   ├── 07_functions.sp
│   ├── 08_control_flow.sp
│   ├── 09_fibonacci.sp
│   ├── 10_sorting.sp
│   ├── 11_higher_order.sp
│   ├── 12_recursion.sp
│   ├── 13_closures.sp
│   ├── 14_primes.sp
│   ├── 15_linked_list.sp
│   ├── 16_stack_queue.sp
│   ├── 17_string_processing.sp
│   ├── 18_math_module.sp
│   ├── 19_fizzbuzz.sp
│   └── 20_game_of_life.sp
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic.py
│   ├── test_vm.py
│   └── test_integration.py
├── pyproject.toml
└── README.md
```

---

## 13. Running Tests

```bash
pip install pytest
python3 -m pytest tests/ -v
```

193 tests covering the lexer, parser, semantic analyser, VM, and all 20 example programs.

---

## 14. Grammar (EBNF)

```ebnf
program     = statement* EOF ;

statement   = var_decl
            | fn_def
            | if_stmt
            | while_stmt
            | for_stmt
            | return_stmt
            | break_stmt
            | continue_stmt
            | import_stmt
            | expr_stmt ;

var_decl    = "let" IDENT ( "=" expr )? ";"? ;
fn_def      = "fn" IDENT "(" params ")" block ;
params      = ( IDENT ( "=" expr )? ( "," IDENT ( "=" expr )? )* )? ;
block       = "{" statement* "}" ;
if_stmt     = "if" expr block ( "else" "if" expr block )* ( "else" block )? ;
while_stmt  = "while" expr block ;
for_stmt    = "for" IDENT "in" expr block ;
return_stmt = "return" expr? ";"? ;
break_stmt  = "break" ";"? ;
continue_stmt = "continue" ";"? ;
import_stmt = "import" IDENT ";"? ;
expr_stmt   = expr ";"? ;

expr        = assignment ;
assignment  = or ( ( "=" | "+=" | "-=" | "*=" | "/=" ) assignment )? ;
or          = and ( "or" and )* ;
and         = not ( "and" not )* ;
not         = "not" not | comparison ;
comparison  = additive ( ( "==" | "!=" | "<" | "<=" | ">" | ">=" ) additive )? ;
additive    = multiplicative ( ( "+" | "-" ) multiplicative )* ;
multiplicative = unary ( ( "*" | "/" | "%" ) unary )* ;
unary       = "-" unary | power ;
power       = postfix ( "**" unary )? ;     (* right-assoc *)
postfix     = primary ( call_args | subscript | attribute )* ;
call_args   = "(" ( expr ( "," expr )* )? ")" ;
subscript   = "[" expr "]" ;
attribute   = "." IDENT ;
primary     = INTEGER | FLOAT | STRING | "true" | "false" | "nil"
            | IDENT | "(" expr ")" | array | dict | fn_expr ;
array       = "[" ( expr ( "," expr )* )? "]" ;
dict        = "{" ( expr ":" expr ( "," expr ":" expr )* )? "}" ;
fn_expr     = "fn" "(" params ")" block ;
```

---

## License

MIT
