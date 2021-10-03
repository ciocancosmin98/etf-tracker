import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.dates as mdates

from sources.etf_http_source import BrdHttpSource, AllianzHttpSource
from utils.etf_interpolator import EtfInterpolator
from utils.etf_interpolator import largestCommonInterval
from utils.etf_plots import plotPrices, plotPricesAxes
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

# plotPrices(dates, etfs)

root = tkinter.Tk()
root.wm_title('ETF Tracker 1.0')

fig = Figure(figsize=(5, 4), dpi=100)
axes = fig.add_subplot(111)
fig.autofmt_xdate()

plotPricesAxes(axes, dates, etfs)

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def on_click(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))

    #print(toolbar.selection_get())
    print(toolbar._buttons['Zoom'].var.get())

    xlims = axes.get_xlim()
    daysDisplayed = xlims[1] - xlims[0]

    print(daysDisplayed)

    if daysDisplayed > 365 * 4:
        interval = 365
    elif daysDisplayed > 365:
        interval = 90
    else:
        interval = 30

    axes.xaxis.set_major_locator(mdates.DayLocator(interval=interval))



canvas.mpl_connect("key_press_event", on_key_press)
canvas.mpl_connect("button_release_event", on_click)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
