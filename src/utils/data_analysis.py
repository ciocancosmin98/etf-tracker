from typing import List, Tuple
import datetime

import sys
sys.path.append('..')

from ..utils.types import EtfPoint

def listToDict(points: List[EtfPoint]):
    return {
        point.date : point.price for point in points
    }

def periodicGains(points: List[EtfPoint], period: datetime.timedelta, startDate = None) -> List[Tuple[datetime.date, float]]:
    pricesDict = listToDict(points)
    maxDate = points[-1].date

    if startDate is None:
        startDate = points[0].date

    if not startDate in pricesDict:
        raise ValueError('Start date not in range')

    periodicGains: List[Tuple[datetime.date, float]] = []

    lastDate = startDate
    while lastDate in pricesDict:
        nextDate = lastDate + period

        if not nextDate in pricesDict:
            nextDate = maxDate

            if nextDate == lastDate:
                break

        priceRatio = pricesDict[nextDate] / pricesDict[lastDate]
        periodicGains.append((lastDate, priceRatio - 1.0))

        lastDate = nextDate

    return periodicGains