import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mic = yf.Ticker("MSFT")
    MSOFT = mic.history(period="5mo")
    delcols = ["Dividends", "Stock Splits", "Volume"]
    for a in delcols:
        del MSOFT[a]
    #plt.plot(MSOFT["Open"])
    #plt.show()
    print(MSOFT)
    MSOFT["Open"].plot()
    plt.show()




