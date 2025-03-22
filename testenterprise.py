import unittest
import numpy as np
from basicvaluation import Enterprise

class TestEnterprise(unittest.TestCase):
    def setUp(self):
        # Create an Enterprise instance for testing
        self.enterprise = Enterprise(name="Test Corp", ticker="TST", shares_outstanding=1000)

        # Set up initial data
        self.enterprise.set_revenue(np.array([1000.0]))
        self.enterprise.set_cost_of_sales(np.array([400.0]))
        self.enterprise.set_op_ex(np.array([200.0]))
        self.enterprise.set_d_and_a(np.array([50.0]))
        self.enterprise.set_interest(np.array([30.0]))
        self.enterprise.set_tax(np.array([100.0]))
        self.enterprise.set_curr_assets(np.array([500.0]))
        self.enterprise.set_curr_liabilities(np.array([300.0]))

    def test_calc_gross_profit(self):
        self.enterprise.calc_gross_profit()
        expected = np.array([600.0])  # revenue - cost_of_sales
        np.testing.assert_array_equal(self.enterprise.income_statement['gross_profit'], expected)

    def test_calc_EBITDA(self):
        self.enterprise.calc_gross_profit()
        self.enterprise.calc_EBITDA()
        expected = np.array([400.0])  # gross_profit - op_ex
        np.testing.assert_array_equal(self.enterprise.income_statement['EBITDA'], expected)

    def test_calc_EBIT(self):
        self.enterprise.calc_gross_profit()
        self.enterprise.calc_EBITDA()
        self.enterprise.calc_EBIT()
        expected = np.array([350.0])  # EBITDA - d_and_a
        np.testing.assert_array_equal(self.enterprise.income_statement['EBIT'], expected)

    def test_calc_net_income(self):
        self.enterprise.calc_gross_profit()
        self.enterprise.calc_EBITDA()
        self.enterprise.calc_EBIT()
        self.enterprise.calc_net_income()
        expected = np.array([220.0])  # EBIT - interest - tax
        np.testing.assert_array_equal(self.enterprise.income_statement['net_income'], expected)

    def test_calc_net_working_capital(self):
        self.enterprise.calc_net_working_capital()
        expected = np.array([200.0])  # curr_assets - curr_liabilities
        np.testing.assert_array_equal(self.enterprise.balance_sheet['net_working_capital'], expected)

    def test_set_methods(self):
        # Test setting additional values
        self.enterprise.set_revenue(np.array([2000.0]))
        self.enterprise.set_cost_of_sales(np.array([800.0]))
        self.enterprise.set_op_ex(np.array([300.0]))
        self.enterprise.set_curr_assets(np.array([600.0]))
        self.enterprise.set_curr_liabilities(np.array([400.0]))

        # Check updated values
        np.testing.assert_array_equal(self.enterprise.income_statement['revenue'], np.array([1000.0, 2000.0]))
        np.testing.assert_array_equal(self.enterprise.income_statement['cost_of_sales'], np.array([400.0, 800.0]))
        np.testing.assert_array_equal(self.enterprise.income_statement['op_ex'], np.array([200.0, 300.0]))
        np.testing.assert_array_equal(self.enterprise.balance_sheet['curr_assets'], np.array([500.0, 600.0]))
        np.testing.assert_array_equal(self.enterprise.balance_sheet['curr_liabilities'], np.array([300.0, 400.0]))

if __name__ == "__main__":
    unittest.main()