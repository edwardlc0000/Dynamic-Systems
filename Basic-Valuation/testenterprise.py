import unittest
import numpy as np
from enterprise import Enterprise

class TestEnterprise(unittest.TestCase):
    def setUp(self):
        # Create an Enterprise instance for testing
        self.enterprise = Enterprise(name="Test Corp", ticker="TST", shares_outstanding=1000)

    def tearDown(self):
        # Clean up after each test
        del self.enterprise

    def test_constructor(self):
        # Test that the constructor initializes the object correctly
        self.assertEqual(self.enterprise.name, "Test Corp")
        self.assertEqual(self.enterprise.ticker, "TST")
        self.assertEqual(self.enterprise.shares_outstanding, 1000)
        self.assertTrue(isinstance(self.enterprise.income_statement, dict))
        self.assertTrue(isinstance(self.enterprise.balance_sheet, dict))

    def test_init_methods(self):
        # Test initialization methods for income statement
        self.enterprise.init_revenue(np.array([1000.0]))
        self.enterprise.init_cost_of_sales(np.array([400.0]))
        self.enterprise.init_op_ex(np.array([200.0]))
        self.enterprise.init_d_and_a(np.array([50.0]))
        self.enterprise.init_interest(np.array([30.0]))
        self.enterprise.init_tax(np.array([100.0]))

        # Test initialization methods for balance sheet
        self.enterprise.init_cash(np.array([500.0]))
        self.enterprise.init_curr_assets(np.array([600.0]))
        self.enterprise.init_curr_liabilities(np.array([300.0]))
        self.enterprise.init_npp_and_e(np.array([1000.0]))
        self.enterprise.init_debt(np.array([400.0]))

        # Assertions for income statement
        np.testing.assert_array_equal(self.enterprise.income_statement['revenue'], np.array([1000.0]))
        np.testing.assert_array_equal(self.enterprise.income_statement['cost_of_sales'], np.array([400.0]))
        np.testing.assert_array_equal(self.enterprise.income_statement['op_ex'], np.array([200.0]))
        np.testing.assert_array_equal(self.enterprise.income_statement['d_and_a'], np.array([50.0]))
        np.testing.assert_array_equal(self.enterprise.income_statement['interest'], np.array([30.0]))
        np.testing.assert_array_equal(self.enterprise.income_statement['tax'], np.array([100.0]))

        # Assertions for balance sheet
        np.testing.assert_array_equal(self.enterprise.balance_sheet['cash'], np.array([500.0]))
        np.testing.assert_array_equal(self.enterprise.balance_sheet['curr_assets'], np.array([600.0]))
        np.testing.assert_array_equal(self.enterprise.balance_sheet['curr_liabilities'], np.array([300.0]))
        np.testing.assert_array_equal(self.enterprise.balance_sheet['npp_and_e'], np.array([1000.0]))
        np.testing.assert_array_equal(self.enterprise.balance_sheet['debt'], np.array([400.0]))

    def test_calc_methods(self):
        # Initialize data
        self.enterprise.init_revenue(np.array([1000.0]))
        self.enterprise.init_cost_of_sales(np.array([400.0]))
        self.enterprise.init_op_ex(np.array([200.0]))
        self.enterprise.init_d_and_a(np.array([50.0]))
        self.enterprise.init_interest(np.array([30.0]))
        self.enterprise.init_tax(np.array([100.0]))

        # Test calc_gross_profit
        self.enterprise.calc_gross_profit()
        np.testing.assert_array_equal(self.enterprise.income_statement['gross_profit'], np.array([600.0]))

        # Test calc_EBITDA
        self.enterprise.calc_EBITDA()
        np.testing.assert_array_equal(self.enterprise.income_statement['EBITDA'], np.array([400.0]))

        # Test calc_EBIT
        self.enterprise.calc_EBIT()
        np.testing.assert_array_equal(self.enterprise.income_statement['EBIT'], np.array([350.0]))

        # Test calc_net_income
        self.enterprise.calc_net_income()
        np.testing.assert_array_equal(self.enterprise.income_statement['net_income'], np.array([220.0]))

    def test_calc_net_working_capital(self):
        # Initialize data
        self.enterprise.init_curr_assets(np.array([600.0]))
        self.enterprise.init_curr_liabilities(np.array([300.0]))

        # Test calc_net_working_capital
        self.enterprise.calc_net_working_capital()
        np.testing.assert_array_equal(self.enterprise.balance_sheet['net_working_capital'], np.array([300.0]))

    def test_project_revenue(self):
        # Initialize revenue
        self.enterprise.init_revenue(np.array([1000.0]))

        # Project revenue
        rev_growth = np.array([0.1, 0.2, 0.15])  # 10%, 20%, 15% growth
        self.enterprise.project_revenue(rev_growth)

        # Expected revenue
        expected_revenue = np.array([1000.0, 1100.0, 1320.0, 1518.0])
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['revenue'], expected_revenue)

    def test_project_cost_of_sales(self):
        # Initialize revenue
        self.enterprise.init_revenue(np.array([1000.0, 1100.0, 1320.0, 1518.0]))

        # Project cost of sales
        gross_margin = np.array([0.4, 0.4, 0.35, 0.3])  # 40%, 35%, 30% gross margin
        self.enterprise.project_cost_of_sales(gross_margin)

        # Expected cost of sales
        expected_cost_of_sales = np.array([600.0, 660.0, 858.0, 1062.6])
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['cost_of_sales'], expected_cost_of_sales)

    def test_project_operating_expenses(self):
        # Initialize revenue
        self.enterprise.init_revenue(np.array([1000.0, 1100.0, 1320.0, 1518.0]))

        # Project operating expenses
        opex_sales = np.array([0.2, 0.2, 0.25, 0.22])  # 20%, 25%, 22% of revenue
        self.enterprise.project_operating_expenses(opex_sales)

        # Expected operating expenses
        expected_op_ex = np.array([200.0, 220.0, 330.0, 333.96])
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['op_ex'], expected_op_ex)

    def test_project_statements(self):
        # Initialize revenue
        self.enterprise.init_revenue(np.array([1000.0]))

        # Project income statement
        rev_growth = np.array([0.1, 0.2, 0.15])  # 10%, 20%, 15% growth
        gross_margin = np.array([0.4, 0.4, 0.35, 0.3])  # 40%, 35%, 30% gross margin
        opex_sales = np.array([0.2, 0.2, 0.25, 0.22])  # 20%, 25%, 22% of revenue
        self.enterprise.project_statements(rev_growth, gross_margin, opex_sales)

        # Expected values
        expected_revenue = np.array([1000.0, 1100.0, 1320.0, 1518.0])
        expected_cost_of_sales = np.array([600.0, 660.0, 858.0, 1062.6])
        expected_gross_profit = np.array([400.0, 440.0, 462.0, 455.4])
        expected_op_ex = np.array([200.0, 220.0, 330.0, 333.96])
        expected_EBITDA = np.array([200.0, 220.0, 132.0, 121.44])

        # Assertions
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['revenue'], expected_revenue)
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['cost_of_sales'], expected_cost_of_sales)
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['gross_profit'], expected_gross_profit)
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['op_ex'], expected_op_ex)
        np.testing.assert_array_almost_equal(self.enterprise.income_statement['EBITDA'], expected_EBITDA)

if __name__ == "__main__":
    unittest.main()