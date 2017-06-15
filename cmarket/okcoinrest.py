# -*- coding: utf-8 -*-
"""
okccoin rest api
"""
import requests

URL_GET_R_TICKER = "https://www.okcoin.cn/api/v1/ticker.do"


class OKCoin(object):
    """
    OKcoin
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
        """get real time ticker data
        params: btc_cny ltc_cny
        """
        # if self.market not in ["btc_cny", "ltc_cny"]:
        #     return self.__err()
        if self.market == "btccny":
            market = "btc_cny"
        elif self.market == "ltccny":
            market = "ltc_cny"
        else:
            return self.__err()
        payload = {'symbol':market}
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
        parsed the okcion tickerdata
        """
        if not self.tickerdata:
            return self.__err()
        self.tickerdata["ticker"]["date"] = self.tickerdata["date"]
        self.tickerdata["ticker"]["platform"] = "okcoin"
        self.tickerdata["ticker"]["market"] = self.market
        self.tickerdata.pop("date")
        
        return self.tickerdata
