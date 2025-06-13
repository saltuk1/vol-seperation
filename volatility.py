import pandas as pd
import numpy as np
import math
from typing import Dict, Tuple, List, Optional

class Volatility:

    def __init__(self, data: pd.DataFrame):

        self.data = data.copy()
        self.volatility_metrics = {}
        # self.signals = {} # Saving it for the future


    def calculate_volatility_metrics(self, window: int = 30) -> Dict[str, pd.Series]:

        # Calculate log returns
        self.data['log_returns'] = np.log(self.data['Close']/self.data['close'].shift(1))

        # Calculate volatility (Yang-Zheng)
        self.volatility_metrics['Vol_YZ'] = self._yang_zheng_volatility(window)

        # Calculate volatility (Parkinson)

        # Calculate volatility (Garman-Klaas)

        # Calculate volatility (Standard Deviation)

    def _yang_zheng_volatility(self, window: int) -> pd.Series:

        log_co = np.log(self.data['Close']/self.data['Open'])
        log_ho = np.log(self.data['High']/self.data['Open'])
        log_hc = np.log(self.data['High']/self.data['Close'])
        log_lo = np.log(self.data['Low']/self.data['Open'])
        log_lc = np.log(self.data['Low']/self.data['Close'])

        log_oc_prev = np.log(self.data['Open']/self.data['Close'].shift(1))

        k = 0.34 / (1.34 + ((window + 1)/window -1))

        opentoclose_var = log_oc_prev.rolling(window).var()
        closetoopen_var = log_co.rolling(window).var()
        roger_satchell_var = ((log_hc*log_ho) + (log_lc*log_lo)).rolling(window).mean()

        daily_yang_zheng_vol = np.sqrt(opentoclose_var + k*closetoopen_var + (1- k)*roger_satchell_var)
        annualized_yang_zheng_vol = daily_yang_zheng_vol * np.sqrt(252)

        return daily_yang_zheng_vol, annualized_yang_zheng_vol
    
    def _parkinson_volatility(self, window: int) -> pd.Series:

        log_hl = np.log(self.data['High']/self.data['Low'])
        squared_hl = log_hl**2
        park_const = 1 / (4 * np.log(2))

        daily_parkinson_vol = np.sqrt((park_const * squared_hl).rolling(window).mean())
        annualized_parkinson_vol = daily_parkinson_vol * np.sqrt(252)
        return daily_parkinson_vol, annualized_parkinson_vol


    
    
'''    def calculate_std_deviation(self):
        
        # Using log returns to apply the CLT for returns, since raw returns are left-skewed
        
        logreturns = np.log(self.close / self.close.shift(1))
        daily_vol = logreturns.rolling(window=self.window).std()
        annualized_std = daily_vol * np.sqrt(self.annualizefactor)
        return annualized_std

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
