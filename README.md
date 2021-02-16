# Transpiler from Python to Java

This script is a proof of concept of a transpiler from Python to Java.
This creation couldn't be possible without the help of @lauraloperfido and @AlessandroSchiavo.


## Usage

You can compile the code with the help of PyInstaller.

After you've done it, you can run the transpiler by opening a terminal in the project directory and typing the following command:

``` transpiler.exe -i/--input "path/to/input.py" [--verbose] ```

The output will be readable in the directory "output/output.java".
The --verbose option will return the Abstract Syntax Tree and the Symbol Table created while parsing.

A node of the AST is a Python dictionary:

``` 
tree = {
    "node": NODE_NAME,
    "value": NODE_VALUE,
    "type": NODE_TYPE,
    "index": NODE_INDEX,
    "children": NODE_CHILDREN
}
```

The Symbol Table will be a list of lists:

```
['VARIABLE_NAME', 'VARIABLE_TYPE', 'VARIABLE_SCOPE', 'FUNC_PARAMETERS', 'LENGTH']
```

## Features

The transpiler will work with these types of data (in Python):
- [x] int
- [ ] long
- [x] float
- [ ] complex
- [x] bool
- [x] str
- [x] tuple
- [ ] frozenset
- [x] list
- [ ] dict
- [ ] set
- [ ] file

It will also recognize these types of operations:
- [x] sum of two numbers
- [x] difference between two numbers
- [x] multiplication of two numbers
- [ ] division of two numbers
- [x] module of two numbers
- [x] if statements
- [x] while statements
- [ ] for statements
- [x] assignment statements
- [x] definition of a function
- [x] call of a function
- [x] return statements
- [x] user input
- [x] output of a single variable per instruction
- [x] concatenation of lists or tuples
- [x] length of lists or tuples

We have worked on these types of errors:
- [x] lexical error (wrong symbols sometimes are missing) with relative row.
- [x] syntax error, with relative row. Because of the type of parsing ply does, the shift-reduce one, with complex structures the error will be found at the end of the specific rule.
- [x] semantic errors:
  - [x] missing declaration of a variable.
  - [x] redeclaration of a variable with a different type (this is an error in Java, not in Python).
  - [x] missing declaration of a function.
  - [x] invalid operation between different types.
  - [x] list/tuple index out of range.

## Known Issues

All the variables in input will be recognized as Strings and won't be casted, so if you are entering a number you will have to manually cast it in Java in order to use it for other scopes.
All the numbers passed as Object in a function will be casted as Double.
The transpiler will work only with Python code built this way (the order of the functions doesn't matter, but it's important that everything is defined in a function to better understand the scope of each variable):


``` 
def first_function(first_function_parameters):
    # body of first function
    
[...]

def n_function(n_function_parameters):
    # body of n function
    
def main():
    # body of main


if __name__ == "__main__":
    main()

```
