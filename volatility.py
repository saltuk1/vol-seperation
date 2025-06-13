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
        self.volatility_metrics['Vol_Parkinson'] = self._parkinson_volatility(window)

        # Calculate volatility (Garman-Klaas)
        self.volatility_metrics['Vol_GK'] = self._garman_klaas_volatility(window)

        # Calculate volatility (Standard Deviation)
        self.volatility_metrics['Vol_Std'] = self.data['log_returns'].rolling(window).std() * np.sqrt(252)

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

        return annualized_yang_zheng_vol
    
    def _parkinson_volatility(self, window: int) -> pd.Series:

        log_hl = np.log(self.data['High']/self.data['Low'])
        squared_hl = log_hl**2
        park_const = 1 / (4 * np.log(2))

        daily_parkinson_vol = np.sqrt((park_const * squared_hl).rolling(window).mean())
        annualized_parkinson_vol = daily_parkinson_vol * np.sqrt(252)
        return annualized_parkinson_vol
    
    def _garman_klaas_volatility(self, window:int) -> pd.Series:

        log_hl = np.log(self.data['High']/self.data['Low'])**2
        log_co = np.log(self.data['Close']/self.data['Open'])**2

        gk_const = 2*np.log(2) - 1

        daily_garman_klaas_vol = np.sqrt((0.5 * log_hl - gk_const * log_co).rolling(window).mean())
        annualized_garman_klaas_vol = daily_garman_klaas_vol * np.sqrt(252)

        return annualized_garman_klaas_vol