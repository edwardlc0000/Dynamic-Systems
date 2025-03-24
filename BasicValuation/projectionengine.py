# enterprise.py
# Created On: 2025-03-23
# Created By: Edward Cromwell
# A class for projecting and analyzing the financial statements of enterprises

import numpy as np

from enterprise import Enterprise

class ProjectionEngine:

    def __init__(self, enterprise: Enterprise):
        self.enterprise = enterprise

    def project_statements(self, rev_growth: np.ndarray,
                           gross_margin: np.ndarray,
                           opex_sales: np.ndarray,
                           d_and_a_prior_npp_and_e: np.ndarray,
                           net_cap_ex_sales: np.ndarray,
                           net_working_capital_sales: np.ndarray):
        self.project_revenue(rev_growth)
        self.project_cost_of_sales(gross_margin)
        self.project_gross_profit()
        self.project_operating_expenses(opex_sales)
        self.project_EBITDA()
        self.project_fixed_assets(d_and_a_prior_npp_and_e, net_cap_ex_sales)
        self.project_EBIT()
        self.project_net_working_capital(net_working_capital_sales)
    
    def project_revenue(self, rev_growth: np.ndarray):
        for growth in rev_growth:
            self.enterprise.income_statement['Revenue'] = np.append(
                self.enterprise.income_statement['Revenue'],
                self.enterprise.income_statement['Revenue'][-1] * (1 + growth)
            )

    def project_cost_of_sales(self, gross_margin: np.ndarray):
        for i, margin in enumerate(gross_margin):
            self.enterprise.income_statement['Cost of Sales'] = np.append(
                self.enterprise.income_statement['Cost of Sales'],
                self.enterprise.income_statement['Revenue'][-len(gross_margin) + i] * (1 - margin)
            )

    def project_gross_profit(self):
        self.enterprise.income_statement['Gross Profit'] = (self.enterprise.income_statement['Revenue'] 
                                                 - self.enterprise.income_statement['Cost of Sales'])
        

    def project_operating_expenses(self, opex_sales: np.ndarray):
        for i, opex in enumerate(opex_sales):
            self.enterprise.income_statement['Op. Ex.'] = np.append(
                self.enterprise.income_statement['Op. Ex.'],
                self.enterprise.income_statement['Revenue'][-len(opex_sales) + i] * opex
            )

    def project_EBITDA(self):
            self.enterprise.income_statement['EBITDA'] = (self.enterprise.income_statement['Gross Profit']
                                               -self.enterprise.income_statement['Op. Ex.'])

    def project_EBIT(self):
        self.enterprise.income_statement['EBIT'] = (self.enterprise.income_statement['EBITDA']
                                         -self.enterprise.income_statement['D&A'])

    def project_net_income(self):
        self.enterprise.income_statement['Net Income'] = (self.enterprise.income_statement['EBIT']
                                               -self.enterprise.income_statement['Interest']
                                               -self.enterprise.income_statement['Tax'])

    def project_fixed_assets(self, d_and_a_prior_npp_and_e: np.ndarray, net_cap_ex_sales: np.ndarray):
        for i in range(len(d_and_a_prior_npp_and_e)):
            next_d_and_a: float = self.enterprise.balance_sheet['Net PP&E'][self.enterprise.pointer + i] * d_and_a_prior_npp_and_e[i]
            self.enterprise.income_statement['D&A'] = np.append(
                self.enterprise.income_statement['D&A'],
                next_d_and_a
            )
            self.enterprise.statement_of_cash_flow['D&A'] = np.append(
                self.enterprise.statement_of_cash_flow['D&A'],
                next_d_and_a
            )

            next_net_cap_ex: float = self.enterprise.income_statement['Revenue'][-len(net_cap_ex_sales) + i] * net_cap_ex_sales[i]
            self.enterprise.statement_of_cash_flow['Net Cap. Ex.'] = np.append(
                self.enterprise.statement_of_cash_flow['Net Cap. Ex.'],
                next_net_cap_ex
            )

            next_cap_ex: float = next_d_and_a + next_net_cap_ex
            self.enterprise.statement_of_cash_flow['Cap. Ex.'] = np.append(
                self.enterprise.statement_of_cash_flow['Cap. Ex.'],
                next_cap_ex
            )

            next_npp_and_e: float = self.enterprise.balance_sheet['Net PP&E'][-1] + next_cap_ex - next_d_and_a
            self.enterprise.balance_sheet['Net PP&E'] = np.append(
                self.enterprise.balance_sheet['Net PP&E'],
                next_npp_and_e
            )

    def project_net_working_capital(self, net_working_capital_sales: np.ndarray):
        for i, nwc_sales in enumerate(net_working_capital_sales):
            self.enterprise.balance_sheet['Net Working Capital'] = np.append(
                self.enterprise.balance_sheet['Net Working Capital'],
                self.enterprise.income_statement['Revenue'][-len(net_working_capital_sales) + i] * nwc_sales
            )

    def project_fcf(self):
        self.enterprise.discounted_cash_flow['EBITDA'] = self.enterprise.income_statement['EBITDA']
        self.enterprise.discounted_cash_flow['D&A'] = self.enterprise.income_statement['D&A']
        self.enterprise.discounted_cash_flow['EBIT'] = self.enterprise.income_statement['EBIT']
        self.enterprise.discounted_cash_flow['Tax'] = np.multiply(self.enterprise.income_statement['EBIT'],
                                                                  self.enterprise.stat_tax_rate)
        self.enterprise.discounted_cash_flow['NOPAT'] = (self.enterprise.discounted_cash_flow['EBIT']
                                                         - self.enterprise.discounted_cash_flow['Tax'])
        
        self.enterprise.discounted_cash_flow['Change in NWC'] = np.append(
            self.enterprise.discounted_cash_flow['Change in NWC'],
            0.0
        )
        for i in range(0, len(self.enterprise.balance_sheet['Net Working Capital']) - 1):
            self.enterprise.discounted_cash_flow['Change in NWC'] = np.append(
                self.enterprise.discounted_cash_flow['Change in NWC'],
                self.enterprise.balance_sheet['Net Working Capital'][i + 1]
                - self.enterprise.balance_sheet['Net Working Capital'][i]
            )
        
        self.enterprise.discounted_cash_flow['Cap. Ex.'] = self.enterprise.statement_of_cash_flow['Cap. Ex.']

        self.enterprise.discounted_cash_flow['Free Cash Flow'] = (self.enterprise.discounted_cash_flow['NOPAT']
                                                       + self.enterprise.discounted_cash_flow['D&A']
                                                       - self.enterprise.discounted_cash_flow['Change in NWC']
                                                       - self.enterprise.discounted_cash_flow['Cap. Ex.']
                                                       )
