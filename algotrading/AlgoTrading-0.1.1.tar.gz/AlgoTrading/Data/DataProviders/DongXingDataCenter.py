# -*- coding: utf-8 -*-
u"""
Created on 2015-9-23

@author: cheng.li
"""

import datetime as dt
import numpy as np
import pandas as pd
from enum import IntEnum
from enum import unique
from AlgoTrading.Data.Data import DataFrameDataHandler
from DataAPI import api


@unique
class FreqType(IntEnum):
    MIN1 = 1
    MIN5 = 5
    EOD = 0


class DXDataCenter(DataFrameDataHandler):

    _req_args = ['symbolList', 'startDate', 'endDate', 'freq']

    def __init__(self, **kwargs):
        super(DXDataCenter, self).__init__(kwargs['logger'])
        self.symbolList = [s.lower() for s in kwargs['symbolList']]
        self.fields = ['instrumentID', 'tradingDate', 'tradingTime', 'openPrice', 'highPrice', 'lowPrice', 'closePrice', 'volume']
        self.shortDict = {s[:6]: s for s in self.symbolList}
        self.startDate = kwargs['startDate']
        self.endDate = kwargs['endDate']
        self._freq = kwargs['freq']
        self._getMinutesBars(startDate=self.startDate.strftime("%Y-%m-%d"),
                             endDate=self.endDate.strftime("%Y-%m-%d"),
                             freq=self._freq)
        if kwargs['benchmark']:
            self._getBenchmarkData(kwargs['benchmark'],
                                   self.startDate.strftime("%Y-%m-%d"),
                                   self.endDate.strftime("%Y-%m-%d"))

    def _getMinutesBars(self, startDate, endDate, freq):

        self.logger.info("Starting load bars data from DX data center...")

        self.symbolData = {}

        if freq == FreqType.MIN1:
            data_api = api.GetEquityBarMin1
        elif freq == FreqType.MIN5:
            data_api = api.GetEquityBarMin5
        elif freq == FreqType.EOD:
            data_api = api.GetEquityBarEOD
        else:
            raise ValueError("Unknown bar type")

        res = data_api([s[:6] for s in self.symbolList],
                       startDate,
                       endDate,
                       self.fields)

        timeIndexList = []
        dataList = []

        res = res.as_matrix()
        for row in res:
            s = self.shortDict[row[0]]
            if s not in self.symbolData:
                self.symbolData[s] = {}
                self.latestSymbolData[s] = []
            timeIndexList.append(row[1] + " " + row[2][:-1] + "+0000")
            dataList.append((s, {'open': row[3],
                                 'high': row[4],
                                 'low': row[5],
                                 'close': row[6],
                                 'volume': row[7]}))

        timeIndexList = np.array(timeIndexList, dtype='datetime64').astype(dt.datetime)
        for timeIndex, data in zip(timeIndexList, dataList):
            self.symbolData[data[0]][timeIndex] = data[1]

        self.dateIndex = np.unique(timeIndexList)
        self.dateIndex.sort()
        self.start = 0
        for i, s in enumerate(self.symbolList):
            if s not in self.symbolData:
                del self.symbolList[i]

        self.logger.info("Bars loading finished!")

    def _getBenchmarkData(self, indexID, startTimeStamp, endTimeStamp):

        self.logger.info("Starting load benchmark {0:s} daily bar data from DX data center...".format(indexID))

        indexData = api.GetIndexBarEOD(indexID[:6], startDate=startTimeStamp, endDate=endTimeStamp)
        indexData = indexData[['closePrice']]
        indexData.columns = ['close']
        indexData.index = pd.to_datetime(indexData.index.date)
        indexData['return'] = np.log(indexData['close'] / indexData['close'].shift(1))
        indexData = indexData.dropna()
        self.benchmarkData = indexData

        self.logger.info("Benchmark data loading finished!")
