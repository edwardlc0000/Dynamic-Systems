# basicvaluation.py
# Created On: 2025-03-22
# Created By: Edward Cromwell
# An exploration of basic valuations of US corporations using numerical methods

import numpy as np
import pandas as pd
from typing import Dict
from typing import Final

# Define a constant for the statutory tax rate
stat_tax_rate: Final[float] = 0.21


class Enterprise:

    """
    Initialize an Enterprise instance.

    Args:
        name (str): The name of the company.
        ticker (str): The stock ticker symbol of the company.
        shares_outstanding (int): The number of shares outstanding.
        pointer (int): A pointer to track the current period (default is 0).
    """
    def __init__(self, name: str, ticker: str, shares_outstanding: int, pointer: int = 0):
        self.name: str = name
        self.ticker: str = ticker
        self.shares_outstanding: int = shares_outstanding
        self.pointer: int = pointer
        self.value: float = None

        self.income_statement: Dict[str, np.ndarray] = {
            'Revenue': np.array([]),
            'Cost of Sales': np.array([]),
            'Gross Profit': np.array([]),
            'Op. Ex.': np.array([]),
            'EBITDA': np.array([]),
            'D&A': np.array([]),
            'EBIT': np.array([]),
            'Interest': np.array([]),
            'Tax': np.array([]),
            'Net Income': np.array([])
        }

        self.balance_sheet: Dict[str, np.ndarray] = {
            'Cash': np.array([]),
            'Current Assets': np.array([]),
            'Net PP&E': np.array([]),
            'Current Liabilities': np.array([]),
            'Long-Term Debt': np.array([]),
            'Net Working Capital': np.array([])
        }

        self.statement_of_cash_flow: Dict[str, np.ndarray] = {
            'D&A': np.array([]),
            'Net Cap. Ex.': np.array([]),
            'Cap. Ex.': np.array([]),
        }

    def import_statements(self,
                          income_statement: Dict[str, np.ndarray],
                          balance_sheet: Dict[str, np.ndarray],
                          statement_of_cash_flow: Dict[str, np.ndarray]):
        self.validate_statements(income_statement,
                                 balance_sheet,
                                 statement_of_cash_flow)
        self.import_is(income_statement)
        self.import_bs(balance_sheet)
        self.import_scf(statement_of_cash_flow)

    """
    Import data into the income statement.

    Args: income_statement (Dict[str, np.ndarray]): A dictionary containing income statement data.
    """
    def import_is(self, income_statement: Dict[str, np.ndarray]):
        self.income_statement = self.income_statement | income_statement

    """
    Import data into the balance sheet.

    Args: balance_sheet (Dict[str, np.ndarray]): A dictionary containing balance sheet data.
    """
    def import_bs(self, balance_sheet: Dict[str, np.ndarray]):
        self.balance_sheet = self.balance_sheet | balance_sheet

    """
    Import data into the statement of cash flows.

    Args: statement_of_cash_flow (Dict[str, np.ndarray]): A dictionary containing cash flow statement data.
    """
    def import_scf(self, statement_of_cash_flow: Dict[str, np.ndarray]):
        self.statement_of_cash_flow = self.statement_of_cash_flow | statement_of_cash_flow
    
    """
    Retrieve the income statement as a DataFrame.

    Returns: pd.DataFrame: The income statement.
    """
    def get_income_statement(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.income_statement, orient='columns')
    
    """
    Retrieve the balance sheet as a DataFrame.

    Returns: pd.DataFrame: The income balance sheet.
    """
    def get_balance_sheet(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.balance_sheet, orient='columns')
    
    """
    Retrieve the statement of cash flows as a DataFrame.

    Returns: pd.DataFrame: The statement of cash flows.
    """
    def get_statement_of_cash_flows(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.statement_of_cash_flow, orient='columns')

    def validate_statements(*statements):
        lengths = []
        for statement in statements:
            lengths.extend(map(len, statement.values()))
        if len(set(lengths)) != 1:
            raise ValueError("Statements lengths must be the same")

    def __str__(self):
        return f"Enterprise(name= {self.name}, ticker= {self.ticker}, value= {self.value},shares_outstanding= {self.shares_outstanding})"