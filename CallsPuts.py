from glob import glob
import datetime as dt
import zipfile
import pickle as pkl

import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.palettes import Spectral4

data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"


# Load the data.
try:
    1/0
    dfs = pkl.load(open("CallsAndPuts.pkl", 'r'))
except:
    police = []
    for file in glob(data_loc+"INTL.*zip"):
        zf = zipfile.ZipFile(file)
        thing = pd.read_csv(zf.open("INTL.IVYOPPRC."+file[-13:-4]+".txt"), 
                delimiter='\t', names=["SecurityID", "Date", "OptionID", "Exchange",
                "Currency", "Bid", "BidTime", "BidUnderlying", "Ask", "AskTime", 
                "AskUnderlying", "Last", "LastTime", "LastUnderlying", "IVol",
                "Delta", "Gamma", "Vega", "Theta", "CalcPrice", "Volume", 
                "OpenInterest", "SpecialSettlement", "ReferenceExchange"],
                na_values=[-99.99],
                usecols=["SecurityID", "Delta", "Volume"]) # Open interest
        thing.dropna(inplace=True)
        thing["CallPut"] = thing["Delta"] > 0
        del thing["Delta"]
        newthing = thing.groupby(["SecurityID", "CallPut"]).sum().reset_index()
        def lx(x):
            try:
                return  (x[x["CallPut"]==True]["Volume"].values*1./
                x[x["CallPut"]==False]["Volume"].values).tolist()[0]
            except IndexError:
                return None
        COP = newthing.groupby("SecurityID").apply(lambda x: lx(x))
        police.append((file[-13:-5], COP))
        print("{} is complete.".format(file[-13:-5]))


    def f(e):
        mdf = e[1].reset_index()
        mdf.columns = ["SecurityID", "CallOverPut"] # Open Interest
        mdf["Date"] = dt.datetime.strptime(e[0], "%Y%m%d")
        return mdf

    dfs = pd.concat([f(e) for e in police])
    # print("writing data")
    # pkl.dump(dfs, open("CallsAndPuts.pkl", 'w'))




def make_graph(index, id):
    df = dfs[dfs["SecurityID"]==id][["Date", "CallOverPut"]] 
    df = df.sort(columns="Date")
    output_file(index+".html")
    p = figure(title="Call over Put - "+index, x_axis_type="datetime", 
            plot_width=800, toolbar_location='left')
    p.line(df["Date"], df["CallOverPut"], color=Spectral4[0])
    p.line(df["Date"], pd.rolling_mean(df["CallOverPut"], 10), color=Spectral4[3])
    script, div = components(p)
    with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
            index+"_CallsOverPuts_div.html", 'w') as f:
        f.write(div)
    with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
            index+"_CallsOverPuts_script.html", 'w') as f:
        f.write(script)
    show(p)

make_graph("STOXX", 504880)
make_graph("FTSE", 506528)
make_graph("CAC", 506497)
make_graph("DAX", 506496)

"""secpr = []
for file in glob(data_loc+"INTL.*zip"):
    zf = zipfile.ZipFile(file)
    thing = pd.read_csv(zf.open("INTL.IVYSECPR."+file[-13:-4]+".txt"), 
            sep='\t', header=False, names=[ "SecurityID", "Date", "Exchange", 
                "Bid", "Ask", "High", "Low", "Open", "Close", "TotalRet", 
                "AskFactor", "CTotalRetFactor", "Currency", "Volume"], 
            na_values=["", "NA", "-99.99"], 
            usecols=["SecurityID", "Date", "Close", "Exchange"])
    # Select the data we want
    secpr_STOXX = thing[(thing["SecurityID"] == 504880) & 
            (thing["Exchange"] == 21)]
    secpr_FTSE = thing[(thing["SecurityID"] == 506528) & 
            (thing["Exchange"] == 222)]
    secpr_CAC  = thing[(thing["SecurityID"] ==506497) & 
            (thing["Exchange"] == 26)] # Not sure about this one
    secpr_DAX  = thing[(thing["SecurityID"] ==506496) & 
            (thing["Exchange"] == 21)] # Not sure about this one
    secpr.append((secpr_STOXX["Close"].values, secpr_FTSE["Close"].values,
        secpr_CAC["Close"].values, secpr_DAX["Close"].values))"""


"""# Price data frame
pdf = pd.read_csv(data_loc+"Price.csv")
pdf = pdf[pdf["SecurityID"] == SecurityID]
pdf = pdf.sort(columns="Date")
pdf["Date"] = map(lambda x: dt.datetime.strptime(str(x), "%Y%m%d"), 
        pdf.Date)
price_graph = figure(title="Price History", 
        x_axis_type='datetime', plot_width=800, plot_height=275)
price_graph.line(pdf["Date"], pdf["Close"], legend="Closing Price", 
        line_width=2, color=Spectral4[0])
price_graph.legend.orientation = "top_left"
price_graph.xgrid[0].ticker.desired_num_ticks = 12
show(price_graph)"""
