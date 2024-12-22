# Step 3

## Handling User Input - The Simple Way

Let's modify `get_greetee` to use Python's `input()` function to prompt the user for a value. Note that even if you enter a numeric value, `input()` always returns a string.

```python
def get_greetee() -> str:
    name: str = input("Enter a name: ")
    return name

def main() -> None:
    greetee = get_greetee()
    print(f"Hello, {greetee}!")

if __name__ == "__main__":
    main()
```

Y'all know the drill, test that it works.

## Handling User Input - A More Complicated Way

We like to over engineer here, so let's modify our code to use `sys.argv`. Our goal is to run the following command `python main.py World` and have the terminal print "Hello, World!" back to us.

If we don't pass in any value, we want to print an error message and exit the program.

```python
from sys import exit, argv

def get_greetee() -> str:
    args: list[str] = argv

    if len(args) > 1:
        return args[1]
    print("Error: Please provide a name as a command line argument")
    exit(1)

def main() -> None:
    greetee: str = get_greetee()
    print(f"Hello, {greetee}!")

if __name__ == "__main__":
    main()
```

Y'all know the drill, test it!

### What is `sys` and why are we importing it?

The sys module provides access to some variables used or maintained by Python - it is a way to interact with the Python system itself.

`argv` is a list of strings within `sys` that contains the command line arguments passed to a Python script. argv[0] is always the script name and any additional arguments follow.

`exit` is a function provided by `sys` that can stop the program from running. We can optionally pass in a status code; a status code of 0 indicates a successfull execution, a status code of 1 indicates the program is terminating because of an error.

## Handling User Input - Even More Complicated User Input

We're going to add another layer of complication. We're going to use flags so we can use the following command `python main.go -g World` to print "Hello,World!" to the terminal.

We're first going to make a function called `init_argparse()` that returns an `ArgumentParser`

```python
from argparse import ArgumentParser

def init_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-g", dest="greetee", type=str, required=True,
                       help="Name of person to greet")
    return parser
```

### What Is `ArgumentParser`?

`argparse.ArgumentParser` is a class in Python's standard library that helps handle command line arguments. We can avoid typing out `argparse.ArgumentParser` by modifying `import argparse` to `from argparse ipmort ArgumentParser`. Now we can use `ArgumentParser` by itself in our file.

### Breaking Down `add_argument()`

Let's explain the `add_argument` function within `ArgumentParser`.

We're passing in several argument so let's go down the list:The name of the variable where the value will be stored.

- `"-g"`: The flag that users will type in the command line
- `dest="greetee"`: The name of the variable where the value will be stored
- `type=str`: Specifies that the input should be treated as a string. The parser will attempt to convert the input to this type
- `required=True`: Makes this argument mandatory. If the user doesn't provide the -g flag, the program will show an error message
- `help="Name of person to greet"`: The help text that appears when someone runs the program with --help flag

Now let's modify our code to use this `ArgumentParser`, we can now modify our program to remove our `print()` and `get_greetee()` in `main()`, replacing them with a `print_greeting()` function that takes in string as an argument and prints it with a hello message.

```python
from argparse import ArgumentParser, Namespace

def init_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="A greeting program")
    parser.add_argument("-g", dest="greetee", type=str, required=True,
                       help="Name of person to greet")
    return parser

def print_greeting(greetee: str) -> None:
    print(f"Hello, {greetee}")

def main() -> None:
    parser: ArgumentParser = init_argparse()
    args: Namespace = parser.parse_args()
    print_greeting(args.greetee)

if __name__ == "__main__":
    main()
```

Test, test, test!

### What's `Namespace`?

A `Namespace` in `argparse` is like a simple container that holds your parsed arguments, it allows us to reference arguments from the command line as though it were an Object in Python

Let's commit these changes

```bash
git add main.py
git commit -m "step 3: handling user input
```

Next up, we're going to modify our program to read in a file and write out its contents.
