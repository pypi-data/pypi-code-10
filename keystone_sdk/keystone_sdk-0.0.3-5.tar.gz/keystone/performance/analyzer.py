# -*- coding: utf-8 -*-

from six import with_metaclass
import abc
import numpy as np
from datetime import datetime, timedelta
from copy import copy

from keystone.performance import risk

class KSSampleRate():
    DAY = "DAY"
    HOUR = "HOUR"
    MINUTE = "MINUTE"
    SECOND = "SECOND"

    @classmethod
    def offset(cls, rate):
        if rate == cls.DAY:
            return timedelta(days = 1)
        elif rate == cls.HOUR:
            return timedelta(hours = 1)
        elif rate == cls.MINUTE:
            return timedelta(minutes = 1)
        elif rate == cls.SECOND:
            return timedelta(seconds = 1)
        else:
            return timedelta(0)

    @classmethod
    def getAnnulizedMultiplier(self, rate, tradingDays =250, tradingHours = 4, squared = False):
        if rate == KSSampleRate.HOUR:
            multiplier = tradingDays * tradingHours
        elif rate == KSSampleRate.MINUTE:
            multiplier = tradingDays * tradingHours * 60
        elif rate == KSSampleRate.SECOND:
            multiplier = tradingDays * tradingHours * 3600
        else:
            multiplier = tradingDays
        if squared:
            multiplier = np.sqrt(multiplier)

        return multiplier


class KSAnalyzer(with_metaclass(abc.ABCMeta)):
    '''
    Abstract class of analyzer.
    
    Class properties:
    returnTracker: ReturnTracker instance, shared by all analyzer
    tradingDays: shared by all analyzer
    tradingHours: shared by all analyzer
    sampleRate: shared by all analyzer
    riskless: shared by all analyzer
    '''
    returns = None
    tradingDays = None
    tradingHours = None
    sampleRate = None
    riskless = None
    def getAnnulizedMultiplier(self, squared = True):
        return KSSampleRate.getAnnulizedMultiplier(
            self.sampleRate, 
            self.tradingDays, 
            self.tradingHours, 
            squared)
    def update(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def value(self, *args, **kwargs):
        pass

class KSVolatility(KSAnalyzer):
    def value(self, *args, **kwargs):
        if self.returns is None or len(self.returns.algoReturns) <= 1:
            return 0.0
        return np.std(self.returns.algoReturns, ddof=1) * self.getAnnulizedMultiplier(squared = True)

class KSBeta(KSAnalyzer):
    def value(self, *args, **kwargs):
        """
        http://en.wikipedia.org/wiki/Beta_(finance)
        """
        if self.returns is None or len(self.returns.algoReturns) <= 1:
            return 0.0
            
        return risk.beta(self.returns.algoReturns, self.returns.benchmarkReturns)

class KSDownsideRisk(KSAnalyzer):
    def value(self, *args, **kwargs):
        """
        https://en.wikipedia.org/wiki/Downside_risk
        """
        if self.returns is None or len(self.returns.algoReturns) <= 1:
            return 0.0
            
        return risk.downside_risk(self.returns.algoReturns,
                             self.returns.algoMeanReturns,
                             self.getAnnulizedMultiplier())

class KSAlpha(KSAnalyzer):
    def value(self, *args, **kwargs):
        """
        http://en.wikipedia.org/wiki/Alpha_(investment)
        """
        if self.returns is None or len(self.returns.algoReturns) == 0:
            return 0.0
            
        beta = KSBeta().value()
        return risk.alpha(
            self.returns.algoAnnulizedMeanReturns[-1],
            self.riskless,
            self.returns.benchmarkAnnulizedMeanReturns[-1],
            beta)

class KSInformationRatio(KSAnalyzer):
    def value(self, *args, **kwargs):
        """
        http://en.wikipedia.org/wiki/Information_ratio
        """
        if self.returns is None or len(self.returns.algoReturns) <= 1:
            return 0.0
            
        volatility = KSVolatility().value()
        return risk.information_ratio(
            self.returns.algoAnnulizedMeanReturns[-1],
            self.returns.benchmarkAnnulizedMeanReturns[-1],
            volatility)

class KSSortinoRatio(KSAnalyzer):
    def value(self, *args, **kwargs):
        """
        http://en.wikipedia.org/wiki/Sortino_ratio
        """
        if self.returns is None or len(self.returns.algoReturns) <= 1:
            return 0.0

        downsideRisk = KSDownsideRisk().value()
        return risk.sortino_ratio(
            self.returns.algoAnnulizedMeanReturns[-1],
            self.riskless,
            downsideRisk)

class KSSharpRatio(KSAnalyzer):
    def value(self, *args, **kwargs):
        """
        http://en.wikipedia.org/wiki/Sharpe_ratio
        """
        if self.returns is None or len(self.returns.algoReturns) <= 1:
            return 0.0

        volatility = KSVolatility().value()
        return risk.sharpe_ratio(
            self.returns.algoAnnulizedMeanReturns[-1],
            self.riskless,
            volatility)

class KSMaxDrawdown(KSAnalyzer):
    def __init__(self):
        KSAnalyzer.__init__(self)
        self.currentMaxReturn = -np.inf
        self.currentDrawdown = 0.0

    def value(self, *args, **kwargs):
        if self.returns is None or len(self.returns.algoCumulativeReturns) == 0:
            return self.currentDrawdown

        self.currentMaxReturn = np.max((self.currentMaxReturn, self.returns.algoCumulativeReturns[-1]))
        # The drawdown is defined as: (high - low) / high
        # The above factors out to: 1.0 - (low / high)
        drawdown = 1.0 - (1.0 + self.returns.algoCumulativeReturns[-1])/(1.0 + self.currentMaxReturn)
        if self.currentDrawdown < drawdown:
            self.currentDrawdown = drawdown

        return self.currentDrawdown


class KSDefaultAnalyzer(KSAnalyzer):
    def value(self, *args, **kwargs):
        ret = {
        'alpha': KSAlpha().value(),
        'beta': KSBeta().value(),
        'volatility': KSVolatility().value(),
        'max_drawdown': KSMaxDrawdown().value(),
        'downside_risk': KSDownsideRisk().value(),
        'sharpe_ratio': KSSharpRatio().value(),
        'sortino_ratio': KSSortinoRatio().value(),
        'information_ratio': KSInformationRatio().value()
        }
        return ret

class KSCumulativeAnalyzer(KSAnalyzer):
    def __init__(self):
        self.alpha = []
        self.beta = []
        self.volatility = []
        self.max_drawdown = []
        self.downside_risk = []
        self.sharpe_ratio = []
        self.sortino_ratio = []
        self.information_ratio = []

        self.count = 0

    def value(self, *args, **kwargs):
        fields = copy(self.__dict__)
        return fields

    def update(self, *args, **kwargs):
        self.count += 1
        if self.count > 2:
            self.alpha.append(KSAlpha().value())
            self.beta.append(KSBeta().value())
            self.volatility.append(KSVolatility().value())
            self.max_drawdown.append(KSMaxDrawdown().value())
            self.downside_risk.append(KSDownsideRisk().value())
            self.sharpe_ratio.append(KSSharpRatio().value())
            self.sortino_ratio.append(KSSortinoRatio().value())
            self.information_ratio.append(KSInformationRatio().value())
