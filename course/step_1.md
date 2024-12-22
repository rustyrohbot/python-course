# Step One

## Adding Structure

We're starting our with a one-line Python file that prints "Hello, World!.

Before we get into reading data from a CSV file, let's first add some structure to the code that we can then build off of.

Right now our code looks like this:

```python
print("Hello, World!")
```

Let's change it to look like this:

```python
if __name__ == "__main__":
    print("Hello, World!")
```

Run it with `python main.py` to make sure it still prints "Hello, World!" to the terminal.

Now let's make one more change.

```python
def main() -> None:
    print("Hello, World!")

if __name__ == "__main__":
    main()
```

Again. run it with `python main.py` to make sure it still prints "Hello, World!" to the terminal.

Now let's go over the changes we made.

### What Does `if __name__ == "__main__":` Mean?

When you run a Python file directly (like `python main.go`), Python sets a special variable __name__ to "__main__". If you import that file instead, __name__ takes the file’s name.

For the purpose of this course, it's ensuring that the `main()` function gets run first every time we try to run the program.

### What Does `-> None` Mean?

In Python, `-> None` is a type hint that indicates that the function does not return anything back. We will get some more practice with this in the next step.

### Why Use Type Hints?

Type hints aren't required, some say that it adds noise to the codebase, I would argue it makes easier to understand what the code is doing.

### Why Call it `main`?

It is common practice to call the function that is the entrypoint the program `main`. Java was also the first programming language I properly understood, and I like the convention.

### Why add structure?

As we say in the last step, we don't need any of this to have a program that print out "Hello, World!" to the console. But we are going to building a small application through this course and I think structure is important because it allows you to quickly reorient yourself in the codebase if you take a break from it.

## Commit It

Y'all know the drill, we want to `add` and `commit` our change.

```bash
git add main.py
git commit -m "step 1: adding structure"
```
