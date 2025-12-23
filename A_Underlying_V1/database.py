import os
import pandas as pd
from A_Underlying_V1.underlying_class import Underlying

def check_database_exists(path: str) -> bool:
    return os.path.exists(path)

def load_database(path: str) -> pd.DataFrame:
    if check_database_exists(path):
        df = pd.read_csv(path)
        return df
    else:
        raise FileNotFoundError(f"{path} does not exist. Please create the database first.")
        
def save_database(df: pd.DataFrame, path: str):
    if not check_database_exists(path):
        try:
            df.to_csv(path, index=False)
            print(f"Database saved to {path}")
        except Exception as e:
            print(f"An error occurred while saving the database: {e}")
    else:
        try:
            df.to_csv(path, index=False)
            print(f"Database updated to {path}")
        except Exception as e:
            print(f"An error occurred while saving the database: {e}")


def delete_database(path: str):
    if check_database_exists(path):
        if input(f"Are you sure you want to delete {path}? (y/n): ").lower() == 'y':
            os.remove(path)
            print(f"{path} has been deleted.")
        else:
            print("Operation cancelled.")
    else:
        print(f"{path} does not exist.")

def create_database(path: str):
    # Sample data for demonstration
    data = {
        'name': [],
        'symbol': [],
        'exchange': [],
        'type': [],
        'isin': [],
        'description': [],
        'id': []
    }
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    save_database(df, path)
    
    print("Database created and saved to database.csv")

def check_underlying_in_database(isin: str, path: str) -> bool:
    df = load_database(path)
    return isin.upper() in df['isin'].values

def add_underlying_to_database(underlying: Underlying, path: str) -> None:
    df: pd.DataFrame = load_database(path)
    if check_underlying_in_database(underlying.isin, path):
        print(f"Underlying with ISIN {underlying.isin} already exists in the database.")
    else:
        new_entry = {
            'name': underlying.name,
            'symbol': underlying.symbol,
            'exchange': underlying.exchange,
            'type': underlying.type,
            'isin': underlying.isin,
            'description': underlying.description,
            'id': underlying.id
        }
        new_df = pd.DataFrame([new_entry])
        df = pd.concat([df, new_df], ignore_index=True)
        save_database(df, path)
        print(f"Underlying {underlying.name} added to the database.")

def remove_underlying_from_database(isin: str, path: str, force_clause:bool=False) -> None:
    df = load_database(path)
    isin = isin.upper()

    if check_underlying_in_database(isin, path):
        if not force_clause:
            if input(f"Are you sure you want to remove the underlying with ISIN {isin}? (y/n): ").lower() == 'y':
                df = df[df['isin'] != isin]
                save_database(df, path)
                print(f"Underlying with ISIN {isin} has been removed from the database.")
            else:
                print("Operation cancelled.")
        else:
            df = df[df['isin'] != isin]
            save_database(df, path)
            print(f"Underlying with ISIN {isin} has been removed from the database.")

    else:
        print(f"Underlying with ISIN {isin} not found in the database.")

def get_underlying_info_from_database(isin: str, path: str) -> Underlying:
    df = load_database(path)
    isin = isin.upper()
    if check_underlying_in_database(isin, path):
        row = df[df['isin'] == isin].iloc[0]
        underlying = Underlying(
            name=row['name'],
            symbol=row['symbol'],
            exchange=row['exchange'],
            isin=row['isin'],
            type=row['type'],
            description=row['description'],
            id=row['id'],
        )
        return underlying
    else:
        raise ValueError(f"Underlying with ISIN {isin} not found in the database.")
    
def get_all_underlyings_from_database(path: str) -> list[Underlying]:
    df = load_database(path)
    underlyings = []
    for _, row in df.iterrows():
        underlying = Underlying(
            name=row['name'],
            symbol=row['symbol'],
            exchange=row['exchange'],
            isin=row['isin'],
            type=row['type'],
            description=row['description'],
            id=row['id'],
        )
        underlyings.append(underlying)
    return underlyings

def number_of_underlyings_in_database(path: str) -> int:
    df = load_database(path)
    return len(df)

class Database():
    def __init__(self):
        self.file_name: str
        self.path: str

    def create_database(self, path:str):
        create_database(path)

    def start_connection(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} does not exist.")
        else:
            self.path = path
            print(f"Connection to {self.path} established.")

    def end_connection(self):
        print(f"Connection to {self.path} closed.")
        self.path = ""

    def add_underlyings(self, underlyings: list[Underlying]) -> None:
        for underlying in underlyings:
            add_underlying_to_database(underlying, self.path)

    def get_underlying(self, isin: str) -> Underlying:
        return get_underlying_info_from_database(isin, self.path)
    
    def get_underlyings(self, isins: list[str]) -> list[Underlying]:
        underlyings = []
        for isin in isins:
            underlying = self.get_underlying(isin)
            underlyings.append(underlying)
        return underlyings

    def get_all_underlyings(self) -> list[Underlying]:
        return get_all_underlyings_from_database(self.path)

    def remove_underlying(self, isin: str, force_clause: bool) -> None:
        df = load_database(self.path)
        isin = isin.upper()
        if check_underlying_in_database(isin, self.path):
            remove_underlying_from_database(isin, self.path, force_clause)
        else:
            print(f"Underlying with ISIN {isin} not found in the database.")

    def remove_underlyings(self, isins: list[str], force_clause: bool) -> None:
        for isin in isins:
            self.remove_underlying(isin, force_clause)

    def remove_database(self) -> None:
        delete_database(self.path)

    def number_of_underlyings(self) -> int:
        return number_of_underlyings_in_database(self.path)
