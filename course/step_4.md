# Step Four

Before we get started, make a directory named input, `mkdir input`, and copy over the `expenses.csv` and `revenue.csv` files into it.

Note that this is not real data. I took the column headers from the spreadsheets I use to do accounting for my side business, and then used a combination of ChatGPT 4o and Claude 3.5 Sonnet to generate dummy data to use for this course.

## Reading A CSV File

### Part One - Modifying Our ArgumentParser

Let's start simple and first modify our `init_argparse` function to expect a `'f` flag that is the path for the file we want to read.

```python
def init_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="CSV file reader")
    parser.add_argument("-f", dest="file_path", type=str, required=True,
                       help="Path to the CSV file to read")
    return parser
```

To test this, we need to update `print_greeting(args.greetee)` to `print_greeting(args.file_path)`.

Test it!

### Part Two - Reading A Filepath

Now let's first use Python's built-in `pathlib` library to convert our input text into a filepath that the program can open.

```python
from argparse import ArgumentParser, Namespace
from pathlib import Path

def init_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="CSV file reader")
    parser.add_argument("-f", dest="file_path", type=str, required=True,
                       help="Path to the CSV file to read")
    return parser

def main() -> None:
    parser: ArgumentParser = init_argparse()
    args: Namespace = parser.parse_args()

    file_path: Path = Path(args.file_path)
    print(file_path)
```

Test! If you run `python main.py -f input/revenue.csv`, we should get `input/revenue.csv` printed back to the terminal. Leaving out the `input/` should result in an error.

### Part Three - Reading The File

We can now get to reading the contents of the file and printing it back.

Let's make a function called `read_csv_file()` that takes in a `Path` as an argument, and returns a `list[dict[str, str]]`.

*Why a `list[dict[str, str]]`?*

When you read a csv file with `Dictreader`, each row gets converted to a dictionary where the column headers become keys, and the individual row values get mapped to the dictionary values. The values are stored as strings.

If we look at both `revenue.csv` and `expenses.csv`, we have vaues that are dates and numeric. We will cover converting these in a later step.

This one's a bit more complicated than the earlier steps.

First we want to `open` the file using Python's built-in function. We pass in the path to the file as our first argument, and `newline=''` as the second. Operating systems don't all use the same character to mark the end of a line, so `newline=''` lets us handle all three.

Then we want to use `DictReader` from the `csv` package to read in the file we just opened.

Third we want convert the reader into a `list[dict[str, str]]` by using the `list()` function

Finally before we return our data, we want to close out the file. This helps prevent running out of the system's file handles, the resource that tracks access to the file, and it helps prevent locking the file from other programs.

Now that we have all of that wrapped in a `try`/`except` (also called a try/catch).

Why do we have to wrap it? Because we want to avoid accidents, multiple lines that we just covered can fail and throw an exception.

`open` can fail if the file doesn't exist, we don't have permissions to access it, or the disk if corrupted. `DictReader` could fail if the file isn't formatted or encoded correcetly. This last one is an edge case because it would likely fail before getting here, but `list()` could fail if the file is so large the program runs out of memory performing the type conversion.

```python
from argparse import ArgumentParser, Namespace

def read_csv_file(file_path: Path) -> list[dict[str, str]]:
    try:
        csvfile: TextIO = open(file_path, newline='')
        reader: DictReader = DictReader(csvfile)
        data: list[dict[str, str]] = list(reader)
        csvfile.close()
        return data
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        exit(1)
    except PermissionError as e:
        print(f"Permission denied accessing file: {file_path}")
        exit(1)
    except csv.Error as e:
        print(f"Invalid CSV format in {file_path}: {e}")
        exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit(1)
```

Y'all better have not forgot to test.

```python
from argparse import ArgumentParser, Namespace

def main() -> None:
    parser: ArgumentParser = init_argparse()
    args: Namespace = parser.parse_args()

    file_path: Path = Path(args.file_path)
    data: list[dict[str, str]] = read_csv_file(file_path)
    print(data)

if __name__ == "__main__":
    main()
```

## Cleaning Up `read_csv_file`

That was a lot of new things all at once, so we're going to do an easy refactor of the function we just made.

We can replace our `open` with a `with open`. Replace your try block with the following code

```python
    try:
        with open(file_path, newline='') as csvfile:
            reader: DictReader = DictReader(csvfile)
            data: list[dict[str, str]] = list(reader)
            return data
```

Let's break down the line that's doing the heavy lifting. `with` is a context manager (a Python feature that handles the setup and cleanup of resources) keyword. In this case it is telling Python to manage a file. `open(file_path, newline='')` is doing the same as before. And `as csv` names the created resource csvfile. Very similar to what we had before but inverted. Everything after the `:` is "context", and after the block ends, python automatically closes and cleans up any resources within the context.

## Peeking At The Data

First let's keep our `main()` function side effect free and wrap printing out the data from the csv file in a function. We can use a `for` loop to iterate through every `dict` within data.

```python
def display_data(data: list[dict[str, str]]) -> None:
    for row in data:
        print(row)
```

### How Is This Different From `print(data)`?

Both will print the list of dictionaries. The difference is that `display_data()` prints each dictionary on a new line (because it loops through them). While `print(data)` will print the entire list at once in the standard Python list representation with square brackets and commas.

Printing each row individually allows us to leave the door open for granular formatting when printing the dataset.

```python
from argparse import ArgumentParser, Namespace
from pathlib import Path

def display_data(data: list[dict[str, str]]) -> None:
    for row in data:
        print(row)

def main() -> None:
    parser: ArgumentParser  = init_argparse()
    args: Namespace = parser.parse_args()

    file_path: Path = Path(args.file_path)
    data: list[dict[str, str]] = read_csv_file(file_path)
    display_data(data)

if __name__ == "__main__":
    main()
```

Remember to test and commit!

```bash
git add main.py
git add input
git commit -m "step 4: reading csv files"
```
