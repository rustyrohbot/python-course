from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import exit
from decimal import Decimal
import pandas as pd

def init_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="CSV file reader")
    parser.add_argument("-f", dest="file_path", type=str, required=True,
                       help="Path to the CSV file to read")
    return parser

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
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit(1)
    except PermissionError:
        print(f"Permission denied accessing file: {file_path}")
        exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit(1)

def revenue_by_month_sorted(df: pd.DataFrame) -> dict[str, Decimal]:
    monthly: pd.Series = df.groupby(df['Date'].dt.month)['Amount'].sum()
    return dict(sorted(monthly.items()))

def annual_revenue(df: pd.DataFrame) -> dict[int, Decimal]:
    yearly: pd.Series = df.groupby(df['Date'].dt.year)['Amount'].sum()
    return dict(yearly)

def revenue_by_client_sorted(df: pd.DataFrame) -> dict[str, Decimal]:
    client_revenue: pd.Series = df.groupby('Client')['Amount'].sum()
    return dict(sorted(client_revenue.items()))

def revenue_by_project_sorted(df: pd.DataFrame) -> dict[str, Decimal]:
    project_revenue: pd.Series = df.groupby('Project')['Amount'].sum()
    return dict(sorted(project_revenue.items()))

def revenue_by_tool(df: pd.DataFrame) -> dict[str, Decimal]:
    tool_revenue: pd.Series = df.groupby('Tool')['Amount'].sum()
    return dict(sorted(tool_revenue.items()))

def payment_status_summary(df: pd.DataFrame) -> dict[str, int]:
    status_counts: pd.Series = df['Payment_Status'].value_counts().sort_index()
    return dict(status_counts)

def invoice_count_by_client(df: pd.DataFrame) -> dict[str, int]:
    invoice_counts: pd.Series = df.groupby('Client').size().sort_index()
    return dict(invoice_counts)

def payment_method_count(df: pd.DataFrame) -> dict[str, int]:
    method_counts: pd.Series = df['Payment_Method'].value_counts().sort_index()
    return dict(method_counts)

def projects_per_client_count(df: pd.DataFrame) -> dict[str, int]:
    project_counts: pd.Series = df.groupby('Client')['Project'].nunique().sort_index()
    return dict(project_counts)

def average_invoice_by_client(df: pd.DataFrame) -> dict[str, Decimal]:
    averages: pd.Series = df.groupby('Client')['Amount'].mean().sort_index()
    return dict(averages)

def revenue_by_client_and_tool_sorted(df: pd.DataFrame) -> dict[str, dict[str, Decimal]]:
    pivot: pd.DataFrame = df.pivot_table(
        values='Amount',
        index='Client',
        columns='Tool',
        aggfunc='sum',
        fill_value=Decimal('0')
    )
    return {
        client: dict(sorted(row.items()))
        for client, row in pivot.iterrows()
    }

def display_monthly_revenue(monthly_data: dict[str, Decimal]) -> None:
    print("\n=== Revenue by Month ===")
    for month, amount in monthly_data.items():
        print(f"Month {month}: ${amount:,.2f}")

def display_annual_revenue(yearly_data: dict[int, Decimal]) -> None:
    print("\n=== Annual Revenue ===")
    for year, amount in yearly_data.items():
        print(f"Year {year}: ${amount:,.2f}")

def display_client_revenue(client_data: dict[str, Decimal]) -> None:
    print("\n=== Revenue by Client ===")
    for client, amount in client_data.items():
        print(f"{client}: ${amount:,.2f}")

def display_project_revenue(project_data: dict[str, Decimal]) -> None:
    print("\n=== Revenue by Project ===")
    for project, amount in project_data.items():
        print(f"{project}: ${amount:,.2f}")

def display_tool_revenue(tool_data: dict[str, Decimal]) -> None:
    print("\n=== Revenue by Tool ===")
    for tool, amount in tool_data.items():
        print(f"{tool}: ${amount:,.2f}")

def display_payment_status(status_data: dict[str, int]) -> None:
    print("\n=== Payment Status Summary ===")
    for status, count in status_data.items():
        print(f"{status}: {count} invoices")

def display_invoice_counts(invoice_data: dict[str, int]) -> None:
    print("\n=== Client Invoice Summary ===")
    for client, count in invoice_data.items():
        print(f"{client}: {count} invoices")

def display_payment_method_counts(payment_method_counts: dict[str, int]) -> None:
    print("\n=== Payment Method Summary ===")
    for payment_method, count in payment_method_counts.items():
        print(f"{payment_method}: {count} invoices")

def display_projects_per_client(projects_per_client: dict[str, int]) -> None:
    print("\n=== Projects per Client ===")
    for client, count in projects_per_client.items():
        print(f"{client}: {count} projects")

def display_average_invoice_amount(average_invoice_amount: dict[str, Decimal]) -> None:
    print("\n=== Average Invoice Amount by Client ===")
    for client, amount in average_invoice_amount.items():
        print(f"{client}: ${amount:,.2f}")

def display_revenue_by_client_and_tool(revenue_by_client_and_tool: dict[str, dict[str, Decimal]]) -> None:
    print("\n=== Revenue by Client and Tool ===")
    for client, tools in revenue_by_client_and_tool.items():
        print(f"\n{client}:")
        for tool, amount in tools.items():
            print(f"  {tool}: ${amount:,.2f}")

def main() -> None:
    parser: ArgumentParser = init_argparse()
    args: Namespace = parser.parse_args()

    file_path: Path = Path(args.file_path)
    df: pd.DataFrame = read_csv_file(file_path)

    # Calculate all metrics
    monthly_revenue_sorted: dict[str, Decimal] = revenue_by_month_sorted(df)
    yearly_revenue_sorted: dict[int, Decimal] = annual_revenue(df)
    client_revenue_sorted: dict[str, Decimal] = revenue_by_client_sorted(df)
    project_revenue_sorted: dict[str, Decimal] = revenue_by_project_sorted(df)
    tool_revenue_sorted: dict[str, Decimal] = revenue_by_tool(df)
    payment_status_counts: dict[str, int] = payment_status_summary(df)
    client_invoice_counts: dict[str, int] = invoice_count_by_client(df)
    payment_method_counts: dict[str, int] = payment_method_count(df)
    projects_per_client: dict[str, int] = projects_per_client_count(df)
    average_invoice_amount: dict[str, Decimal] = average_invoice_by_client(df)
    revenue_by_client_and_tool: dict[str, dict[str, Decimal]] = revenue_by_client_and_tool_sorted(df)

    # Display all results
    display_monthly_revenue(monthly_revenue_sorted)
    display_annual_revenue(yearly_revenue_sorted)
    display_client_revenue(client_revenue_sorted)
    display_project_revenue(project_revenue_sorted)
    display_tool_revenue(tool_revenue_sorted)
    display_payment_status(payment_status_counts)
    display_invoice_counts(client_invoice_counts)
    display_payment_method_counts(payment_method_counts)
    display_projects_per_client(projects_per_client)
    display_average_invoice_amount(average_invoice_amount)
    display_revenue_by_client_and_tool(revenue_by_client_and_tool)

if __name__ == "__main__":
    main()