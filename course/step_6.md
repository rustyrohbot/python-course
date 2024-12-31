# Step 6

We did a lot in that last step, so we're going to focus on some more reps before introducing a new concept.

Remember the pattern from last time, we are writing functions that expect a `list[dict[str, str]]` as an input.

## More Stats

### Count Invoice By Client

Let's start simple by adding the following function, `def invoice_count_by_client(data: list[dict[str, str]]) -> dict[str, int]:`.

We want to initialize our return value, and loop through each row, and count the number of times that a `row['Client']` appears. Remember to wrap a `try`/`except` to guard against a `KeyError`

We're keeping our `main` function side-effect free, so let's write a function to print out the `dict[str, int]` we get back from our count function.


## Count By Payment Method

We're gonna get some more reps in with grouping similar values, let's make another function, `def payment_method_count(data: list[dict[str, str]]) -> dict[str, int]:`.

Same as before, we want to initialize our return value, and loop through each row, and count the number of times that a `row['Payment_Method']` appears. Remember to wrap a `try`/`except` to guard against a `KeyError`

And remember, after testing, move your prints into their own function that expects a `dict[str, int]`

## Count Projects By Client

This time I'm only gonna give the function definition. Follow the same pattern we've been doing to implement the function to count the number of projects each client has. Then write a function to print the returned value.

`def projects_per_client_count(data: list[dict[str, str]]) -> dict[str, int]:`

## Moving Onto Averages

We've done a couple functions now where we count matching values, let's now try calculating the average invoice amount by client. This time we're going to initialize two variables, `total_amount: defaultdict[str, Decimal] = defaultdict(Decimal)` and `invoice_count: defaultdict[str, int] = defaultdict(int)`. One to keep track of the total amount per client, and one to keep track of invoices per client.

First we want to loop through every row in our data, and update two values, we wantto add amount to ` total_amount[client]` and increment `invoice_count[client] += 1`. (Remember to guard against `KeyErrors`)

Now let's introduce a new variable, `averages: dict[str, Decimal]`

And then loop through the clients in `total_amount`, when `invoice_count[client]` is greater than 0, we want to update `averages[client] to be total_amount[client] divided by invoice_count[client].

Finally, implement a print function.

*Note*, this is not an ideal way to implement this, what we're focusing on for this step is building up fundamentals when it comes to parsing and looping through data.

## Calculating Revenue By Client And Tool

Now we're gonna get into some grouping. Again, this is not the optimal way to implment the function, what we care about right now is building up a strong understanding of the basics.

Our function starts with this, `def revenue_by_client_and_tool_sorted(data: list[dict[str, str]]) -> dict[str, dict[str, Decimal]]:`

Notice how this time we are returning a dictionary where the key is a string, but the value is another dictionary. What we want to do is map a client to a tool, and counting the matching values per client.

First let's initalize the return `result: dict[str, dict[str, Decimal]] = {}`, we're not using a `defaultdict` this time because introducing lambdas this early is out of scope for this step

So what we want to do is loop through every row in data, In each cycle, extract the client, tool, and amount. With all of this, we can use the square brackets to reference nested values. Which means that we can do `result[client][tool] += amount` to increase the amount on a matching client-tool grouping.

Remember that we didn't use a `defaultdict`, so we need to initalize values if their isn't an existing one.

I've been sorting my return values, y'all don't have to, but if you want to, this one a is also bit tricky.

``` python
    return {
        client: dict(sorted(tools.items()))
        for client, tools in sorted(result.items())
    }
```

Remember the print function!

## Wrapping Up

Y'all know the drill: `add`, `commit`, and `push`

```bash
git add main.py
git commit -m "step 6: more stats, more reps"
git push
```

Next up, we're going to add classes, and then introduce a 3rd party library that can more easily do what we've covered in steps 5 and 6.