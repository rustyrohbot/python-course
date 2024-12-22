def get_greetee() -> str:
    return "World"

def main() -> None:
    greetee: str = get_greetee()
    print(f"Hello, {greetee}!")

if __name__ == "__main__":
    main()