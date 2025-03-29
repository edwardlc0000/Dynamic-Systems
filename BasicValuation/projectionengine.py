# enterprise.py
# Created On: 2025-03-23
# Created By: Edward Cromwell
# A class for projecting and analyzing the financial statements of enterprises

import numpy as np
from scipy.optimize import root_scalar

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
        for i in range(0, len(d_and_a_prior_npp_and_e)):
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
        
    def dcf_model(self, unlevered_cost_equity: float, cost_of_debt: float,
                  begin_lev: float, growth_rate: float):
        
        if self.enterprise.discounted_cash_flow['Free Cash Flow'] < 0.0:
            self.enterprise.enterprise_value = -self.enterprise.debt_value
            self.enterprise.equity_value = 0
            return
        
        if begin_lev >= 1.0: 
            raise ValueError("Leverage must be less than 100%.")
        
        result = root_scalar(lambda begin_lev: self.lev_difference(begin_lev, unlevered_cost_equity, cost_of_debt, growth_rate), 
                             bracket=[0.0000, 0.9999], method='brentq')
        
        final_leverage: float = result.root

        final_cost_of_equity: float = (unlevered_cost_equity
                                + ((final_leverage / (1 - final_leverage))
                                * (unlevered_cost_equity - cost_of_debt)))
        final_wacc: float = (final_leverage * (1 - self.enterprise.stat_tax_rate) * cost_of_debt
                    + (1 - final_leverage) * final_cost_of_equity)
        
        enterprise_value: float = self.calculate_enterprise_value(final_wacc, growth_rate)
        self.enterprise.enterprise_value = enterprise_value

        equity_value: float = enterprise_value - self.enterprise.debt_value
        self.enterprise.equity_value = equity_value

        fcf: np.ndarray = self.enterprise.discounted_cash_flow['Free Cash Flow'][self.enterprise.pointer + 1:]
        discount_factors: np.ndarray = 1/((1 + final_wacc) ** np.arange(1, len(fcf) + 1))
        pv_fcf: np.ndarray = fcf * discount_factors
        self.enterprise.discounted_cash_flow['PV Free Cash Flow'] = np.zeros(self.enterprise.pointer + 1)
        self.enterprise.discounted_cash_flow['PV Free Cash Flow'] = np.append(
            self.enterprise.discounted_cash_flow['PV Free Cash Flow'],
            pv_fcf
        )

    def calculate_enterprise_value(self, wacc: float, growth_rate: float):
        if wacc <= growth_rate:
            raise ValueError("WACC must be greater than the growth rate.")
        
        fcf: np.ndarray = self.enterprise.discounted_cash_flow['Free Cash Flow'][self.enterprise.pointer + 1:]
        discount_factors: np.ndarray = 1/((1 + wacc) ** np.arange(1, len(fcf) + 1))

        epsilon = np.finfo(float).eps  # Small value to prevent division by a value close to zero

        pv_fcf: float = np.sum(fcf * discount_factors)
        terminal_value: float = (fcf[-1]/(wacc - growth_rate + epsilon)) * discount_factors[-1]
        enterprise_value: float = pv_fcf + terminal_value

        return enterprise_value
    
    def lev_difference(self, begin_lev, unlevered_cost_equity, cost_of_debt, growth_rate):
        cost_of_equity: float = (unlevered_cost_equity
                                + ((begin_lev/(1 - begin_lev))
                                * (unlevered_cost_equity - cost_of_debt)))
        wacc: float = (begin_lev * (1 - self.enterprise.stat_tax_rate) * cost_of_debt
                + (1- begin_lev) * cost_of_equity)
        
        enterprise_value: float = self.calculate_enterprise_value(wacc, growth_rate)
        debt_value: float = self.enterprise.debt_value
        
        ending_lev: float = debt_value/enterprise_value

        return ending_lev - begin_lev