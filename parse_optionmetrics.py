import os
import glob 
import zipfile
import fileinput
import datetime as dt
from subprocess import call

import numpy as np
import pandas as pd


# data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"
data_loc = "/if/udata/optionmetrics/"
program_loc = os.getcwd()

date = "20150731"
# index_ID = 504880
index_ID = None

def update_secnm(date):
    """
    Creates a new security name csv file.
    Security names don't change often.  
    This does not need to be used regularly, if at all.
    
    Parameters:
    -----------
    date: string
    """
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    secnm = pd.read_csv(zf.open("INTL.IVYSECNM.{}D.txt".format(date)), 
            sep='\t', header=None, names=[
        "SecurityID", "EffectiveDate", "VALOR", "Issuer", "SEDOL", "ISIN"])
    secnm = secnm[["SecurityID", "ISIN"]]
    secnm.to_csv(data_loc+"csv/IVYSECNM.csv", index=False)


def get_ivol(date):
    """
    Extracts implied volatility data for a given date.
    
    Also adds in column names, removes some columns, and
    filters the data to only include ATM options.

    Parameters:
    -----------
    date: string

    Returns:
    --------
    vsurf: Pandas dataframe
    """
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    vsurf = pd.read_csv(zf.open("INTL.IVYVSURF.{}D.txt".format(date)), 
            sep='\t', header=None, 
            names=[ "SecurityID", "Date", "Days", "Delta", "Flag", 
                "IVol", "IStrike", "IPrem", "Dispersion", "Curr"],
            na_values=["", "NA", "-99.99"], 
            usecols=["SecurityID", "Date", "Days", "Delta", "IVol"])
    vsurf = vsurf[(abs(vsurf["Delta"])==50)] # ATM options
    vsurf = vsurf.groupby(["Date", "SecurityID", "Days"]).mean().reset_index()
    return vsurf[["SecurityID", "Date", "Days", "IVol"]]

def get_histvol(date, index_ID):
    """
    Extracts historical volatility data for a given date.
    
    Also adds in column names and removes some columns.

    Parameters:
    -----------
    date: string

    Returns:
    --------
    histvol: Pandas dataframe
    """
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    histvol = pd.read_csv(zf.open("INTL.IVYHISTVOL.{}D.txt".format(date)), 
                sep='\t', header=None, 
                names=[ "SecurityID", "Date", "Days", "Currency", "Vol"], 
                na_values=["", "NA", "-99.99"], 
                usecols=["SecurityID", "Date", "Days", "Vol"])
    return histvol

def get_price(date, index_ID):
    """
    Extracts price data for a given date for STOXX and FTSE
    
    Also adds in column names and removes some columns.

    Parameters:
    -----------
    date: string

    Returns:
    --------
    secpr: Pandas dataframe
    """
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    secpr = pd.read_csv(zf.open("INTL.IVYSECPR.{}D.txt".format(date)), 
                sep='\t', header=None, names=[ "SecurityID", "Date", 
                    "Exchange", "Bid", "Ask", "High", "Low", "Open", "Close",
                    "TotalRet", "AskFactor", "CTotalRetFactor", "Currency", 
                    "Volume"], na_values=["", "NA", "-99.99"], 
                usecols=["SecurityID", "Date", "Close", "Exchange"])
    # Select the data we want
    # Choosing the exchange insures we have reliable price data from
    # a source with good liquidity.
    secpr_STOXX = secpr[(secpr["SecurityID"] == 504880) & 
            (secpr["Exchange"] == 21)] 
    secpr_FTSE = secpr[(secpr["SecurityID"] == 506528) & 
            (secpr["Exchange"] == 222)]
    secpr = pd.concat([secpr_STOXX, secpr_FTSE])
    return secpr[["SecurityID", "Date", "Close"]]

def CallOverPut(date):
    """
    Computes the ratio of calls over puts.

    Parameters:
    -----------
    date: string

    Returns:
    --------
    COP: Pandas dataframe
    """
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    thing = pd.read_csv(zf.open("INTL.IVYOPPRC."+date+"D.txt"), 
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
    COP = COP.reset_index()
    COP.columns = ["SecurityID", "CallOverPut"] # Open Interest
    COP["Date"] = dt.datetime.strptime(date, "%Y%m%d")
    return COP

os.chdir(data_loc+"raw_zip/")
file_no = 0
print("Beginning to process data")
files = glob.glob("INTL.IVYDB.*.zip")
files.sort()
update_secnm(files[-1][-13:-5]) # Optional step

for file in files:
    os.chdir(data_loc+"raw_zip")
    date = file[-13:-5]
    print("Processing data for {}-{}-{} ".format(date[:4], date[4:6], date[6:]))
    try:
        # The file might be empty, which is no use to us.
        if os.stat("../temp/Vol{}D.temp".format(date)).st_size < 1:
            redo=True
        else:
            redo=False
    except:
        redo=True
    if redo:
        print date
        i = get_ivol(date)
        r = get_histvol(date, index_ID)
        p = get_price(date, index_ID)

        os.chdir(data_loc+"temp/")
        ir = pd.merge(i, r, on=["Date", "Days", "SecurityID"])
        ir = ir[["SecurityID", "Date", "Days", "IVol", "Vol"]]
        ir.to_csv("Vol{}D.temp".format(date), 
                index=False, header=False)
        p.to_csv("Price{}D.temp".format(date), 
                index=False, header=False)
        if os.stat("Vol{}D.temp".format(date)).st_size < 1:
            print("DOUBLE BAZOOKA!") # Random message
            raw_input()
            i["Vol"] = np.nan
            i["Close"] = np.nan
            i = i[["SecurityID", "Date", "Days", "IVol", "Vol","Close"]]
            i.to_csv("Vol{}D.temp".format(date), 
                index=False, header=False)
            print(" Historical price and volatility data were missing.")
        os.chdir(data_loc+"raw_zip/")
    try:
        # The file might be empty, which is no use to us.
        if os.stat("../temp/CallOverPut{}D.temp".format(date)).st_size < 1:
            redo=True
        else:
            redo=False
    except:
        redo=True
    if redo:
        COP = CallOverPut(date)
        COP.to_csv(data_loc+"temp/CallOverPut{}D.temp".format(date), 
                index=False, header=False)
    # Display progress
    file_no+=1
    print(" {:.2f}% complete.  \n".format(file_no*100./len(files)))

print("Writing data to csv. This may take a long time.")
os.chdir(data_loc+"csv/")
with open("Vol.csv", 'w') as fout:
    fi = fileinput.input(files=glob.glob("../temp/Vol*.temp"))
    fout.write("SecurityID,Date,Days,IVol,HistVol\n")
    for line in fi:
        fout.write(line)
    fi.close()

with open("Price.csv", 'w') as fout:
    fi = fileinput.input(files=glob.glob("../temp/Price*.temp"))
    fout.write("SecurityID,Date,Close\n")
    for line in fi:
        fout.write(line)
    fi.close()

with open("CallOverPut.csv", 'w') as fout:
    fi = fileinput.input(files=glob.glob("../temp/CallOverPut*.temp"))
    fout.write("SecurityID,CallOverPut,Date\n")
    for line in fi:
        fout.write(line)
    fi.close()
os.chdir(program_loc)
print("Optionmetrics data is ready to use.")


