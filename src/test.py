from sources.etf_http_source import BrdHttpSource, AllianzHttpSource
from utils.etf_interpolator import EtfInterpolator
from utils.etf_interpolator import largestCommonInterval
from utils.etf_plots import plotPrices
from utils.types import EtfPlotInfo

brds = BrdHttpSource()
alls = AllianzHttpSource()

global_e = EtfInterpolator(brds.get('GLOBAL_E'))
global_a = EtfInterpolator(brds.get('GLOBAL_A'))
world_equity = EtfInterpolator(alls.get('WORLD_EQUITY'))
europe_equity = EtfInterpolator(alls.get('EUROPE_EQUITY'))
leu_simplu = EtfInterpolator(alls.get('LEU_SIMPLU'))

etfs = []

minDate, maxDate = largestCommonInterval(global_a, world_equity, europe_equity, leu_simplu)
#minDate = maxDate - datetime.timedelta(days=60)

print(minDate, maxDate)
emaWeight = 0.0

#pointsList = global_e.getRange(minDate, maxDate, normalizedStart=True, emaWeight=emaWeight)
#dates = list(map(lambda point: point.date, pointsList))
#prices = list(map(lambda point: point.price, pointsList))
#etfs.append(EtfPlotInfo('BRD - Global E', prices))

pointsList = global_a.getRange(minDate, maxDate, normalizedStart=True, emaWeight=emaWeight)
dates = list(map(lambda point: point.date, pointsList))
prices = list(map(lambda point: point.price, pointsList))
etfs.append(EtfPlotInfo('BRD - Global A', prices))

pointsList = europe_equity.getRange(minDate, maxDate, normalizedStart=True, emaWeight=emaWeight)
dates = list(map(lambda point: point.date, pointsList))
prices = list(map(lambda point: point.price, pointsList))
etfs.append(EtfPlotInfo('Allianz - Europe Equity', prices))

pointsList = world_equity.getRange(minDate, maxDate, normalizedStart=True, emaWeight=emaWeight)
dates = list(map(lambda point: point.date, pointsList))
prices = list(map(lambda point: point.price, pointsList))
etfs.append(EtfPlotInfo('Allianz - World Equity', prices))

pointsList = leu_simplu.getRange(minDate, maxDate, normalizedStart=True, emaWeight=emaWeight)
dates = list(map(lambda point: point.date, pointsList))
prices = list(map(lambda point: point.price, pointsList))
etfs.append(EtfPlotInfo('Allianz - Leu Simplu', prices))

plotPrices(dates, etfs)