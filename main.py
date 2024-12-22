from argparse import ArgumentParser, Namespace
from pathlib import Path
from csv import DictReader, Error
from sys import exit

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