# Step Five

Okay, five steps in. I promse we're going to do something more fun than printing data to a screen.

But first, let's talk about what it is we're trying to accomplish here.

My goal for the end of this course is to have y'all build out a cli application that can read data from a source, analyze it, and then visualize it. But that's not all, what I just described can be a simple script.

We aim for the stars here. What we are going to do is build an application that can read in data from a variety of sources (csv, excel, sheets, sql), we are going make pretty charts with that data, and we are going to over engineer it.

Why?

Because I refuse to use spreadsheets software any more than I absolutely need to. Gimme a clean data source and Python can do wonders.

Now without further ado, let's start getting some stats.

## Monthly Revenue Statistics

Let's start crunching numbers. We left off with a `list` of `dict`s of `str:str` key-value pairs called data. Instead of printing each row, let's try to figure out what our revenue per month is.

Let's make a function called `revenue_by_month` that expects a `list[dict[str, str]]` and returns a `dict[str, float]`.

First let's make initialize a dict called `monthly_revenue` that's a `dict` where the key is a `str` and the value is a `float`.

Next we want to loop through every row in data, which we know is a `list[dict[str, str]]`. So we're in the loop.

Let's first extract the month by getting the value for 'Date' in the row, then split it by '/', and then get the first value in the resuling list. With function chaining, we can do all of this in the same statement, `month: str = row['Date'].split('/')[0]`. Test by printing it.

Second, let's get the amount. Remember that our values have both a "$" to mark the currency and ","s. Python supports a `replace()` function on variables/values that are `str`s, so we can replace those chracters with empty strings. Then finally we want to wrap the whole chain with a `float()` to convert to a type that we perform math on. I am opting to do it in a single statment but it will also work if you break it into multiple statements. `amount: float = float(row['Amount'].replace('$', '').replace(',', ''))`. Again, test by printing it.

What next?

We have a variable called monthly_revenue that is a `dict[str,float]`, within our loop, month is a `str` and amount is a `float`. Some simple grouping and addition can make monthly_revenue hold data representative of its namesake. We can do this with either `monthly_revenue[month] = monthly_revenue[month] +1` or `monthly_revenue[month] += 1`, in my code I am going with the latter. We've been priting a lot to the terminal. Let's move our print to the end of the loop

Try running it now. An error right? See, this is why we test.

It's a `KeyError`, this means that our `dict` does not have a value. In a little bit we'll guard against this by wrapping a `try`/`except`, but erroring out doesn't solve our problem, we want to add numbers. We can fix this by initializing a value if the key does not exist. We can use an `if` statement to initialize the value to zero.

```python
if month not in monthly_revenue:
    monthly_revenue[month] = 0.0
```

If we test this, we should see a dictionary with 12 keys, one for each month.

We saw that we can get a `KeyError`, a `ValueError` can also occur so let's guard against this by wrapping it.

Our function should now look like this

```python
def revenue_by_month(data: list[dict[str, str]]) -> dict[str, float]:
    monthly_revenue: dict[str, float] = {}

    for row in data:
        try:
            month: str = row['Date'].split('/')[0]
            amount: float = float(row['Amount'].replace('$', '').replace(',', ''))

            if month not in monthly_revenue:
                monthly_revenue[month] = 0.0

            monthly_revenue[month] += amount

        except ValueError as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {e}")
            exit(1)
        except KeyError as e:
            print(f"Missing required field in row: {row}")
            print(f"Error details: {e}")
            exit(1)

    return monthly_revenue
```

### Tidying Up

First let's add `from collections import defaultdict`, and then replace the current `monthly_revenue` with a `monthly_revenue: defaultdict[str, float] = defaultdict(float)`. `defaultdict` is a wrapper class or subclass of `dict` that defaults missing keys based on the type it is initialized with. In our case, `float` defaults to 0.0. Now we can remove our `if`.

Because we overengineer here, let's pull the logic for row and amount into their own functions.I'm only giving y'all the function headers this time, it's on y'all to move it over. `def get_month_from_cell(date: str) -> str:` and `def get_amount_from_cell(amount: str) -> float:`.

