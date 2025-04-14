import requests
from sec_edgar_downloader import Downloader

class EdgarParser:
    def __init__(self):
        self.dl = Downloader("MyCompany", "my@email.com")

    def get_10k_filings(self, ticker: str, years: list):
        """Download 10-K filings and extract balance sheets"""
        for year in years:
            self.dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{2024-12-31")
            # Extract XBRL data to pandas DataFrame
            xbrl_data = self._parse_xbrl(f"edgar/{ticker}_10k_{year}.xml")
            xbrl_data.to_csv(f"data/edgar/{ticker}_10k_{year}.csv")

    def _parse_xbrl(self, file_path: str) -> pd.DataFrame:
        # Implement XBRL parsing logic
        return pd.DataFrame(...)
