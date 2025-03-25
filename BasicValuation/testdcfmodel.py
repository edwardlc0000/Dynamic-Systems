import unittest
import numpy as np
from enterprise import Enterprise
from projectionengine import ProjectionEngine

class TestProjectionEngine(unittest.TestCase):
    def setUp(self):
        # Create an Enterprise instance for testing
        self.enterprise = Enterprise(name="Test Corp", ticker="TST", shares_outstanding=1000, debt_value=500.0)

        # Import initial data into the Enterprise instance
        self.enterprise.import_is({
            'EBITDA': np.array([300.0, 320.0, 350.0, 370.0]),  # Increased EBITDA
            'D&A': np.array([50.0, 55.0, 60.0, 65.0]),
            'EBIT': np.array([250.0, 265.0, 290.0, 305.0]),  # Adjusted EBIT
            'Tax': np.array([52.5, 55.65, 60.9, 64.05]),  # 21% tax rate on EBIT
            'Net Income': np.array([197.5, 209.35, 229.1, 240.95])  # Adjusted Net Income
        })
        self.enterprise.import_bs({
            'Net Working Capital': np.array([150.0, 155.0, 160.0, 165.0])  # Smaller changes in NWC
        })
        self.enterprise.import_scf({
            'Cap. Ex.': np.array([80.0, 85.0, 90.0, 95.0])  # Reduced CapEx
        })

        # Create a ProjectionEngine instance
        self.projection_engine = ProjectionEngine(self.enterprise)

        # Project Free Cash Flow
        self.projection_engine.project_fcf()

    def test_dcf_model(self):
        # Define inputs for the DCF model
        unlevered_cost_equity = 0.08  # 8%
        cost_of_debt = 0.05  # 5%
        begin_lev = 0.5  # Initial leverage
        growth_rate = 0.02  # 2% growth rate

        # Run the DCF model
        self.projection_engine.dcf_model(unlevered_cost_equity, cost_of_debt, begin_lev, growth_rate)

        # Expected results
        expected_leverage = 0.1513  # Beginning and ending leverage should converge
        expected_wacc = 0.065  # Weighted Average Cost of Capital
        expected_enterprise_value = 3_304.127  # Example enterprise value
        expected_equity_value = 2_804.127  # Enterprise value - debt value

        # Assertions
        self.assertAlmostEqual(self.enterprise.equity_value, expected_equity_value, places=2)
        self.assertAlmostEqual(self.enterprise.enterprise_value, expected_enterprise_value, places=2)
        self.assertAlmostEqual(self.enterprise.debt_value / expected_enterprise_value, expected_leverage, places=2)

    def test_dcf_model_invalid_wacc(self):
        # Define inputs with WACC <= growth rate
        unlevered_cost_equity = 0.04  # 4%
        cost_of_debt = 0.03  # 3%
        begin_lev = 0.5  # Initial leverage
        growth_rate = 0.05  # 5% growth rate (greater than WACC)

        # Expect a ValueError due to invalid WACC
        with self.assertRaises(ValueError):
            self.projection_engine.dcf_model(unlevered_cost_equity, cost_of_debt, begin_lev, growth_rate)

if __name__ == "__main__":
    unittest.main()