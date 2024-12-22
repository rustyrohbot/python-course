from argparse import ArgumentParser, Namespace

def init_argparse() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="A greeting program")
    parser.add_argument("-g", dest="greetee", type=str, required=True,
                       help="Name of person to greet")
    return parser

def print_greeting(greetee: str) -> None:
    print(f"Hello, {greetee}")

def main() -> None:
    parser: ArgumentParser  = init_argparse()
    args: Namespace = parser.parse_args()
    print_greeting(args.greetee)

if __name__ == "__main__":
    main()