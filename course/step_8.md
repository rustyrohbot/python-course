# Step 8

## Replacing All Of Our Hard Work With A Library

### Pandas

We just went through a little over a half dozen steps reading data and crunching numbers. What if I told you that a 3rd party library can do it all for us?

First, let's make a file called `requirements.txt`

```bash
touch requirements.txt
```

Then in our new text file, add the following line, `pandas==2.2.3`, the `==` ensured an exact version, in our case, 2.2.3

```bash
echo "pandas==2.2.3" >> requirements.txt
```

Now for this next part, make sure you are in your virtual environment.

Made sure? Good. Now run `pip install -r requirements.txt`. This will take whatever 3rd party libraries are listed in `requirements.txt`. Because we are using a virtual environment, it will install the packages to it instead of system's Python.

This also means if we ever need to switch machines or we lose our data. As long as it is on a git provider and tracks it's dependencies with a `requirements.txt` file, we can always recreate our project.

### Updating Our Imports

Now that we have `pandas` installed to our virtual environment, add `import pandas as pd`. Why are we not using the `from` syntax? We're going to be using multiple components from `pandas`, so in this case, it makes more sense to import all of them and short hand it to pd using `as`.


### Updating How We Read CSV Files

Remember last time how we used a `RevenueTransaction` to encapsulate the data? We can remove all of that because `pandas` has a dedicated type called `DataFrame` that is built to handle tabular data.

So we can take this old `try` block

```python
def read_csv_file(file_path: Path) -> list[RevenueTransaction]:
    try:
        with open(file_path, newline='') as csvfile:
            reader: DictReader = DictReader(csvfile)
            return [RevenueTransaction.from_row(row) for row in reader]
```

And update it to use a `DataFrame` as such

```python
def read_csv_file(file_path: Path) -> pd.DataFrame:
    try:
        df: pd.DataFrame = pd.read_csv(file_path)
        df['Amount'] = (df['Amount']
                       .str.replace('$', '')
                       .str.replace(',', '')
                       .astype(str)
                       .apply(Decimal))
        df['Date'] = pd.to_datetime(df['Date'])
        df['Invoice_Number'] = df['Invoice_Number'].astype(int)

        return df
```

We can directly read the entire csv into the `DataFrame`, and then individually update the data in the entire column for Amount, Date, and Invoice Number. `Pandas` provides some handy functions like `to_datetime()`, `astype()`, and `apply()` to handle type conversions.

### Refactoring Calculations

Now that we have our data converted to a `DataFrame`, we can update all our calculation functions. Let's start with `revenue_by_month_sorted`

```python
def revenue_by_month_sorted(df: pd.DataFrame) -> dict[str, Decimal]:
    monthly: pd.Series = df.groupby(df['Date'].dt.month)['Amount'].sum()
    return dict(sorted(monthly.items()))
```

Let's look at this line because it's doing a lot, `monthly: pd.Series = df.groupby(df['Date'].dt.month)['Amount'].sum()`

First `df['Date'].dt.month`, this extracts the month from each date.

Second, `df.groupby(...)`, this will take whatever `...` is and group the values in the `DataFrame` by it, in our case, it's the month.

Third, `['Amount']`, this will take just the amount column.

Fourth, `.sum()`, we are taking all the values in the column we selected and summing them up.

A `Series` is similar to a flattened dictionary, a list containing pairs of (key, value). So in our final line, we are converting it back to a sorted `dict`.

That same pattern will apply to `annual_revenue`, `revenue_by_client_sorted`, `revenue_by_project_sorted`, and `revenue_by_tool`.

Now let's do `payment_status_summary`.

```python
def payment_status_summary(df: pd.DataFrame) -> dict[str, int]:
    status_counts: pd.Series = df['Payment_Status'].value_counts().sort_index()
    return dict(status_counts)
```

First, `df['Payment_Status']`, we are selecting the `Payment_Status` column.

Second, `value_counts()`, counts each unique value.

Third, `sort_index()`, sorts the values alphabetically

You can repeat this pattern for `invoice_count_by_client`.

Next up, `invoice_count_by_client`.

```python
def invoice_count_by_client(df: pd.DataFrame) -> dict[str, int]:
    invoice_counts: pd.Series = df.groupby('Client').size().sort_index()
    return dict(invoice_counts)
```

First, `groupby('Client')`, we are grouping are values by Client.

Second, `size()`, we are counting the size of each grouping

Third, `sort_index()`, we are sorting the counted values.

And finally returning a `dict` from converting the `Series`

Next up, `projects_per_client_count`

```python
def projects_per_client_count(df: pd.DataFrame) -> dict[str, int]:
    project_counts: pd.Series = df.groupby('Client')['Project'].nunique().sort_index()
    return dict(project_counts)
```

First, `df.groupby('Client')`, we are grouping are values by Client.

Second, `['Project']`, within each group, we are only selecting the Project column

Third, `.nunique()`, will count unique/distinct values (not their total occurrences)

Fourth, `.sort_index()`, we are sorting alphabetically by client name (the original grouping)

And finally return a `dict` like always.

You can repeat this pattern on `average_invoice_by_client`, only instead of `nunique()`, we wil lbe using `mean()` to calculate the average Amount.

### The Last One, Pivot Tables

We are going to update `revenue_by_client_and_tool_sorted` to use a `pivot_table`. A pivot table lets us restructure and reshape our data without making a new `DataFrame`. So let's look at the following.

```python
pivot: pd.DataFrame = df.pivot_table(
    values='Amount',
    index='Client',
    columns='Tool',
    aggfunc='sum',
    fill_value=Decimal('0')
)
```

Going through each parameter: `values` is the data we want to analyze; `index` is what we want our rows to be; `columns` is what we want our columns to be; `aggfunc` refers to the aggregation function we want to use to combine our values; and `fill_value` defines what we will use if data for the combination does not exist.

If you went with the sorted return, you can modify it to use the new pivot table

```python
    return {
        client: dict(sorted(row.items()))
        for client, row in pivot.iterrows()
    }
```

## Git Reps

Now that we've replaced all of our hard with a library, let's get this on the cloud.

```bash
git add requirements.txt
git add main.py
git commit -m "step 8: introducing pandas"
git push
```