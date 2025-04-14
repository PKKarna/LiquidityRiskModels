import pandas as pd
import numpy as np
from datetime import datetime

class LiquidityReporter:
    def __init__(self, balance_sheet_path: str):
        self.df = pd.read_csv(balance_sheet_path, parse_dates=['date'])
        self.validate_data()
        
    def validate_data(self):
        """Check for missing values and negative balances."""
        assert not self.df.isnull().values.any(), "Missing values detected"
        assert (self.df.select_dtypes(include=[np.number]) >= 0).all().all(), "Negative balances invalid"

    def calculate_lcr(self) -> float:
        """Liquidity Coverage Ratio (Basel III)"""
        hqla = self.df['cash_treasuries'] + self.df['central_bank_reserves']
        net_outflows = self.df['deposit_outflows_30d'] + self.df['wholesale_funding_runoff']
        return (hqla.sum() / net_outflows.sum()) * 100

    def calculate_nsfr(self) -> float:
        """Net Stable Funding Ratio"""
        asf = (self.df['stable_deposits'] * 0.95 +
               self.df['tier1_capital'] * 1.0)
        rsf = (self.df['loans_1y'] * 0.85 +
               self.df['mortgages'] * 0.65)
        return (asf.sum() / rsf.sum()) * 100

    def generate_fr2052a_report(self) -> pd.DataFrame:
        """FR 2052a-style liquidity report"""
        return pd.pivot_table(
            self.df,
            values=['cash_flows', 'liabilities'],
            index=['date'],
            columns=['product_type'],
            aggfunc=np.sum
        )

if __name__ == "__main__":
    reporter = LiquidityReporter("data/jpm_10k_2023.csv")
    print(f"LCR: {reporter.calculate_lcr():.2f}%")
    print(f"NSFR: {reporter.calculate_nsfr():.2f}%")
    reporter.generate_fr2052a_report().to_csv("reports/fr2052a_output.csv")
