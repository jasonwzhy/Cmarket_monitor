# -*- coding: utf-8 -*-

import requests

DBHOST = "http://localhost:32768/"

def show_dbs():
    payload = {"q":"show databases"}
    r = requests.post(DBHOST+"query", data=payload)
    print r.text

def insert(db,line_data):
    payload = line_data
    url = DBHOST+"write?db="+db
    r = requests.post(url, data=payload)
    print r.text

def _format_line_pro(tablename, tagkeys, fieldkeys, tskey, data, ts=None):
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
        tsline += _fil_nano(ts)
    else:
        try:
            tsline += _fil_nano(int(data[tskey]))
        except:
            pass
    return tbline + ",".join(tagline) +" "+ ",".join(fieldline) + tsline

def _fil_nano(ts):
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

    print _format_line_pro("ticker",["last",],["buy","sell"],"date",data['ticker'])

    # show_dbs()

    # data = "cpu,host=server05,region=uswest load=423 1434055562000000000"
    # insert("mydb",data)
