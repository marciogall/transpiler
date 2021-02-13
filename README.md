# Transpiler from Python to Java

This script is a proof of concept of a transpiler from Python to Java. It has been tested only on simple piece of code and it could be a little bit case specific, but it could be used as a starting part to create a more powerful Python transpiler.
This creation won't be possible without the help of @lauraloperfido and @AlessandroSchiavo


## Usage

Before using the transpiler, make sure you have installed all the requirements by running in a terminal. Consider using a virtual environment.

``` pip install -r requirements.txt ```

To run the transpiler, open a terminal in the directory and type the following command:

``` python Parser.py -i/--input "path/to/input.py" [--verbose] ```

The output will be readable in the directory "output/Output.java".
The --verbose option will return the Abstract Syntax Tree and the Symbol Table created while parsing.

A node of the AST is a Python dictionary:

``` 
self.tree = {
    "node": NODE_NAME,
    "value": NODE_VALUE,
    "type": NODE_TYPE,
    "index": NODE_INDEX,
    "children": NODE_CHILDREN (if any)
}
```

The Symbol Table will be a list of list:

``` 
['VARIABLE_NAME', 'VARIABLE_TYPE', 'VARIABLE_SCOPE', 'FUNC_PARAMETERS', 'LENGTH']
```

## Features

The transpiler will work with this type of data (in Python):
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

It will also recognize this type of construction:
- [x] sum of two numbers
- [x] difference of two numbers
- [x] product of two numbers
- [ ] division of two numbers
- [x] module of two numbers
- [x] if statements
- [x] while statements
- [ ] for statements
- [x] assignment statements
- [x] definition of a function
- [x] call of a function
- [x] comment
- [x] return statements
- [x] user input
- [x] output of a single variable per instruction
- [x] concatenation of lists or tuples
- [x] length of a tuple

We have worked on this type of error:
- [x] grammar error (in particular wrong symbols, but it could be that some of them should be added) with relative row.
- [x] syntax error, with relative row. Because of the type of parsing ply does, the shift-reduce one, with complex structure the error will be found at the end of the specific production.
- [x] semantic errors:
  - [x] declaration of a variable.
  - [x] redeclaration of a variable with the different type. This is an error in Java, not in Python.
  - [x] declaration of a function.
  - [x] invalid operation between different types.
  - [x] list/tuple index out of range.

## Known Issues

In general the transpiler could be a little bit case specific.
All the variables in input will be recognized as Strings and won't be casted, so if you are entering a number you will have to manually cast it in Java in order to use it for other scopes.
All the numbers passed as Object in a function will be casted as Double. It's not so memory friendly, but it's effective.
The transpiler will work only with Python code so formed (the order of the functions doesn't matter, but it matters that all is defined in a function to better understand
the scope of each variable):


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