Now let's sort our dictionary, we're not going into sorting algorithms in this course, so we're going to use the built in functions. Replace the return for `revenue_by_month` with `dict(sorted(monthly_revenue.items()))`.

Let's break that down, `sorted()` is a function that takes in an `Iterable`, and returns a sorted `list`. If we pass in a `list` of `tuple`s, it sorts by the first item in the tuple. `items()` takes all the entries in the `dict` and flattens them into something that Python will accept as a `list` of `tuple`s. Finally `dict()` takes that flattened `list` and makes it a `dict` again.

We're going to do one last thing, we are going to add an `from decimal import Decimal` and update our `float`s to `Decimal`s. Without going into all the techincal details, `Decimal` is more precise than `float`, and because while fake, this is financial data, it is a good excuse to use it.

Next up, let's keep our main free of side effects and define a function that prints our monthly revenue in a way that's easier to read than a single line.

Because we're now returning a sorted list, I updated the function and variable names. Here is how mine looks in the end.

```python
from sys import exit
from collections import defaultdict
from decimal import Decimal

def get_month_from_cell(date: str) -> str:
    return date.split('/')[0]

def get_amount_from_cell(amount: str) -> Decimal:
    return Decimal(amount.replace('$', '').replace(',', ''))

def revenue_by_month_sorted(data: list[dict[str, str]]) -> dict[str, Decimal]:
    monthly_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)

    for row in data:
        try:
            month: str = get_month_from_cell(row['Date'])
            amount: Decimal = get_amount_from_cell(row['Amount'])
            monthly_revenue[month] += amount
        except ValueError as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {e}")
            exit(1)
        except KeyError as e:
            print(f"Missing required field in row: {row}")
            print(f"Error details: {e}")
            exit(1)

    return dict(sorted(monthly_revenue.items()))

def display_monthly_revenue(monthly_data: dict[str, Decimal]) -> None:
    print("\n=== Revenue by Month ===")
    for month, amount in monthly_data.items():
        print(f"Month {month}: ${amount:,.2f}")

def main() -> None:
    parser: ArgumentParser  = init_argparse()
    args: Namespace = parser.parse_args()

    file_path: Path = Path(args.file_path)
    data: list[dict[str, str]] = read_csv_file(file_path)

    monthly_revenue_sorted: dict[str, Decimal] = revenue_by_month_sorted(data)
    display_monthly_revenue(monthly_revenue_sorted)
```

## Reps, Reps, Reps

Now that we've covered one, let's go through adding some more number crunching. Let's go through making the following functions:

- `def annual_revenue(data: list[dict[str, str]) -> dict[int, Decimal]:`

- `def revenue_by_client_sorted(data: list[dict[str, str]]) -> dict[str, Decimal]:`

- `def revenue_by_project_sorted(data: list[dict[str, str]]) -> dict[str, Decimal]:`

- `def revenue_by_tool(data: list[dict[str, str]]) -> dict[str, Decimal]:`

- `def payment_status_summary(data: list[dict[str, str]]) -> dict[str, int]:`

I'm gonna leave y'all to do those yourselves and making their corresponding print functions. `main.py` in this repo's root will have my version if you get stuck. But all of their patterns are the same or similar to what we did for `revenue_by_month_sorted()`.

You can simplify the `try`/`except` block by handling both errors the same way. Here is an example with `revenue_by_month_sorted()`

There's a simple and a complicated way to implement `annual_revenue()`, I'll let y'all guess which one I picked.

```python
def revenue_by_month_sorted(data: list[dict[str, str]]) -> dict[str, Decimal]:
    monthly_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)

    for row in data:
        try:
            month: str = get_month_from_cell(row['Date'])
            amount: Decimal = get_amount_from_cell(row['Amount'])
            monthly_revenue[month] += amount
        except (ValueError, KeyError) as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {e}")
            exit(1)
```

## Commit and Push

```bash
git add main.py
git add input
git commit -m "step 5: starting to crunch numbers"
```

And then push!

```bash
git push
```
