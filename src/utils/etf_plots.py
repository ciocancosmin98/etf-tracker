import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import List, Tuple
import datetime

import sys
sys.path.append('..')

from utils.types import EtfPlotInfo


def plotPrices(dates: List[datetime.date], etfs: List[EtfPlotInfo]):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=365))

    for etf in etfs:
        assert len(dates) == len(etf.prices)
        plt.plot(dates, etf.prices, label=etf.name)

    plt.legend()

    plt.gcf().autofmt_xdate()
    plt.show()

def plotGains(gains: List[Tuple[datetime.date, float]]):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())

    dates = list(map(lambda point: point[0], gains))
    prices = list(map(lambda point: point[1] * 100, gains))

    plt.bar(dates, prices, width=20)
    plt.gcf().autofmt_xdate()
    plt.show()