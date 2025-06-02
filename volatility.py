import pandas as pd

class Volatilty():

    def __init__(self, ticker : str, open : pd.Series, close : pd.Series , high : pd.Series , low : pd.Series):

        # Arguments passed as pd.Series

        self.ticker = ticker
        self.open = open
        self.close = close
        self.high = high
        self.low = low


    def calculate_mean(self):
        
        return self.close.mean()