import os
from abc import ABC, abstractmethod
from twelvedata import TDClient
import os
import pandas as pd
import yfinance

class DataSourceAdapter(ABC):
    @abstractmethod
    def get_data(self,symbol: str, interval: str) -> pd.DataFrame:
        pass

class TwelveDataAdapter(DataSourceAdapter):

    def __init__(self, api_key: str):
        self.api_key = os.getenv("TWELVE_DATA_API",default=None)

    def get_data(self, symbol: str, interval: str, exchange: str = None, outputsize: int = 10,
                 timezone: str = "America/New York") -> pd.DataFrame:

        try:
            if not self.api_key:
                raise ValueError("Not Found API Key")
            client = TDClient(apikey=self.api_key)
            if not exchange:
                response = client.time_series(symbol=symbol, interval=interval, outputsize=outputsize,
                                              timezone=timezone)
            else:
                response = client.time_series(symbol=symbol, interval=interval, exchange=exchange,
                                              outputsize=outputsize, timezone=timezone)
        except Exception as e:
            raise e

        return response.as_pandas()

class YahooFinanceAdapter(DataSourceAdapter):

    def get_data(self, symbol: str, interval: str) -> pd.DataFrame:
        try:
            response = yfinance.Ticker(symbol).history(period="1d", interval=interval,actions=False)
        except Exception as e:
            raise e

        return response