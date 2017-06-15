# -*- coding: utf-8 -*-
"""
market api
"""

from btccrest import BTCChina
from okcoinrest import OKCoin

import time

def market_platform(platform, market):
    """return the formated data in diffrent platform &
    diffrent market
    """
    if market not in ["btccny", "ltccny", "ltcbtc"] or platform not in ["okcoin", "btcc"]:
        raise ValueError("Error Market or Platform")
    if platform == "okcoin":
        platform_obj = OKCoin
    elif platform == "btcc":
        platform_obj = BTCChina
    return platform_obj(market)

def connect_market(platform, market):
    """
    set platform options
    """
    try:
        res = market_platform(platform, market)
    except ValueError as ve:
        print ve
        return False
    if not res:
        return False
    res.time_out = 1
    return res

#Test
if __name__ == "__main__":
    mt = connect_market("btcc", "btccny")
    import json
    if not mt:
        exit()
    while True:
        print mt.get_rt_ticker()
        # print r.parsed_tickerdata
        # print get_rticker("btcc","btccny")
        # print get_rticker("btcc","ltccny")
        # print get_rticker("btcc","ltcbtc")
        # print get_rticker("okcoin","btccny")
        # print get_rticker("okcoin","ltccny")
        time.sleep(0.1)
