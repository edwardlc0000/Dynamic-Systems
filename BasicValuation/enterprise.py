# enterprise.py
# Created On: 2025-03-22
# Created By: Edward Cromwell
# A class for modeling the financial statements of enterprises

import numpy as np
import pandas as pd
from typing import Dict, List
from typing import Final


class Enterprise:

    """
    Initialize an Enterprise instance.

    Args:
        name (str): The name of the company.
        ticker (str): The stock ticker symbol of the company.
        shares_outstanding (int): The number of shares outstanding.
        pointer (int): A pointer to track the current period (default is 0).
    """
    def __init__(self, name: str, ticker: str, shares_outstanding: int, debt_value: float, stat_tax_rate: float = 0.21,pointer: int = 0):
        self.name: str = name
        self.ticker: str = ticker
        self.shares_outstanding: int = shares_outstanding
        self.stat_tax_rate: float = stat_tax_rate
        self.pointer: int = pointer
        self.enterprise_value: float = None
        self.equity_value: float = None
        self.debt_value: float = debt_value

        # Initialize the income statement with floating-point arrays
        self.income_statement: Dict[str, np.ndarray] = {
            'Revenue': np.array([], dtype=float),
            'Cost of Sales': np.array([], dtype=float),
            'Gross Profit': np.array([], dtype=float),
            'Op. Ex.': np.array([], dtype=float),
            'EBITDA': np.array([], dtype=float),
            'D&A': np.array([], dtype=float),
            'EBIT': np.array([], dtype=float),
            'Interest': np.array([], dtype=float),
            'Tax': np.array([], dtype=float),
            'Net Income': np.array([], dtype=float)
        }

        # Initialize the balance sheet with floating-point arrays
        self.balance_sheet: Dict[str, np.ndarray] = {
            'Cash': np.array([], dtype=float),
            'Current Assets': np.array([], dtype=float),
            'Net PP&E': np.array([], dtype=float),
            'Current Liabilities': np.array([], dtype=float),
            'Long-Term Debt': np.array([], dtype=float),
            'Net Working Capital': np.array([], dtype=float)
        }

        # Initialize the statement of cash flows with floating-point arrays
        self.statement_of_cash_flow: Dict[str, np.ndarray] = {
            'D&A': np.array([], dtype=float),
            'Net Cap. Ex.': np.array([], dtype=float),
            'Cap. Ex.': np.array([], dtype=float),
        }

        # Initializes the discounted cash flow analysis with floating-point arrays
        self.discounted_cash_flow: Dict[str, np.ndarray] = {
            'EBITDA': np.array([], dtype=float),
            'D&A': np.array([], dtype=float),
            'EBIT': np.array([], dtype=float),
            'Tax': np.array([], dtype=float),
            'NOPAT': np.array([], dtype=float),
            'Change in NWC': np.array([], dtype=float),
            'Cap. Ex.': np.array([], dtype=float),
            'Free Cash Flow': np.array([], dtype=float),
            'PV Free Cash Flow': np.array([], dtype=float)
        }

    """
    Import the financial statement data into the Enterprise instance

    Args: statements (Dict[str, np.ndarray]): Dictionaries containing financial statement data.
    """
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
    Import data into the financial statements.

    Args: income_statement (Dict[str, np.ndarray]): A dictionary containing financial statement data.
    """
    def import_is(self, income_statement: Dict[str, np.ndarray]):
        self.income_statement = self.income_statement | income_statement

    def import_bs(self, balance_sheet: Dict[str, np.ndarray]):
        self.balance_sheet = self.balance_sheet | balance_sheet

    def import_scf(self, statement_of_cash_flow: Dict[str, np.ndarray]):
        self.statement_of_cash_flow = self.statement_of_cash_flow | statement_of_cash_flow
    
    """
    Retrieve the  financial statements as a DataFrame.

    Returns: pd.DataFrame: The financial statement.
    """
    def get_income_statement(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.income_statement, orient='columns')

    def get_balance_sheet(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.balance_sheet, orient='columns')
    
    def get_statement_of_cash_flows(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.statement_of_cash_flow, orient='columns')

    def get_discounted_cash_flow(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.discounted_cash_flow, orient='columns')

    '''
    Ensures that the financial statements passed as an input are of the same length.

    Args: statements (Dict[str, np.ndarray]): Dictionaries containing financial statement data.
    '''
    def validate_statements(self, *statements: Dict[str, np.ndarray]):
        lengths: List[int] = []
        for statement in statements:
            lengths.extend(map(len, statement.values()))
        if len(set(lengths)) != 1:
            raise ValueError("Statements lengths must be the same")

    def __str__(self):
        return f"Enterprise(name= {self.name}, ticker= {self.ticker}, enterprise_value= {self.enterprise_value}, equity_value= {self.equity_value}, shares_outstanding= {self.shares_outstanding})"