# -*- coding: utf-8 -*-
"""
The app gets the market ticker data to db from
configure file.
"""
import time
import json
import os
import sys
sys.path.append("..")
from cmarket import marketapi
# import cmarket.marketapi
from db.dbinflux import DbInflux

__DEBUG__ = True

def dprint(argv):
    if __DEBUG__:
        print argv

class MarketTicker(object):
    """
    get the marker ticker
    """
    def __init__(self,confpath):
        self.confpath = confpath
        self.load_conf(self.confpath)
        self.market = marketapi.connect_market(self.confdata["platform"],\
                        self.confdata["market"])
        self.db = DbInflux(self.confdata["dbhost"], self.confdata["dbport"])

    def load_conf(self, confpath):
        """
        load a config file ,return the config data
        """
        with open(confpath) as json_file:
            confdata = json.load(json_file)
        if confdata:
            self.confdata = confdata
        else:
            raise ValueError

    def do_ticker(self):
        """
        get ticker and save to db
        """
        conf = self.confdata
        tdata = self.market.get_rt_ticker()
        dprint(tdata)
        if tdata:
            self.db.insert(conf["db"], conf["table"], conf["tagkeys"],\
                            conf["fieldkeys"], conf["tskey"], tdata["ticker"])

    def run(self):
        """
        run the ticker app
        """
        while True:
            self.do_ticker()
            time.sleep(0.5)


if __name__ == "__main__":
    confile = sys.argv[1]
    if not confile:
        print "argv error."
    root = os.getcwd()
    print root+"/conf/"+confile
    mt = MarketTicker(root+"/conf/"+confile)
    mt.run()