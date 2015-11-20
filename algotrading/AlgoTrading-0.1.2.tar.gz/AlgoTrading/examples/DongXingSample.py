# -*- coding: utf-8 -*-
u"""
Created on 2015-9-23

@author: cheng.li
"""

import datetime as dt

from AlgoTrading.Strategy.Strategy import Strategy
from AlgoTrading.Backtest import strategyRunner
from AlgoTrading.Backtest import DataSource
from AlgoTrading.Data import set_universe
from PyFin.API import MA
from PyFin.API import MAX
from PyFin.API import MIN


class MovingAverageCrossStrategy(Strategy):
    def __init__(self):
        filtering = (MAX(10, 'close') / MIN(10, 'close')) >= 1.02
        indicator = MA(10, 'close') - MA(120, 'close')
        self.signal = indicator[filtering]

    def handle_data(self):
        for s in self.universe:
            amount = self.avaliableForSale(s)
            if self.signal[s] > 0. and self.secPos[s] == 0:
                if s != "if1501":
                    self.order(s, 1, quantity=300)
                else:
                    self.order(s, 1, quantity=300)
            if self.signal[s] < 0. and amount != 0:
                if s != "if1501":
                    self.order(s, -1, quantity=300)
                else:
                    self.order(s, -1, quantity=300)


def run_example():
    universe = set_universe('000300.zicn')
    initialCapital = 150000.0
    startDate = dt.datetime(2012, 1, 1)
    endDate = dt.datetime(2015, 10, 1)

    strategyRunner(userStrategy=MovingAverageCrossStrategy,
                   initialCapital=initialCapital,
                   symbolList=universe,
                   startDate=startDate,
                   endDate=endDate,
                   dataSource=DataSource.DXDataCenter,
                   freq=0,
                   benchmark='000300.zicn',
                   logLevel='critical',
                   saveFile=False,
                   plot=True)


if __name__ == "__main__":
    from AlgoTrading.Env import Settings
    Settings.enableCache()
    startTime = dt.datetime.now()
    print("Start: %s" % startTime)
    run_example()
    endTime = dt.datetime.now()
    print("End : %s" % endTime)
    print("Elapsed: %s" % (endTime - startTime))
