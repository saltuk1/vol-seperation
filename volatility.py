import pandas as pd
import math

class Volatilty():

    def __init__(self, ticker : str, open : pd.Series, close : pd.Series , high : pd.Series , low : pd.Series):

        # Arguments passed as pd.Series

        self.ticker = ticker
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.mean = self.close.mean()
        self.tradingdays = len(self.close)
    
    def calculate_std_deviation(self):
        return self.close.std()

    