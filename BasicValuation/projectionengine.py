

import numpy as np

from enterprise import Enterprise

class ProjectionEngine:

    def __init__(self, enterprise: Enterprise):
        self.enterprise = enterprise

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

    def project_operating_expenses(self, opex_sales: np.ndarray):
        for i, opex in enumerate(opex_sales):
            self.enterprise.income_statement['Op. Ex.'] = np.append(
                self.enterprise.income_statement['Op. Ex.'],
                self.enterprise.income_statement['Revenue'][-len(opex_sales) + i] * opex
            )

    def project_fixed_assets(self, d_and_a_prior_npp_and_e: np.ndarray, net_cap_ex_sales: np.ndarray):
        for i in range(len(d_and_a_prior_npp_and_e)):
            next_d_and_a: float = self.enterprise.balance_sheet['Net PP&E'][i] * d_and_a_prior_npp_and_e[i]
            self.enterprise.income_statement['D&A'] = np.append(self.enterprise.income_statement['D&A'], next_d_and_a)
            self.enterprise.statement_of_cash_flow['D&A'] = np.append(self.enterprise.statement_of_cash_flow['D&A'], next_d_and_a)

            next_net_cap_ex: float = self.enterprise.income_statement['Revenue'][-len(d_and_a_prior_npp_and_e) + i] * net_cap_ex_sales[i]
            self.enterprise.statement_of_cash_flow['Net Cap. Ex.'] = np.append(self.enterprise.statement_of_cash_flow['Net Cap. Ex.'], next_net_cap_ex)

            next_cap_ex: float = next_d_and_a + next_net_cap_ex
            self.enterprise.statement_of_cash_flow['Cap. Ex.'] = np.append(self.enterprise.statement_of_cash_flow['Cap. Ex.'], next_cap_ex)

            next_npp_and_e: float = self.enterprise.balance_sheet['Net PP&E'][-1] + next_net_cap_ex
            self.enterprise.balance_sheet['Net PP&E'] = np.append(self.enterprise.balance_sheet['Net PP&E'], next_npp_and_e)

    def project_net_working_capital(self, net_working_capital_sales: np.ndarray):
        for i, nwc_sales in enumerate(net_working_capital_sales):
            self.enterprise.balance_sheet['Net Working Capital'] = np.append(
                self.enterprise.balance_sheet['Net Working Capital'],
                self.enterprise.income_statement['Revenue'][-len(net_working_capital_sales) + i] * nwc_sales
            )

    def project_statements(self, rev_growth: np.ndarray, gross_margin: np.ndarray,
                           opex_sales: np.ndarray, d_and_a_prior_npp_and_e: np.ndarray,
                           net_cap_ex_sales: np.ndarray, net_working_capital_sales: np.ndarray):
        self.project_revenue(rev_growth)
        self.project_cost_of_sales(gross_margin)
        self.enterprise.calc_gross_profit()
        self.project_operating_expenses(opex_sales)
        self.enterprise.calc_EBITDA()
        self.project_fixed_assets(d_and_a_prior_npp_and_e, net_cap_ex_sales)
        self.enterprise.calc_EBIT()
        self.project_net_working_capital(net_working_capital_sales)