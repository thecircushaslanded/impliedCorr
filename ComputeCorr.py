import datetime as dt
from itertools import permutations

import pandas as pd
from bokeh.io import gridplot, vplot, output_file, show
from bokeh.plotting import figure
from bokeh.palettes import Spectral4
from bokeh.embed import components


data_loc2 = "/if/home/m1rab03/data/impliedCorr/"
data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"

def compute_corr(index, n_days, corr_type="implied"):
    """
    This reads in the data, and creates a dataframe with the
    computed correlation for options with the selected maturity (n_days).

    if vol == "IVol", the implied correlation will be computed.
    if vol == "HistVol", the realized correlation will be computed.

    """
    if corr_type == "implied":
        vol = "IVol"
    elif corr_type == "realized":
        vol = "HistVol"
    else:
        print corr_type
        raise Exception("Value specified is not a valid option.")
    df = pd.read_csv(data_loc2+index+"CombinedData.csv")
    # remove na rows ?
    df = df.dropna()

    denominator = df[["Date", vol,  "Weight", "Days"]].groupby(["Date", "Days"]
            ).apply(lambda group: sum([a[0]*a[1] for a in permutations(
                group[vol]*group["Weight"],2)])).reset_index()
    denominator.rename(columns={0:"denominator"}, inplace=True)


    w2s2 = df[["Date", vol, "Weight", "Days"]].groupby(["Date", "Days"]
            ).apply(lambda group: sum(group["Weight"]**2 * group[vol]**2)
            ).reset_index()
    w2s2.rename(columns={0:"w2s2"}, inplace=True)


    idx = df[df["Weight"] == 0]
    idx["s2"] = idx[vol]**2
    idx.rename(columns={vol:"idx_"+vol}, inplace=True)
    if vol == "IVol":
        idx = idx[["Date", "Days", "s2", "idx_IVol", "HistVol"]]
    if vol == "HistVol":
        idx = idx[["Date", "Days", "s2", "idx_HistVol"]]


    average_ivol = df[["Date", "IVol", "Days"]].groupby(["Date", "Days"]).mean(
            ).reset_index()
    average_ivol.rename(columns={"IVol":"average_IVol"}, inplace=True)


    result = pd.merge(denominator, w2s2, on=["Date", "Days"])
    result = pd.merge(result, idx, on=["Date", "Days"])
    result = pd.merge(result, average_ivol, on=["Date", "Days"])
    result["corr"] = (result["s2"] - result["w2s2"]) / result["denominator"]

    del result["s2"]
    del result["w2s2"]
    del result["denominator"]
    # result.to_csv(data_loc2+"ImpliedCorr.csv")
    result["Date"] = map(lambda x: dt.datetime.strptime(str(x), "%Y%m%d"), 
            result.Date)


    sel = result[result["Days"] == n_days]
    sel = sel.dropna().reset_index()
    return sel

def v_graph(index, sel_implied, sel_realized):
    output_file("VGraph.html")
    p = figure(title="ATM Volatility (3 Month)", 
            x_axis_type='datetime', plot_width=800, plot_height=500)
    p.line(sel_implied["Date"], sel_implied["idx_IVol"], 
            legend="Implied Volatility", line_width=2, color=Spectral4[0])
    """p.line(sel["Date"], sel["average_IVol"], 
            legend="Average IVol of Constituents", 
            line_width=2, color=Spectral4[1])"""
    p.line(sel_implied["Date"], sel_realized["idx_HistVol"], 
            legend="Realized Volatility", line_width=2, color=Spectral4[1])
    p.legend.orientation = "top_left"
    p.xgrid[0].ticker.desired_num_ticks = 13
    return p

def p_graph(index, v):
    output_file("PriceGraph.html")
    if index == "STOXX":
        SecurityID = 504880
    elif index == "FTSE":
        SecurityID = 506528
    elif index == "CAC":
        SecurityID = 506497
    else:
        print index
        raise Exception("Value specified is not a valid option.")
    pdf = pd.read_csv(data_loc+"Price.csv")
    pdf = pdf[pdf["SecurityID"] == SecurityID]
    pdf = pdf.sort(columns="Date")
    pdf["Date"] = map(lambda x: dt.datetime.strptime(str(x), "%Y%m%d"), 
            pdf.Date)
    p = figure(title="Price History", 
            x_axis_type='datetime', plot_width=800, plot_height=275,
            x_range=v.x_range)
    p.line(pdf["Date"], pdf["Close"], legend="Closing Price", 
            line_width=2, color=Spectral4[0])
    p.legend.orientation = "top_left"
    p.xgrid[0].ticker.desired_num_ticks = 12
    return p

def c_graph(index, sel_implied, sel_realized, v):
    output_file("CorrGraph.html")
    c2 = figure(title=index+"\nCorrelation",
            x_axis_type='datetime', plot_width=800, plot_height=275,
            x_range=v.x_range)
    c2.line(sel_implied["Date"], sel_implied["corr"], 
            legend="Implied Correlation", line_width=2, color=Spectral4[1])
    """c2.line(sel_realized["Date"], sel_realized["corr"], 
            legend="Realized Correlation", line_width=2, color=Spectral4[2])"""
    c2.legend.orientation = "top_left"
    c2.xgrid[0].ticker.desired_num_ticks = 12
    return c2

index = "FTSE"
sel = compute_corr(index, 91)
sel_realized = compute_corr(index, 91, corr_type="realized")
v = v_graph(index, sel, sel_realized)
p = p_graph(index, v)
c = c_graph(index, sel, sel_realized, v)

output_file(index+"Summary.html")

g = gridplot([[c], [v], [p]], toolbar_location='left')
script, div = components(g)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_div.html", 'w') as f:
    f.write(div)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_script.html", 'w') as f:
    f.write(script)

show(g)

index = "STOXX"
sel = compute_corr(index, 91)
sel_realized = compute_corr(index, 91, corr_type="realized")
sel_realized = sel_realized[sel_realized["corr"] < 2]
sel= sel[sel["corr"] < 2]
v = v_graph(index, sel, sel_realized)
p = p_graph(index, v)
c = c_graph(index, sel, sel_realized, v)

output_file(index+"Summary.html")

g = gridplot([[c], [v], [p]], toolbar_location='left')
script, div = components(g)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_div.html", 'w') as f:
    f.write(div)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_script.html", 'w') as f:
    f.write(script)

show(g)

