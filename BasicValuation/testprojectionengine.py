import unittest
import numpy as np
from enterprise import Enterprise
from projectionengine import ProjectionEngine

class TestProjectionEngine(unittest.TestCase):
    def setUp(self):
        # Create an Enterprise instance for testing
        self.enterprise = Enterprise(name="Test Corp", ticker="TST", shares_outstanding=1000, debt_value=0)

        # Import initial data into the Enterprise instance
        self.enterprise.import_is({
            'Revenue': np.array([1000.0]),
            'Cost of Sales': np.array([600.0]),
            'Op. Ex.': np.array([200.0]),
            'D&A': np.array([50.0]),
            'Interest': np.array([30.0]),
            'Tax': np.array([100.0])
        })
        self.enterprise.import_bs({
            'Net PP&E': np.array([1000.0]),
            'Net Working Capital': np.array([150.0])
        })
        self.enterprise.import_scf({
            'D&A': np.array([50.0]),
            'Net Cap. Ex.': np.array([0.0]),
            'Cap. Ex.': np.array([50.0])
        })

        # Create a ProjectionEngine instance
        self.projection_engine = ProjectionEngine(self.enterprise)

    def test_project_revenue(self):
        # Define revenue growth rates
        rev_growth = np.array([0.1, 0.2, 0.15])  # 10%, 20%, 15% growth

        # Project revenue
        self.projection_engine.project_revenue(rev_growth)

        # Expected revenue
        expected_revenue = np.array([1000.0, 1100.0, 1320.0, 1518.0])
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['Revenue'], expected_revenue)

    def test_project_cost_of_sales(self):
        # Define gross margins
        gross_margin = np.array([0.4, 0.35, 0.3])  # 40%, 35%, 30% gross margin

        # Initialize revenue
        self.enterprise.import_is({'Revenue': np.array([1000.0, 1100.0, 1320.0, 1518.0])})

        # Project cost of sales
        self.projection_engine.project_cost_of_sales(gross_margin)

        # Expected cost of sales
        expected_cost_of_sales = np.array([600.0, 660.0, 858.0, 1062.6])
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['Cost of Sales'], expected_cost_of_sales)

    def test_project_operating_expenses(self):
        # Define operating expenses as a percentage of revenue
        opex_sales = np.array([0.2, 0.25, 0.22])  # 20%, 25%, 22% of revenue

        # Initialize revenue
        self.enterprise.import_is({'Revenue': np.array([1100.0, 1320.0, 1518.0])})

        # Project operating expenses
        self.projection_engine.project_operating_expenses(opex_sales)

        # Expected operating expenses
        expected_op_ex = np.array([200.0, 220.0, 330.0, 333.96])
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['Op. Ex.'], expected_op_ex)

    def test_project_fixed_assets(self):
        # Define D&A and Net CapEx as percentages
        d_and_a_prior_npp_and_e = np.array([0.05, 0.05, 0.05])  # 5% of prior NPP&E
        net_cap_ex_sales = np.array([0.1, 0.1, 0.1])  # 10% of revenue

        # Initialize revenue
        self.enterprise.import_is({'Revenue': np.array([1000.0, 1100.0, 1320.0, 1518.0])})

        # Project fixed assets
        self.projection_engine.project_fixed_assets(d_and_a_prior_npp_and_e, net_cap_ex_sales)

        # Expected D&A
        expected_d_and_a = np.array([50.0, 50.0, 55.5, 62.1])  # 5% of prior NPP&E
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['D&A'], expected_d_and_a)

        # Expected Net PP&E
        expected_npp_and_e = np.array([1000.0, 1110.0, 1242.0, 1393.8])  # Updated NPP&E
        np.testing.assert_array_almost_equal(self.enterprise.balance_sheet['Net PP&E'], expected_npp_and_e)

    def test_project_net_working_capital(self):
        # Define Net Working Capital as a percentage of revenue
        net_working_capital_sales = np.array([0.15, 0.15, 0.15])  # 15% of revenue

        # Initialize revenue
        self.enterprise.import_is({'Revenue': np.array([1000.0, 1100.0, 1320.0, 1518.0])})

        # Project net working capital
        self.projection_engine.project_net_working_capital(net_working_capital_sales)

        # Expected Net Working Capital
        expected_nwc = np.array([150.0, 165.0, 198.0, 227.7])  # Revenue * 15%
        np.testing.assert_array_almost_equal(self.enterprise.balance_sheet['Net Working Capital'], expected_nwc)

    def test_project_statements(self):
        # Define projection inputs
        rev_growth = np.array([0.1, 0.2, 0.15])  # Revenue growth rates
        gross_margin = np.array([0.4, 0.35, 0.3])  # Gross margins
        opex_sales = np.array([0.2, 0.25, 0.22])  # Operating expenses as % of revenue
        d_and_a_prior_npp_and_e = np.array([0.05, 0.05, 0.05])  # D&A as % of prior NPP&E
        net_cap_ex_sales = np.array([0.1, 0.1, 0.1])  # Net CapEx as % of revenue
        net_working_capital_sales = np.array([0.15, 0.15, 0.15])  # NWC as % of revenue

        # Project all statements
        self.projection_engine.project_statements(
            rev_growth, gross_margin, opex_sales,
            d_and_a_prior_npp_and_e, net_cap_ex_sales, net_working_capital_sales
        )

        # Expected values
        expected_revenue = np.array([1000.0, 1100.0, 1320.0, 1518.0])
        expected_cost_of_sales = np.array([600.0, 660.0, 858.0, 1062.6])
        expected_gross_profit = np.array([400.0, 440.0, 462.0, 455.4])
        expected_op_ex = np.array([200.0, 220.0, 330.0, 333.96])
        expected_EBITDA = np.array([200.0, 220.0, 132.0, 121.44])

        # Assertions
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['Revenue'], expected_revenue)
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['Cost of Sales'], expected_cost_of_sales)
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['Gross Profit'], expected_gross_profit)
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['Op. Ex.'], expected_op_ex)
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['EBITDA'], expected_EBITDA)

    def test_project_fcf(self):
        # Initialize required data for the test
        self.enterprise.import_is({
            'EBITDA': np.array([200.0, 220.0, 132.0, 121.44]),
            'D&A': np.array([50.0, 55.0, 60.0, 65.0]),
            'EBIT': np.array([150.0, 165.0, 72.0, 56.44])
        })
        self.enterprise.import_bs({
            'Net Working Capital': np.array([150.0, 165.0, 198.0, 227.7])
        })
        self.enterprise.import_scf({
            'Cap. Ex.': np.array([100.0, 110.0, 120.0, 130.0])
        })

        # Project free cash flow
        self.projection_engine.project_fcf()

        # Expected values
        expected_tax = np.array([31.5, 34.65, 15.12, 11.8524])  # EBIT * stat_tax_rate (0.21)
        expected_nopat = np.array([118.5, 130.35, 56.88, 44.5876])  # EBIT - Tax
        expected_change_in_nwc = np.array([0.0, 15.0, 33.0, 29.7])  # Change in Net Working Capital
        expected_fcf = np.array([68.5, 60.35, -36.12, -50.1124])  # NOPAT + D&A - Change in NWC - Cap. Ex.

        # Assertions
        np.testing.assert_array_almost_equal(self.enterprise.discounted_cash_flow['Tax'], expected_tax)
        np.testing.assert_array_almost_equal(self.enterprise.discounted_cash_flow['NOPAT'], expected_nopat)
        np.testing.assert_array_almost_equal(self.enterprise.discounted_cash_flow['Change in NWC'], expected_change_in_nwc)
        np.testing.assert_array_almost_equal(self.enterprise.discounted_cash_flow['Free Cash Flow'], expected_fcf)

if __name__ == "__main__":
    unittest.main()


