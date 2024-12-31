# Step 3

## Getting Some Reps In With Type Hints

Let's further modify our `main.go` to print a variable named `greetee` and assign "World" as it's value. Then, let's modify our print to print it.

```python
def main() -> None:
    greetee: str = "World"
    print(f"Hello, {greetee}!")

if __name__ == "__main__":
    main()
```

### Why Do We Have An `f` Before Our String?

F-strings are special strings that start with the letter 'f' before the opening quotation mark.

We can embed variables and expressions directly into text by placing them inside curly braces.

When Python sees an f-string, it knows to look inside those curly braces and replace whatever it finds there with the actual values those expressions evaluate to.
your.

### Why Did We Add `: str` After The Variable Name?

The `: str` in `greetee: str = "World"` is a type hint - it explicitly declares that the variable `greetee` should contain a string value.

These are not required, but they help you quickly understand what the kind of value is expected for the variable. This might not matter when we hardcode the value, but it comes in handy when we are want to assign values to function returns.

## Even More Reps with Type Hints

Let's make a function called `get_greetee` that returns "World", because we're returning a string, we're going to mark it with a type hint.

Then, let's change `greetee` from being hardcoded to the value of `get_greetee`

```python
def get_greetee() -> str:
    return "World"

def main() -> None:
    greetee: str = get_greetee()
    print(f"Hello, {greetee}!")

if __name__ == "__main__":
    main()
```

Remember to commit your changes
```bash
git add main.py
git commit -m "step 2: getting in more reps with type hints"
```

Next push this to the cloud.

```bash
git push
```

We're now two steps in, and I still haven't taught y'all to do anything but make an over engineered hello world program. I promise we'll do something more interesting in the next step.
