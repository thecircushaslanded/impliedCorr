import os
import zipfile
import fileinput
import datetime as dt
from glob import glob

import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.palettes import Spectral4

data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"

dfs = pd.read_csv(data_loc+"csv/CallOverPut.csv")


def make_graph(index, id):
    df = dfs[dfs["SecurityID"]==id][["Date", "CallOverPut"]] 
    df = df.sort_values(by="Date")
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
