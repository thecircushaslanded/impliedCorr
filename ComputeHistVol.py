from glob import glob
import datetime as dt
import zipfile

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show

data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"

window = 10
# Load the data.
try:
    1/0
    df = pd.read_csv("HistVolData.csv", index_col=0)
except:
    data = []
    for file in glob(data_loc+"INTL.*zip"):
        zf = zipfile.ZipFile(file)
        thing1 = pd.read_csv(zf.open("INTL.IVYHISTVOL."+file[-13:-4]+".txt"), 
                delimiter='\t', names=["SecurityID", "Date", "Days", "Currency",
                "Volatility"], na_values=[-99.99])
        thing2 = pd.read_csv(zf.open("INTL.IVYSECPR."+file[-13:-4]+".txt"), 
                sep='\t', header=False, names=[ "SecurityID", "Date", "Exchange", 
                    "Bid", "Ask", "High", "Low", "Open", "Close", "TotalRet", 
                    "AskFactor", "CTotalRetFactor", "Currency", "Volume"], 
                na_values=["", "NA", "-99.99"], 
                usecols=["SecurityID", "Date", "Close", "TotalRet", "Exchange"])
                # usecols=["SecurityID", "Date", "Close", "Exchange"])
        try:
            histvol_STOXX = thing1[(thing1["SecurityID"] ==504880) & (
                thing1["Days"]==window)].iloc[0]["Volatility"]
            secpr_STOXX = thing2[(thing2["SecurityID"] == 504880) & 
                    (thing2["Exchange"] == 21)].iloc[0][["Close", "TotalRet"]]
                    # (thing2["Exchange"] == 21)].iloc[0]["Close"]
        except IndexError:
            print("ERROR")
        data.append((file[-13:-5], histvol_STOXX, secpr_STOXX["Close"], secpr_STOXX["TotalRet"]))
        print("{} is complete.".format(file[-13:-5]))

    df = pd.DataFrame(data, columns=["Date", "HistVol", "Close", "TotalRet"])
    # df = pd.DataFrame(data, columns=["Date", "HistVol", "Close"])
    df = df.sort("Date").reset_index(drop=True)
    # df.to_csv("HistVolData.csv")

df = df.sort("Date").reset_index(drop=True)


df["Return"] = np.log(df["Close"]/df["Close"].shift())
df["Return"] = df["TotalRet"]
# window = 8

# df["R_bar_t"] = pd.rolling_mean(df.Return, window, min_periods=window)
"""Equivalent to 
df["R_bar_t"] = [df["Return"].iloc[k-9:k+1].mean() for k in df.index]
"""
# Total Return

df["s_t"] = pd.rolling_std(df.Return, window=window, min_periods=10)
""" Equivalent to
df["s_t"] = np.sqrt([sum((df["Return"].iloc[k-(window-1):k+1] -
    df["R_bar_t"].iloc[k])**2)/(window-1) for k in df.index])
    # df["Return"].iloc[k-(window-1):k+1].mean())**2) for k in df.index])
"""
df["s_zero_mean"] = np.sqrt([sum((df["Return"].iloc[k-(window-1):k+1]
    )**2)/(window-1) for k in df.index])

# Their return
df["Return"] = np.log(df["Close"]/df["Close"].shift())
df["std_t"] = pd.rolling_std(df.Return, window=window, min_periods=10)
df["std_zero_mean"] = np.sqrt([sum((df["Return"].iloc[k-(window-1):k+1]
    )**2)/(window-1) for k in df.index])

print df.head(20)

import matplotlib.pyplot as plt

plt.plot(df.index, df.s_t*np.sqrt(252), label = "Their Return")
plt.plot(df.index, df.s_zero_mean*np.sqrt(252), label = "Their Return, Zero Mean")
plt.plot(df.index, df.std_t*np.sqrt(252), label = "Only Our Calculations")
plt.plot(df.index, df.std_zero_mean*np.sqrt(252), label = "Only Our Calculations, Zero Mean")
plt.plot(df.index, df.HistVol, label="Historical Volatility")
plt.legend()
plt.show()





