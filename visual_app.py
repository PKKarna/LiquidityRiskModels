


#!/usr/bin/env python3
"""
Interactive Liquidity Gap Dashboard for Regulatory Reporting
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.core.calculator import LiquidityCalculator
from datetime import datetime, timedelta

class LiquidityDashboard:
    def __init__(self, data_path: str = "data/sample_10k_2023.csv"):
        self.df = self._load_and_preprocess(data_path)
        self.calculator = LiquidityCalculator(self.df)
        
    def _load_and_preprocess(self, data_path: str) -> pd.DataFrame:
        """Load and prepare data with date handling"""
        df = pd.read_csv(data_path, parse_dates=['date'])
        df['quarter'] = df['date'].dt.to_period('Q')
        return df

    def create_gap_analysis(self) -> go.Figure:
        """Main dashboard with 3 interactive components"""
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"colspan": 2}, None]],
            subplot_titles=("Liquidity Position by Quarter",
                          "HQLA Composition",
                          "Cumulative Liquidity Gap"))

        # 1. LCR Trend Chart
        lcr_data = self.df.groupby('quarter').apply(
            lambda x: self.calculator.calculate_lcr(x)
        ).reset_index()
        
        fig.add_trace(
            go.Bar(
                x=lcr_data['quarter'].astype(str),
                y=lcr_data['value'],
                name="LCR",
                marker_color='#1f77b4',
                hovertemplate="Quarter: %{x}<br>LCR: %{y:.1f}%<extra></extra>"
            ),
            row=1, col=1
        )

        # 2. HQLA Composition Pie
        latest_hqla = self.calculator.calculate_lcr()['hqla_composition']
        fig.add_trace(
            go.Pie(
                labels=list(latest_hqla.keys()),
                values=list(latest_hqla.values()),
                name="HQLA",
                hole=0.4,
                marker_colors=px.colors.qualitative.Pastel
            ),
            row=1, col=2
        )

        # 3. Cumulative Gap Analysis
        maturity_buckets = [
            'O/N', '1-7D', '8-30D', '31-90D', '91-180D',
            '181-365D', '1-2Y', '2-5Y', '5Y+'
        ]
        gap_data = pd.DataFrame({
            'Bucket': maturity_buckets,
            'Assets': [100, 85, 70, 60, 50, 40, 30, 20, 10],
            'Liabilities': [90, 75, 65, 55, 45, 35, 25, 15, 5]
        })
        
        fig.add_trace(
            go.Scatter(
                x=gap_data['Bucket'],
                y=gap_data['Assets'].cumsum(),
                name="Cumulative Assets",
                line=dict(color='green', width=4),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=gap_data['Bucket'],
                y=gap_data['Liabilities'].cumsum(),
                name="Cumulative Liabilities",
                line=dict(color='red', width=4)),
            row=2, col=1
        )

        # Layout Configuration
        fig.update_layout(
            title_text="Liquidity Risk Dashboard",
            template="plotly_white",
            hovermode="x unified",
            height=800,
            annotations=[
                dict(text=f"Last Updated: {datetime.now().strftime('%Y-%m-%d')}",
                     x=0.5, y=-0.15, showarrow=False, xref="paper", yref="paper")
            ]
        )
        
        # Add regulatory thresholds
        fig.add_hline(y=100, line_dash="dot",
                     annotation_text="LCR Minimum",
                     row=1, col=1)
        
        return fig

    def run(self):
        """Run the dashboard server"""
        fig = self.create_gap_analysis()
        fig.show()
        # Uncomment for production:
        # fig.write_html("dashboards/liquidity_gap.html")

if __name__ == "__main__":
    dashboard = LiquidityDashboard()
    dashboard.run()
