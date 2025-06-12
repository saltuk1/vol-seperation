import pandas as pd
import numpy as np
import math
from typing import Dict, Tuple, List, Optional

class Volatility:

    def __init__(self, data: pd.DataFrame):

        self.data = data.copy()
        self.volatility_metrics = {}
        # self.signals = {} # Saving it for the future
    
'''    def calculate_std_deviation(self):
        
        # Using log returns to apply the CLT for returns, since raw returns are left-skewed
        
        logreturns = np.log(self.close / self.close.shift(1))
        daily_vol = logreturns.rolling(window=self.window).std()
        annualized_std = daily_vol * np.sqrt(self.annualizefactor)
        return annualized_std

    def calculate_vol_parkinson(self):

        log_hl_ratio = np.log(self.high / self.low)
        squared_log_hl_ratio = log_hl_ratio**2
        parkinson_constant = 1 / (4 * np.log(2))

        # Rolling mean of the 'variance proxy' (squared log HL ratio)
        daily_parkinson_variance_proxy = np.sqrt(parkinson_constant * squared_log_hl_ratio)
        rolling_parkinson_vol_squared = daily_parkinson_variance_proxy.rolling(window = self.window).mean()
        daily_parkinson_vol = np.sqrt(rolling_parkinson_vol_squared)
        
        # Annualize the daily parkinson vol
        annualized_parkinson_vol = daily_parkinson_vol * np.sqrt(self.annualizefactor)

        return annualized_parkinson_vol

    def calculate_vol_garmanklaas(self):

        log_squared_oc_ratio = (np.log(self.close / self.open))**2
        log_squared_hl_ratio = (np.log(self.high / self.low))**2
        garmanklaas_constat = 2 * np.log(2) - 1

        daily_garmanklaas_proxy = 0.5 * log_squared_hl_ratio - garmanklaas_constat * log_squared_oc_ratio
        daily_garmanklaas_proxy = daily_garmanklaas_proxy.clip(lower=0) # Capped at 0 since variance can't be negative

        rolling_garmanklaas_vol_squared = daily_garmanklaas_proxy.rolling(window = self.window).mean()
        daily_garmanklaas_vol = np.sqrt(rolling_garmanklaas_vol_squared)
        
        annualized_garmanklaas_vol = daily_garmanklaas_vol * np.sqrt(self.annualizefactor)

        return annualized_garmanklaas_vol'''
