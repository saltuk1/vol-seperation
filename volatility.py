import pandas as pd
import numpy as np
import math

class Volatility():

    def __init__(self, ticker : str, open : pd.Series, close : pd.Series , high : pd.Series , low : pd.Series, window:int, annualizefactor:int):
        # Arguments passed as pd.Series

        self.ticker = ticker
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.tradingdays = len(self.close)
        self.window = window
        self.annualizefactor = annualizefactor
    
    def calculate_std_deviation(self):
        
        logreturns = np.log(self.close / self.close.shift(1))
        daily_vol = logreturns.rolling(window=self.window).std()
        annualized_std = daily_vol * np.sqrt(self.annualizefactor)
        return annualized_std

    def calculate_vol_parkinson(self):

        high_low_ratio = np.log(self.high / self.low)
        parkinson_factor = 1 / (4 * np.log(2))
        parkinson_vol = np.sqrt(parkinson_factor * high_low_ratio**2)
        annualized_vol_par = parkinson_vol * np.sqrt(self.annualizefactor)
        return annualized_vol_par




    