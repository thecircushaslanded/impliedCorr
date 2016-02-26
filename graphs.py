import datetime as dt

import pandas as pd
from bokeh.io import gridplot, vplot, output_file, show
from bokeh.plotting import figure
from bokeh.palettes import Spectral4
from bokeh.embed import components

from ComputeCorr import compute_corr


data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"
data_loc2 = "/if/home/m1rab03/data/impliedCorr/"

plot_width = 1200

def cop_graph(index):
    """
    Make a graph of calls over puts
    """
    output_file(index+".html")
    if index=="STOXX":
        id = 504880
    elif index=="FTSE":
        id = 506528
    elif index=="CAC":
        id = 506497
    elif index=="DAX":
        id = 506496
    else:
        raise Exception(ValueError)
    dfs = pd.read_csv(data_loc+"csv/CallOverPut.csv")
    dfs["Date"] = dfs.Date.apply(lambda x: 
            dt.datetime.strptime(str(x), "%Y-%m-%d"))
    df = dfs[dfs["SecurityID"]==id][["Date", "CallOverPut"]] 
    df = df.sort_values("Date")
    p = figure(title="Call Over Put - "+index, 
            x_axis_type="datetime", 
            plot_width=plot_width, 
            toolbar_location='left')
    p.line(df["Date"], df["CallOverPut"], color=Spectral4[0])
    p.line(df["Date"], pd.rolling_mean(df["CallOverPut"], 10), color=Spectral4[3])
    p.legend.location = "top_left"
    p.xgrid[0].ticker.desired_num_ticks = 13
    """script, div = components(p)
    with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
            index+"_CallsOverPuts_div.html", 'w') as f:
        f.write(div)
    with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
            index+"_CallsOverPuts_script.html", 'w') as f:
        f.write(script)"""
    return p

def v_graph(index, sel_implied, sel_realized, x):
    output_file("VGraph.html")
    p = figure(title="ATM Volatility (3 Month)", 
            x_axis_type='datetime', 
            plot_width=plot_width, plot_height=500,
            x_range=x.x_range)
    p.line(sel_implied["Date"], sel_implied["idx_IVol"], 
            legend="Implied Volatility", line_width=2, color=Spectral4[0])
    """p.line(sel["Date"], sel["average_IVol"], 
            legend="Average IVol of Constituents", 
            line_width=2, color=Spectral4[1])"""
    p.line(sel_implied["Date"], sel_realized["idx_HistVol"], 
            legend="Realized Volatility", line_width=2, color=Spectral4[1])
    p.legend.location = "top_left"
    p.xgrid[0].ticker.desired_num_ticks = 13
    return p

def p_graph(index, x):
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
    pdf = pd.read_csv(data_loc+"csv/Price.csv")
    pdf = pdf[pdf["SecurityID"] == SecurityID]
    pdf = pdf.sort_values(by="Date")
    pdf["Date"] = map(lambda x: dt.datetime.strptime(str(x), "%Y%m%d"), 
            pdf.Date)
    p = figure(title="Price History", 
            x_axis_type='datetime', plot_width=plot_width, plot_height=275,
            x_range=x.x_range)
    p.line(pdf["Date"], pdf["Close"], legend="Closing Price", 
            line_width=2, color=Spectral4[0])
    p.legend.location = "top_left"
    p.xgrid[0].ticker.desired_num_ticks = 12
    return p

def c_graph(index, sel_implied, sel_realized, x):
    output_file("CorrGraph.html")
    c2 = figure(title=index+"\nCorrelation",
            x_axis_type='datetime', plot_width=plot_width, plot_height=275,
            x_range=x.x_range)
    c2.line(sel_implied["Date"], sel_implied["corr"], 
            legend="Implied Correlation", line_width=2, color=Spectral4[1])
    """c2.line(sel_realized["Date"], sel_realized["corr"], 
            legend="Realized Correlation", line_width=2, color=Spectral4[2])"""
    c2.legend.location = "top_left"
    c2.xgrid[0].ticker.desired_num_ticks = 12
    return c2



# By index
index = "FTSE"
sel = compute_corr(index, 91)
sel_realized = compute_corr(index, 91, corr_type="realized")
cop = cop_graph(index)
v = v_graph(index, sel, sel_realized, cop)
p = p_graph(index, cop)
c = c_graph(index, sel, sel_realized, cop)

output_file(index+"Summary.html")

g = gridplot([[c], [v], [p], [cop]], toolbar_location='left')
script, div = components(g)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_div.html", 'w') as f:
    f.write(div)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_script.html", 'w') as f:
    f.write(script)

# show(g)


index = "STOXX"
sel = compute_corr(index, 91)
sel_realized = compute_corr(index, 91, corr_type="realized")
sel_realized = sel_realized[sel_realized["corr"] < 2]
sel= sel[sel["corr"] < 2]
cop = cop_graph(index)
v = v_graph(index, sel, sel_realized, cop)
p = p_graph(index, cop)
c = c_graph(index, sel, sel_realized, cop)

output_file(index+"Summary.html")

g = gridplot([[c], [v], [p], [cop]], toolbar_location='left')
script, div = components(g)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_div.html", 'w') as f:
    f.write(div)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_script.html", 'w') as f:
    f.write(script)

# show(g)


index = "CAC"
cop = cop_graph(index)

output_file(index+"Summary.html")

g = gridplot([[cop]], toolbar_location='left')
script, div = components(g)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_div.html", 'w') as f:
    f.write(div)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_script.html", 'w') as f:
    f.write(script)

# show(g)


index = "DAX"
cop = cop_graph(index)

output_file(index+"Summary.html")

g = gridplot([[cop]], toolbar_location='left')
script, div = components(g)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_div.html", 'w') as f:
    f.write(div)
with open("/lcl/if/appl/www/php/fm/GCM_files/LiquidityAndCorr/"+
        index+"_summary_script.html", 'w') as f:
    f.write(script)

# show(g)


