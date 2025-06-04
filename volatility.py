import pandas as pd
import numpy as np
import math

class Volatility():

    def __init__(self, ticker : str, open : pd.Series, close : pd.Series , high : pd.Series , low : pd.Series):
        # Arguments passed as pd.Series

        self.ticker = ticker
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.mean = self.close.mean()
        self.tradingdays = len(self.close)
    
    def calculate_std_deviation(self, window = 20, annualizefactor = 252):
        
        logreturns = np.log(self.close / self.close.shift(1))
        daily_vol = logreturns.rolling(window=window).std()
        annualized_vol = daily_vol * np.sqrt(annualizefactor)
        return annualized_vol



    