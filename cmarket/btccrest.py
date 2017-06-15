# -*- coding: utf-8 -*-
"""
BTCChina rest api
"""

import requests

URL_GET_R_TICKER = "https://data.btcchina.com/data/ticker"

class BTCChina(object):
    """
    Btcchina
    """
    def __init__(self, market=None, timeout=3):
        self.market = market
        self.tickerdata = None
        self.timeout = timeout
    def __err(self):
        return False
    @property
    def time_out(self):
        return self.time_out
    @time_out.setter
    def time_out(self, time):
        self.timeout = time
    def get_rt_ticker(self):
        """get real time ticker data from btcc
        params: btccny ltccny ltcbtc
        """
        if self.market not in ["btccny", "ltccny", "ltcbtc"]:
            return self.__err()
        payload = {'market':self.market}
        try:
            res = requests.get(URL_GET_R_TICKER, \
                                params=payload, timeout=self.timeout)
            self.tickerdata = res.json()
            return self.parsed_tickerdata
        except:
            self.tickerdata = None
    @property
    def parsed_tickerdata(self):
        """
        parsed the btcchina tickerdata
        """
        if not self.tickerdata:
            return self.__err()
        self.tickerdata["ticker"]["platform"] = "btcc"
        self.tickerdata["ticker"]["market"] = self.market
        return self.tickerdata
        