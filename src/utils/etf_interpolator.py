from typing import List, Tuple
import datetime

import sys
sys.path.append('..')

from utils.types import EtfPoint

class EtfInterpolator:
    def _interpolatePrices(self):
        self._prices: dict[datetime.date, float] = {}

        if len(self._points) == 0:
            return
        elif len(self._points) == 1:
            self._prices[self._points[0].date] = self._points[0].price
            return

        last_point = self._points[0]
        self._prices[last_point.date] = last_point.price

        for i in range(1, len(self._points)):
            next_point = self._points[i]

            ndays = (next_point.date - last_point.date).days
            for delta in range(1, ndays + 1):
                interpDate = last_point.date + datetime.timedelta(days=delta)

                interpFactor = delta / ndays
                interpPrice = (1 - interpFactor) * last_point.price + interpFactor * next_point.price

                self._prices[interpDate] = interpPrice

            last_point = next_point

    def __init__(self, points: List[EtfPoint], interpType: str = 'linear'):
        points.sort(key=lambda x: x.date)
        
        self._points = points
        self._minDate = points[0].date
        self._maxDate = points[-1].date
        self._interpType = interpType

        self._interpolatePrices()

    def getMin(self):
        return self._minDate

    def getMax(self):
        return self._maxDate

    def getPrice(self, date: datetime.date):
        if not date in self._prices:
            raise ValueError('Date out of range')

        return self._prices[date]

    def getRange(self, startDate: datetime.date = None, endDate: datetime.date = None, 
            step: int = 1, normalizedStart = False, emaWeight: float = 0.0):
        if startDate is None:
            startDate = self._minDate

        if endDate is None:
            endDate = self._maxDate

        if not (startDate in self._prices and endDate in self._prices):
            raise ValueError('Dates out of range')
            
        pointRange: List[EtfPoint] = []

        ndays = (endDate - startDate).days

        if normalizedStart:
            weightedPrice = 1.0
        else:
            weightedPrice = self._prices[startDate]

        for delta in range(0, ndays + 1, step):
            date  = startDate + datetime.timedelta(days=delta)
            price = self._prices[date]

            if normalizedStart:
                price = price / self._prices[startDate]

            weightedPrice = weightedPrice * emaWeight + price * (1 - emaWeight)

            pointRange.append(EtfPoint(weightedPrice, date))
        
        return pointRange

def largestCommonInterval(*interps: List[EtfInterpolator]) -> Tuple[datetime.date, datetime.date]:
    minDate = interps[0].getMin()
    maxDate = interps[0].getMax()

    for i in range(1, len(interps)):
        interp = interps[i]

        if minDate < interp.getMin():
            minDate = interp.getMin()
        
        if maxDate > interp.getMax():
            maxDate = interp.getMax()

    return (minDate, maxDate)