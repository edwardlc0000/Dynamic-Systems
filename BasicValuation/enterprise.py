# basicvaluation.py
# Created On: 2025-03-22
# Created By: Edward Cromwell
# An exploration of basic valuations using numerical methods

import numpy as np
import pandas as pd
from typing import Dict
from typing import Final

stat_tax_rate: Final[float] = 0.21

class Enterprise:
    def __init__(self, name: str, ticker: str, shares_outstanding: int, pointer: int = 0):
        self.name: str = name
        self.ticker: str = ticker
        self.shares_outstanding: int = shares_outstanding
        self.pointer: int = pointer

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

    def import_is(self, income_statement: Dict[str, np.ndarray]):
        self.income_statement = self.income_statement | income_statement

    def import_bs(self, balance_sheet: Dict[str, np.ndarray]):
        self.balance_sheet = self.balance_sheet | balance_sheet

    def import_scf(self, statement_of_cash_flow: Dict[str, np.ndarray]):
        self.statement_of_cash_flow = self.statement_of_cash_flow | statement_of_cash_flow

    def calc_gross_profit(self):
        self.income_statement['Gross Profit'] = (self.income_statement['Revenue'] 
                                                 - self.income_statement['Cost of Sales'])
        
    def calc_EBITDA(self):
        self.income_statement['EBITDA'] = (self.income_statement['Gross Profit']
                                           -self.income_statement['Op. Ex.'])
        
    def calc_EBIT(self):
        self.income_statement['EBIT'] = (self.income_statement['EBITDA']
                                         -self.income_statement['D&A'])
        
    def calc_net_income(self):
        self.income_statement['Net Income'] = (self.income_statement['EBIT']
                                               -self.income_statement['Interest']
                                               -self.income_statement['Tax'])
        
    def calc_net_working_capital(self):
        self.balance_sheet['Net Working Capital'] = (self.balance_sheet['Current Assets']
                                                     -self.balance_sheet['Current Liabilities'])

    def get_income_statement(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.income_statement, orient='columns')
    
    def get_balance_sheet(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.balance_sheet, orient='columns')
    
    def get_statement_of_cash_flows(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.statement_of_cash_flow, orient='columns')

    def __str__(self):
        return f"Enterprise(name={self.name}, ticker={self.ticker}, shares_outstanding={self.shares_outstanding})"