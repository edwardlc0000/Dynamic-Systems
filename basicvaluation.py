# basicvaluation.py
# Created On: 2025-03-22
# Created By: Edward Cromwell
# An exploration of basic valuations using numerical methods

import numpy as np
from typing import Dict

class Enterprise:
    def __init__(self, name: str, ticker: str, shares_outstanding: int):
        self.name: str = name
        self.ticker: str = ticker
        self.shares_outstanding: int = shares_outstanding

        self.income_statement: Dict[str, np.ndarray] = {
            'period': np.array([]),
            'revenue': np.array([]),
            'cost_of_sales': np.array([]),
            'op_ex': np.array([]),
            'd_and_a': np.array([]),
            'interest': np.array([]),
            'tax': np.array([])
        }

        self.balance_sheet: Dict[str, np.ndarray] = {
            'period': np.array([]),
            'cash': np.array([]),
            'curr_assets': np.array([]),
            'npp_and_e': np.array([]),
            'curr_liabilities': np.array([]),
            'debt': np.array([])
        }

    def set_period(self, period: np.ndarray):
        self.income_statement['period'] = np.append(self.income_statement['period'], period)
        self.balance_sheet['period'] = np.append(self.balance_sheet['period'], period)

    def set_revenue(self, revenue: np.ndarray):
        self.income_statement['revenue'] = np.append(self.income_statement['revenue'], revenue)

    def set_cost_of_sales(self, cost_of_sales: np.ndarray):
        self.income_statement['cost_of_sales'] = np.append(self.income_statement['cost_of_sales'], cost_of_sales)

    def set_op_ex(self, op_ex: np.ndarray):
        self.income_statement['op_ex'] = np.append(self.income_statement['op_ex'], op_ex)

    def set_d_and_a(self, d_and_a: np.ndarray):
        self.income_statement['d_and_a'] = np.append(self.income_statement['d_and_a'], d_and_a)

    def set_interest(self, interest: np.ndarray):
        self.income_statement['interest'] = np.append(self.income_statement['interest'], interest)

    def set_tax(self, tax: np.ndarray):
        self.income_statement['tax'] = np.append(self.income_statement['tax'], tax)

    def set_cash(self, cash: np.ndarray):
        self.balance_sheet['cash'] = np.append(self.balance_sheet['cash'], cash)

    def set_curr_assets(self, curr_assets: np.ndarray):
        self.balance_sheet['curr_assets'] = np.append(self.balance_sheet['curr_assets'], curr_assets)

    def set_curr_liabilities(self, curr_liabilities: np.ndarray):
        self.balance_sheet['curr_liabilities'] = np.append(self.balance_sheet['curr_liabilities'], curr_liabilities)

    def set_npp_and_e(self, npp_and_e: np.ndarray):
        self.balance_sheet['npp_and_e'] = np.append(self.balance_sheet['npp_and_e'], npp_and_e)

    def set_debt(self, debt: np.ndarray):
        self.balance_sheet['debt'] = np.append(self.balance_sheet['debt'], debt)

    def calc_gross_profit(self):
        self.income_statement['gross_profit'] = (self.income_statement['revenue'] 
                                                 - self.income_statement['cost_of_sales'])
        
    def calc_EBITDA(self):
        self.income_statement['EBITDA'] = (self.income_statement['gross_profit']
                                           -self.income_statement['op_ex'])
        
    def calc_EBIT(self):
        self.income_statement['EBIT'] = (self.income_statement['EBITDA']
                                         -self.income_statement['d_and_a'])
        
    def calc_net_income(self):
        self.income_statement['net_income'] = (self.income_statement['EBIT']
                                               -self.income_statement['interest']
                                               -self.income_statement['tax'])
        
    def calc_net_working_capital(self):
        self.balance_sheet['net_working_capital'] = (self.balance_sheet['curr_assets']
                                                     -self.balance_sheet['curr_liabilities'])

    def __str__(self):
        return f"Enterprise(name={self.name}, ticker={self.ticker}, shares_outstanding={self.shares_outstanding})"