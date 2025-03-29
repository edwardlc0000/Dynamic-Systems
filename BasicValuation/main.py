import os
import numpy as np
from typing import Dict
from enterprise import Enterprise
from projectionengine import ProjectionEngine
from dataimport import load_file

def clear_terminal():
    # Check the operating system and execute the appropriate command
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def main():
    print("-------------------------------")
    print("\tBasic Valuation")
    print("-------------------------------")
    print("1. Start the Program.")
    print("2. Exit")

    choice: int = int(input("Choice ->"))

    match choice:
        case 1:
            clear_terminal()
            print("Staring the program...")
        case _:
            clear_terminal()
            print("Exiting program...")
            return

    name: str = input("Enter the company name:\t\t")
    ticker: str = input("Enter the ticker:\t\t")
    tso: int = input("Enter total shares outstanding:\t")
    debt: float = input("Enter the debt value:\t\t")
    try:
        # Launch file dialogs and load data
        income_statement: Dict[str, np.ndarray] = load_file()
        balance_sheet: Dict[str, np.ndarray] = load_file()
        statement_of_cash_flow: Dict[str, np.ndarray] = load_file()

        # Create the Enterprise object and import data
        focus_entity: Enterprise = Enterprise(name=name, ticker=ticker, shares_outstanding=tso, debt_value=debt)
        focus_entity.import_is(income_statement=income_statement)
        focus_entity.import_bs(balance_sheet=balance_sheet)
        focus_entity.import_scf(statement_of_cash_flow=statement_of_cash_flow)

        print(f"Data successfully loaded for {name} ({ticker}).")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()