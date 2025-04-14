from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

class BalanceSheetForecaster:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path, index_col='date', parse_dates=True)

    def forecast_13q(self, column: str) -> pd.DataFrame:
        """13-quarter ARIMA forecasting"""
        model = ARIMA(self.df[column], order=(1, 1, 1))
        fitted = model.fit()
        forecast = fitted.get_forecast(steps=13)
        return pd.DataFrame({
            "Date": forecast.predicted_mean.index,
            column: forecast.predicted_mean.values,
            "CI_Lower": forecast.conf_int()[:, 0],
            "CI_Upper": forecast.conf_int()[:, 1]
        })

# Example usage
forecaster = BalanceSheetForecaster("data/jpm_10k_2023.csv")
deposits_forecast = forecaster.forecast_13q("deposits")
deposits_forecast.to_csv("reports/13q_forecast.csv")
