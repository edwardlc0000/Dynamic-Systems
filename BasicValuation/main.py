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
    tso: int = int(input("Enter total shares outstanding:\t"))
    debt: float = float(input("Enter the debt value:\t\t"))

    try:
        print("Select the Income Statement.")
        income_statement: Dict[str, np.ndarray] = load_file()
        print("Select the Balance Sheet.")
        balance_sheet: Dict[str, np.ndarray] = load_file()
        print("Select the Statement of Cash Flows.")
        statement_of_cash_flow: Dict[str, np.ndarray] = load_file()

        focus_entity: Enterprise = Enterprise(name=name, ticker=ticker, shares_outstanding=tso, debt_value=debt)
        focus_entity.import_statements(income_statement=income_statement,
                                       balance_sheet=balance_sheet,
                                       statement_of_cash_flow=statement_of_cash_flow)

        print(f"Data successfully loaded for {name} ({ticker}).")
    except ValueError as e:
        print(f"Error: {e}")

    projection_data: Dict[str, np.ndarray] = load_file()

    projection_engine = ProjectionEngine(enterprise=focus_entity)
    projection_engine.project_statements(rev_growth=projection_data['Revenue Growth'],
                                         gross_margin=projection_data['Gross Margin'],
                                         opex_sales=projection_data['Operating Expenses (% of Revenue)'],
                                         d_and_a_prior_npp_and_e=projection_data['D&A (% of Prior NPP&E)'],
                                         net_cap_ex_sales=projection_data['Net CapEx (% of Revenue)'],
                                         net_working_capital_sales=projection_data['Net Working Capital (% of Revenue)'])
    projection_engine.project_fcf()

    projection_engine.dcf_model(unlevered_cost_equity=0.08,
                                cost_of_debt=0.05,
                                begin_lev=0.5,
                                growth_rate=0.02)
    print(focus_entity)

if __name__ == "__main__":
    main()