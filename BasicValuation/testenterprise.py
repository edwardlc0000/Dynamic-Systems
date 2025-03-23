import unittest
import numpy as np
import pandas as pd

from enterprise import Enterprise

class TestEnterprise(unittest.TestCase):
    def setUp(self):
        # Create an Enterprise instance for testing
        self.enterprise = Enterprise(name="Test Corp", ticker="TST", shares_outstanding=1000)

        # Sample data for income statement
        self.income_statement = {
            'Revenue': np.array([1000.0]),
            'Cost of Sales': np.array([600.0]),
            'Gross Profit': np.array([400.0]),
            'Op. Ex.': np.array([200.0]),
            'EBITDA': np.array([200.0]),
            'D&A': np.array([50.0]),
            'EBIT': np.array([150.0]),
            'Interest': np.array([30.0]),
            'Tax': np.array([100.0]),
            'Net Income': np.array([20.0])
        }

        # Sample data for balance sheet
        self.balance_sheet = {
            'Cash': np.array([500.0]),
            'Current Assets': np.array([300.0]),
            'Net PP&E': np.array([1000.0]),
            'Current Liabilities': np.array([150.0]),
            'Long-Term Debt': np.array([400.0]),
            'Net Working Capital': np.array([150.0])
        }

        # Sample data for statement of cash flow
        self.statement_of_cash_flow = {
            'D&A': np.array([50.0]),
            'Net Cap. Ex.': np.array([100.0]),
            'Cap. Ex.': np.array([150.0])
        }

    def tearDown(self):
        # Clean up after each test
        del self.enterprise

    def test_import_is(self):
        # Import income statement data
        self.enterprise.import_is(self.income_statement)

        # Assert that the data was imported correctly
        for key, value in self.income_statement.items():
            np.testing.assert_array_equal(self.enterprise.income_statement[key], value)

    def test_import_bs(self):
        # Import balance sheet data
        self.enterprise.import_bs(self.balance_sheet)

        # Assert that the data was imported correctly
        for key, value in self.balance_sheet.items():
            np.testing.assert_array_equal(self.enterprise.balance_sheet[key], value)

    def test_import_scf(self):
        # Import statement of cash flow data
        self.enterprise.import_scf(self.statement_of_cash_flow)

        # Assert that the data was imported correctly
        for key, value in self.statement_of_cash_flow.items():
            np.testing.assert_array_equal(self.enterprise.statement_of_cash_flow[key], value)

    def test_get_income_statement(self):
        # Import income statement data and retrieve it as a DataFrame
        self.enterprise.import_is(self.income_statement)
        df = self.enterprise.get_income_statement()

        # Expected DataFrame
        expected_df = pd.DataFrame.from_dict(self.income_statement, orient='columns')
        pd.testing.assert_frame_equal(df, expected_df)

    def test_get_balance_sheet(self):
        # Import balance sheet data and retrieve it as a DataFrame
        self.enterprise.import_bs(self.balance_sheet)
        df = self.enterprise.get_balance_sheet()

        # Expected DataFrame
        expected_df = pd.DataFrame.from_dict(self.balance_sheet, orient='columns')
        pd.testing.assert_frame_equal(df, expected_df)

    def test_get_statement_of_cash_flows(self):
        # Import statement of cash flow data and retrieve it as a DataFrame
        self.enterprise.import_scf(self.statement_of_cash_flow)
        df = self.enterprise.get_statement_of_cash_flows()

        # Expected DataFrame
        expected_df = pd.DataFrame.from_dict(self.statement_of_cash_flow, orient='columns')
        pd.testing.assert_frame_equal(df, expected_df)

if __name__ == "__main__":
    unittest.main()