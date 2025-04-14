import plotly.express as px
from lcr_nsfr_calculator import LiquidityReporter

class StressTester:
    SCENARIOS = {
        "Baseline": {"deposit_runoff": 0.05, "haircut": 0.03},
        "Severe": {"deposit_runoff": 0.20, "haircut": 0.15}
    }

    def __init__(self, balance_sheet_path: str):
        self.reporter = LiquidityReporter(balance_sheet_path)

    def run_scenarios(self) -> pd.DataFrame:
        results = []
        for name, params in self.SCENARIOS.items():
            stressed_df = self.reporter.df.copy()
            stressed_df['deposits'] *= (1 - params['deposit_runoff'])
            stressed_df['hqla'] *= (1 - params['haircut'])
            lcr = (stressed_df['hqla'].sum() /
                   stressed_df['outflows'].sum()) * 100
            results.append({"Scenario": name, "LCR": lcr})
        return pd.DataFrame(results)

    def plot_gaps(self):
        df = self.run_scenarios()
        fig = px.bar(
            df, x="Scenario", y="LCR",
            title="LCR Under Stress Scenarios",
            labels={"LCR": "LCR (%)"},
            color="LCR",
            color_continuous_scale="RdYlGn"
        )
        fig.write_html("dashboards/stress_test.html")

StressTester("data/jpm_10k_2023.csv").plot_gaps()
