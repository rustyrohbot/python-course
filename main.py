from argparse import ArgumentParser, Namespace
from pathlib import Path
from csv import DictReader, Error
from sys import exit
from collections import defaultdict
from decimal import Decimal

def init_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="CSV file reader")
    parser.add_argument("-f", dest="file_path", type=str, required=True,
                       help="Path to the CSV file to read")
    return parser

def read_csv_file(file_path: Path) -> list[dict[str, str]]:
    try:
        with open(file_path, newline='') as csvfile:
            reader: DictReader = DictReader(csvfile)
            data: list[dict[str, str]] = list(reader)
            return data
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

def get_month_from_cell(date: str) -> str:
    return date.split('/')[0]

def get_year_from_cell(date: str) -> int:
    return int(date.split('/')[-1])

def get_amount_from_cell(amount: str) -> Decimal:
    return Decimal(amount.replace('$', '').replace(',', ''))

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

def annual_revenue(data: list[dict[str, str]]) -> dict[int, Decimal]:
    yearly_revenue: defaultdict[int, Decimal] = defaultdict(Decimal)

    for row in data:
        try:
            year: int = get_year_from_cell(row['Date'])
            amount: Decimal = get_amount_from_cell(row['Amount'])
            yearly_revenue[year] += amount
        except (ValueError, KeyError) as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {e}")
            exit(1)

    return dict(sorted(yearly_revenue.items()))

def revenue_by_client_sorted(data: list[dict[str, str]]) -> dict[str, Decimal]:
    client_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)

    for row in data:
        try:
            client: str = row['Client']
            amount: Decimal = get_amount_from_cell(row['Amount'])
            client_revenue[client] += amount
        except (ValueError, KeyError) as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {e}")
            exit(1)

    return dict(sorted(client_revenue.items()))

def revenue_by_project_sorted(data: list[dict[str, str]]) -> dict[str, Decimal]:
    project_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)

    for row in data:
        try:
            project: str = row['Project']
            amount: Decimal = get_amount_from_cell(row['Amount'])
            project_revenue[project] += amount
        except (ValueError, KeyError) as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {e}")
            exit(1)

    return dict(sorted(project_revenue.items()))

def revenue_by_tool(data: list[dict[str, str]]) -> dict[str, Decimal]:
    tool_revenue: defaultdict[str, Decimal] = defaultdict(Decimal)

    for row in data:
        try:
            tool: str = row['Tool']
            amount: Decimal = get_amount_from_cell(row['Amount'])
            tool_revenue[tool] += amount
        except (ValueError, KeyError) as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {e}")
            exit(1)

    return dict(sorted(tool_revenue.items()))

def payment_status_summary(data: list[dict[str, str]]) -> dict[str, int]:
    status_count: defaultdict[str, int] = defaultdict(int)

    for row in data:
        try:
            status: str = row['Payment_Status']
            status_count[status] += 1
        except KeyError as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {e}")
            exit(1)

    return dict(sorted(status_count.items()))

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

def main() -> None:
    parser: ArgumentParser = init_argparse()
    args: Namespace = parser.parse_args()

    file_path: Path = Path(args.file_path)
    data: list[dict[str, str]] = read_csv_file(file_path)

    monthly_revenue_sorted: dict[str, Decimal] = revenue_by_month_sorted(data)
    yearly_revenue_sorted: dict[int, Decimal] = annual_revenue(data)
    client_revenue_sorted: dict[str, Decimal] = revenue_by_client_sorted(data)
    project_revenue_sorted: dict[str, Decimal] = revenue_by_project_sorted(data)
    tool_revenue_sorted: dict[str, Decimal] = revenue_by_tool(data)
    payment_status_counts: dict[str, int] = payment_status_summary(data)

    display_monthly_revenue(monthly_revenue_sorted)
    display_annual_revenue(yearly_revenue_sorted)
    display_client_revenue(client_revenue_sorted)
    display_project_revenue(project_revenue_sorted)
    display_tool_revenue(tool_revenue_sorted)
    display_payment_status(payment_status_counts)

if __name__ == "__main__":
    main()