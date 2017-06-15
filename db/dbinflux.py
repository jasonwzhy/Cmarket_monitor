# -*- coding: utf-8 -*-
"""
Influx DB api
"""
import requests


class DbInflux(object):
    """
    influxdb
    """
    def __init__(self, host, port):
        self.host = host
        self.port = str(port)
        self.dbhost = "http://"+self.host+":"+self.port+"/" #"http://localhost:32768/"
    def create_db(self):
        pass
    
    def show_dbs(self):
        payload = {"q":"show databases"}
        r = requests.post(self.dbhost+"query", data=payload)
        # print r.text
        # r.json

    def insert(self, db, tablename, tagkeys, fieldkeys, tskey, line_data, ts=None):
        # payload = line_data
        url = self.dbhost+"write?db="+db
        payload = self._format_line_pro(tablename, tagkeys, fieldkeys, tskey, line_data, ts)
        # print payload
        r = requests.post(url, data=payload)

    def _format_line_pro(self, tablename, tagkeys, fieldkeys, tskey, data, ts=None):
        """
        Line Protocol是由tablename , tag , field组成
        方法接受一个dict数据，和定义tablename , tag, field的key list数据
        根据tagkeys, fieldkeys找到dict数据中对应的key，取出拼接为Line Protocol数据
        """
        if not isinstance(tablename, str) and not tablename.strip():
            return False
        tbline = tablename+','
        tagline, fieldline = [], []
        tsline = " "
        for tagkey in tagkeys:
            try:
                tagline.append(tagkey+"="+str(data[tagkey]))
            except:
                pass
        for fieldkey in fieldkeys:
            try:
                fieldline.append(fieldkey+"="+str(data[fieldkey]))
            except:
                pass
        if ts:
            tsline += self._fil_nano(ts)
        else:
            try:
                tsline += self._fil_nano(int(data[tskey]))
            except:
                pass
        return tbline + ",".join(tagline) +" "+ ",".join(fieldline) + tsline

    def _fil_nano(self,ts):
        """
        influxdb 的timestamp 是19位纳x秒级，所以使用字符串手段处理补齐
        """
        if isinstance(ts, int):
            try:
                ts = str(ts)
                ts += "0" * (19 - len(ts))
            except:
                raise ValueError
        return ts

if __name__ == "__main__":
    data={
        "ticker":{
            "high": "19479.00",
            "low": "17796.64",
            "buy": "19080.00",
            "sell": "19097.88",
            "last": "19082.88",
            "vol": "14927.13680000",
            "date": 1496940116,
            "vwap": "18693.56",
            "prev_close": "18302.01",
            "open": "18302.01"
            }
    }
    data2 = {
        "ticker":{
        "date": "1496939964",
        "buy": "18960.0",
        "high": "19700.0",
        "last": "18966.12",
        "low": "17808.0",
        "sell": "18966.12",
        "vol": "15498.2060001"
        }
    }
    db = DbInflux("localhost",32768)
    print db.insert("mydb","ticker",["last"],["low","high"],"date",data['ticker'])