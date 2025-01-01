from argparse import ArgumentParser, Namespace
from pathlib import Path
from csv import DictReader, Error
from sys import exit
from collections import defaultdict
from decimal import Decimal
from dataclasses import dataclass
from datetime import date
from typing import Optional

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

def init_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="CSV file reader")
    parser.add_argument("-f", dest="file_path", type=str, required=True,
                       help="Path to the CSV file to read")
    return parser

def read_csv_file(file_path: Path) -> list[RevenueTransaction]:
    try:
        with open(file_path, newline='') as csvfile:
            reader: DictReader = DictReader(csvfile)
            return [RevenueTransaction.from_row(row) for row in reader]
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        exit(1)
    except PermissionError as e:
        print(f"Permission denied accessing file: {file_path}")
        exit(1)
    except Error as e:
        print(f"Invalid CSV format in {file_path}: {e}")
        exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit(1)

def revenue_by_month_sorted(transactions: list[RevenueTransaction]) -> dict[str, Decimal]:
    monthly_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)
    for t in transactions:
        monthly_revenue[str(t.date.month)] += t.amount
    return dict(sorted(monthly_revenue.items()))

def annual_revenue(transactions: list[RevenueTransaction]) -> dict[int, Decimal]:
    yearly_revenue: defaultdict[int, Decimal] = defaultdict(Decimal)
    for t in transactions:
        yearly_revenue[t.date.year] += t.amount
    return dict(sorted(yearly_revenue.items()))

def revenue_by_client_sorted(transactions: list[RevenueTransaction]) -> dict[str, Decimal]:
    client_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)
    for t in transactions:
        client_revenue[t.client] += t.amount
    return dict(sorted(client_revenue.items()))

def revenue_by_project_sorted(transactions: list[RevenueTransaction]) -> dict[str, Decimal]:
    project_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)
    for t in transactions:
        project_revenue[t.project] += t.amount
    return dict(sorted(project_revenue.items()))

def revenue_by_tool(transactions: list[RevenueTransaction]) -> dict[str, Decimal]:
    tool_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)
    for t in transactions:
        tool_revenue[t.tool] += t.amount
    return dict(sorted(tool_revenue.items()))

def payment_status_summary(transactions: list[RevenueTransaction]) -> dict[str, int]:
    status_count: defaultdict[str, int] = defaultdict(int)
    for t in transactions:
        status_count[t.payment_status] += 1
    return dict(sorted(status_count.items()))

def invoice_count_by_client(transactions: list[RevenueTransaction]) -> dict[str, int]:
    invoice_counts: defaultdict[str, int] = defaultdict(int)
    for t in transactions:
        invoice_counts[t.client] += 1
    return dict(sorted(invoice_counts.items()))

def payment_method_count(transactions: list[RevenueTransaction]) -> dict[str, int]:
    method_counts: defaultdict[str, int] = defaultdict(int)
    for t in transactions:
        method_counts[t.payment_method] += 1
    return dict(sorted(method_counts.items()))

def projects_per_client_count(transactions: list[RevenueTransaction]) -> dict[str, int]:
    client_projects: defaultdict[str, int] = defaultdict(int)
    for t in transactions:
        client_projects[t.client] += 1
    return dict(sorted(client_projects.items()))

def average_invoice_by_client(transactions: list[RevenueTransaction]) -> dict[str, Decimal]:
    total_amount: defaultdict[str, Decimal] = defaultdict(Decimal)
    invoice_count: defaultdict[str, int] = defaultdict(int)

    for t in transactions:
        total_amount[t.client] += t.amount
        invoice_count[t.client] += 1

    averages: dict[str, Decimal] = {}
    for client in total_amount:
        if invoice_count[client] > 0:
            averages[client] = total_amount[client] / invoice_count[client]

    return dict(sorted(averages.items()))

def revenue_by_client_and_tool_sorted(transactions: list[RevenueTransaction]) -> dict[str, dict[str, Decimal]]:
    result: dict[str, dict[str, Decimal]] = {}

    for t in transactions:
        if t.client not in result:
            result[t.client] = {}
        if t.tool not in result[t.client]:
            result[t.client][t.tool] = Decimal('0')

        result[t.client][t.tool] += t.amount

    return {
        client: dict(sorted(tools.items()))
        for client, tools in sorted(result.items())
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
    transactions: list[RevenueTransaction] = read_csv_file(file_path)

    monthly_revenue_sorted: dict[str, Decimal] = revenue_by_month_sorted(transactions)
    yearly_revenue_sorted: dict[int, Decimal] = annual_revenue(transactions)
    client_revenue_sorted: dict[str, Decimal] = revenue_by_client_sorted(transactions)
    project_revenue_sorted: dict[str, Decimal] = revenue_by_project_sorted(transactions)
    tool_revenue_sorted: dict[str, Decimal] = revenue_by_tool(transactions)
    payment_status_counts: dict[str, int] = payment_status_summary(transactions)

    display_monthly_revenue(monthly_revenue_sorted)
    display_annual_revenue(yearly_revenue_sorted)
    display_client_revenue(client_revenue_sorted)
    display_project_revenue(project_revenue_sorted)
    display_tool_revenue(tool_revenue_sorted)
    display_payment_status(payment_status_counts)

    client_invoice_counts: dict[str, int] = invoice_count_by_client(transactions)
    payment_method_counts: dict[str, int] = payment_method_count(transactions)
    projects_per_client: dict[str, int] = projects_per_client_count(transactions)
    average_invoice_amount: dict[str, Decimal] = average_invoice_by_client(transactions)
    revenue_by_client_and_tool: dict[str, dict[str, Decimal]] = revenue_by_client_and_tool_sorted(transactions)

    display_invoice_counts(client_invoice_counts)
    display_payment_method_counts(payment_method_counts)
    display_projects_per_client(projects_per_client)
    display_average_invoice_amount(average_invoice_amount)
    display_revenue_by_client_and_tool(revenue_by_client_and_tool)

if __name__ == "__main__":
    main()