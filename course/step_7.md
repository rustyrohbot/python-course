# Step 7

I'm gonna be honest here, I don't know is abstracting the row data to a class is useful for the scope of this course, but I think they're useful to know, so I'm including it.

## Classes

So what is a class? A class is similar to a blueprint or template to encapsulate your data and related functions.

What data can we encapsulate? If you look at the CSV that we are parsing, the column headers are: Date,Amount,Invoice_Number,Project,Service,Client,Tool,Payment_Status,Payment_Method.

We can capture the data like this:

```python
@dataclass
class RevenueTransaction:
    date: date
    amount: Decimal
    invoice_number: int
    project: str
    service: str
    client: str
    tool: str
    payment_status: str
    payment_method: str
```

### What is a `@dataclass`?

This a decorator we add to a class that will tell it to automatically add common functionality. Without we have to define explicit functions to construct, toString, and equals two instances of the class.

This is what we would have to do without using the decorator

```python
class RevenueTransaction:
    # Constructor
    def __init__(self, date, amount, invoice_number, project, service, client, tool, payment_status, payment_method):
        self.date = date
        self.amount = amount
        self.invoice_number = invoice_number
        self.project = project
        self.service = service
        self.client = client
        self.tool = tool
        self.payment_status = payment_status
        self.payment_method = payment_method
    # Converts the class to a formatted string
    def __repr__(self):
        return (f"RevenueTransaction(date={self.date}, amount={self.amount}, "
                f"invoice_number={self.invoice_number}, project={self.project}, "
                f"service={self.service}, client={self.client}, tool={self.tool}, "
                f"payment_status={self.payment_status}, payment_method={self.payment_method})")

    # Compares this instance of the class against another, checking if they're equal
    def __eq__(self, other):
        if not isinstance(other, RevenueTransaction):
            return NotImplemented
        return (self.date == other.date and
                self.amount == other.amount and
                self.invoice_number == other.invoice_number and
                self.project == other.project and
                self.service == other.service and
                self.client == other.client and
                self.tool == other.tool and
                self.payment_status == other.payment_status and
                self.payment_method == other.payment_method)
```

### Functions In The Class

Next we want to add a function that will take in a row, and from it return an instance of `RevenueTransaction`.

We are decorating the function with a `@classmethod` decorator which tells Python that this function belongs to the `RevenueTransaction` class. This also means that are first parameter in the function with `cls` for class itself instead of `self` to reference an instancelike the previous explanation.

```python
class RevenueTransaction:
    @classmethod
    def from_row(cls, row: dict[str, str]) -> 'RevenueTransaction':
        date_parts: list[str] = row['Date'].split('/')
        return cls(
            date=date(int(date_parts[2]), int(date_parts[0]), int(date_parts[1])),
            amount=Decimal(row['Amount'].replace('$', '').replace(',', '')),
            invoice_number=int(row['Invoice_Number']),
            project=row['Project'],
            service=row['Service'],
            client=row['Client'],
            tool=row['Tool'],
            payment_status=row['Payment_Status'],
            payment_method=row['Payment_Method']
        )
```

We start off with splitting the date into parts. Then we return a `cls()` where `cls` is a `RevenueTransaction`. So, we then assign values from the respective rows. The exception being date where we are now going to use the parts to construct a `date` instead of an int like before.

Notice in amount how we clean the data in-line. These help remove the need for us to have the dedicated functions we had before for `def get_month_from_cell(date: str) -> str:`, `def get_year_from_cell(date: str) -> int:`, and `def get_amount_from_cell(amount: str) -> Decimal:`

## Refactoring The Code

Now let's update the rest of our code to use this new class.

We're gonna first start with our `read_csv_file` function. We want to change our return type to a `list[RevenueTransaction]`.

Now let's look at our original logic in the `try` block

```python
    try:
        with open(file_path, newline='') as csvfile:
            reader: DictReader = DictReader(csvfile)
            data: list[dict[str, str]] = list(reader)
            return data
```

Notice how we first get a `DictReader` from the csv file. Then we convert that reader to a `dict`, and then return it.

We can follow the pattern and update our block to look like this.

```python
    try:
        with open(file_path, newline='') as csvfile:
            reader: DictReader = DictReader(csvfile)
            transactions: list[RevenueTransaction] = []
            for row in reader:
                transaction = RevenueTransaction.from_row(row)
                transactions.append(transaction)
            return transactions
```

Here first initalize an empty list, and then loop through each row in reader to first extract the row, and then append it to the initialized list.

This is a perfectly valid way to implement the function. If we want to be more pythonic, we can use a list comprehension to create a list from a loop in a single line.

```python
    try:
        with open(file_path, newline='') as csvfile:
            reader: DictReader = DictReader(csvfile)
            return [RevenueTransaction.from_row(row) for row in reader]
```

Both are valid, I am opting to use list comprehension in my copy.

### More Refactoring

We updated the function that reads in our file. We now need to update all of our calculation functions. I'm going to start by giving y'all one, but the rest are on you.

Let's start with `revenue_by_month_sorted`.

Currently we have this

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

    return dict(sorted(monthly_revenue.items()))
```

We can simplify it down to this

```python
def revenue_by_month_sorted(transactions: list[RevenueTransaction]) -> dict[str, Decimal]:
    monthly_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)
    for t in transactions:
        monthly_revenue[str(t.date.month)] += t.amount
    return dict(sorted(monthly_revenue.items()))
```

Because the date field in `RevenueTransaction` is a date, we can use `date.month` to get the month and convert it to a string. We can also remove the `try`/`except`.

Now it's up to y'all to update the rest.

Remember to update your type hints!

## Push It

Like always, we want to:  `add`, `commit`, and `push`

```bash
git add main.py
git commit -m "step 6: more stats, more reps"
git pus
```