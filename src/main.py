from src.data.loader import DataLoader


def main() -> None:
    loader = DataLoader("data/raw/employees.csv")
    loader.load()
    loader.inspect()


if __name__ == "__main__":
    main()