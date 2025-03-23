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
            'revenue': np.array([]),
            'cost_of_sales': np.array([]),
            'gross_profit': np.array([]),
            'op_ex': np.array([]),
            'EBITDA': np.array([]),
            'd_and_a': np.array([]),
            'EBIT': np.array([]),
            'interest': np.array([]),
            'tax': np.array([]),
            'net_income': np.array([])
        }

        self.balance_sheet: Dict[str, np.ndarray] = {
            'cash': np.array([]),
            'curr_assets': np.array([]),
            'npp_and_e': np.array([]),
            'curr_liabilities': np.array([]),
            'debt': np.array([]),
            'net_working_capital': np.array([])
        }

        self.statement_of_cash_flow: Dict[str, np.ndarray] = {
            'net_cap_ex': np.array([])
        }

    def init_period(self, period: np.ndarray):
        self.income_statement['period'] = np.append(self.income_statement['period'], period)
        self.balance_sheet['period'] = np.append(self.balance_sheet['period'], period)

    def init_revenue(self, revenue: np.ndarray):
        self.income_statement['revenue'] = np.append(self.income_statement['revenue'], revenue)

    def init_cost_of_sales(self, cost_of_sales: np.ndarray):
        self.income_statement['cost_of_sales'] = np.append(self.income_statement['cost_of_sales'], cost_of_sales)

    def init_op_ex(self, op_ex: np.ndarray):
        self.income_statement['op_ex'] = np.append(self.income_statement['op_ex'], op_ex)

    def init_d_and_a(self, d_and_a: np.ndarray):
        self.income_statement['d_and_a'] = np.append(self.income_statement['d_and_a'], d_and_a)

    def init_interest(self, interest: np.ndarray):
        self.income_statement['interest'] = np.append(self.income_statement['interest'], interest)

    def init_tax(self, tax: np.ndarray):
        self.income_statement['tax'] = np.append(self.income_statement['tax'], tax)

    def init_cash(self, cash: np.ndarray):
        self.balance_sheet['cash'] = np.append(self.balance_sheet['cash'], cash)

    def init_curr_assets(self, curr_assets: np.ndarray):
        self.balance_sheet['curr_assets'] = np.append(self.balance_sheet['curr_assets'], curr_assets)

    def init_curr_liabilities(self, curr_liabilities: np.ndarray):
        self.balance_sheet['curr_liabilities'] = np.append(self.balance_sheet['curr_liabilities'], curr_liabilities)

    def init_npp_and_e(self, npp_and_e: np.ndarray):
        self.balance_sheet['npp_and_e'] = np.append(self.balance_sheet['npp_and_e'], npp_and_e)

    def init_debt(self, debt: np.ndarray):
        self.balance_sheet['debt'] = np.append(self.balance_sheet['debt'], debt)

    def init_net_cap_ex(self, net_cap_ex: np.ndarray):
        self.statement_of_cash_flow['net_cap_ex'] = np.append(self.statement_of_cash_flow['net_cap_ex'], net_cap_ex)

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
        
    def project_revenue(self, rev_growth: np.ndarray):
        for growth in rev_growth:
            self.income_statement['revenue'] = np.append(
                self.income_statement['revenue'],
                self.income_statement['revenue'][-1] * (1 + growth)
            )

    def project_cost_of_sales(self, gross_margin: np.ndarray):
        for i, margin in enumerate(gross_margin):
            self.income_statement['cost_of_sales'] = np.append(
                self.income_statement['cost_of_sales'],
                self.income_statement['revenue'][-len(gross_margin) + i] * (1 - margin)
            )

    def project_operating_expenses(self, opex_sales: np.ndarray):
        for i, opex in enumerate(opex_sales):
            self.income_statement['op_ex'] = np.append(
                self.income_statement['op_ex'],
                self.income_statement['revenue'][-len(opex_sales) + i] * opex
            )

    def project_fixed_assets(self, d_and_a_prior_npp_and_e: np.ndarray, net_cap_ex_sales: np.ndarray):
        for i in range(len(d_and_a_prior_npp_and_e)):
            next_d_and_a = self.balance_sheet['npp_and_e'][i] * d_and_a_prior_npp_and_e[i]
            self.income_statement['d_and_a'] = np.append(self.income_statement['d_and_a'], next_d_and_a)

            next_net_cap_ex = self.income_statement['revenue'][-len(d_and_a_prior_npp_and_e) + i] * net_cap_ex_sales[i]
            self.statement_of_cash_flow['net_cap_ex'] = np.append(self.statement_of_cash_flow['net_cap_ex'], next_net_cap_ex)

            next_npp_and_e = self.balance_sheet['npp_and_e'][-1] - next_d_and_a + next_net_cap_ex
            self.balance_sheet['npp_and_e'] = np.append(self.balance_sheet['npp_and_e'], next_npp_and_e)

    def project_net_working_capital(self, net_working_capital_sales: np.ndarray):
        for i, nwc_sales in enumerate(net_working_capital_sales):
            self.balance_sheet['net_working_capital'] = np.append(
                self.balance_sheet['net_working_capital'],
                self.income_statement['revenue'][-len(net_working_capital_sales) + i] * net_working_capital_sales[i]
            )

    def project_statements(self, rev_growth: np.ndarray, gross_margin: np.ndarray,
                           opex_sales: np.ndarray, d_and_a_prior_npp_and_e: np.ndarray,
                           net_cap_ex_sales: np.ndarray, net_working_capital_sales: np.ndarray):
        self.project_revenue(rev_growth)
        self.project_cost_of_sales(gross_margin)
        self.calc_gross_profit()
        self.project_operating_expenses(opex_sales)
        self.calc_EBITDA()
        self.project_fixed_assets(d_and_a_prior_npp_and_e, net_cap_ex_sales)
        self.calc_EBIT()
        self.project_net_working_capital(net_working_capital_sales)

    def get_income_statement(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.income_statement, orient='columns')
    
    def get_balance_sheet(self) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.balance_sheet, orient='columns')

    def __str__(self):
        return f"Enterprise(name={self.name}, ticker={self.ticker}, shares_outstanding={self.shares_outstanding})"