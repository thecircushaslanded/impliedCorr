import os
import glob 
import zipfile
import fileinput
from subprocess import call

import numpy as np
import pandas as pd


data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"
program_loc = os.getcwd()

date = "20150731"
# index_ID = 504880
index_ID = None

def update_secnm(date):
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    secnm = pd.read_csv(zf.open("INTL.IVYSECNM.{}D.txt".format(date)), 
            sep='\t', header=False, names=[
        "SecurityID", "EffectiveDate", "VALOR", "Issuer", "SEDOL", "ISIN"])
    secnm = secnm[["SecurityID", "ISIN"]]
    secnm.to_csv(data_loc+"IVYSECNM.csv", index=False)


def get_ivol(date):
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    vsurf = pd.read_csv(zf.open("INTL.IVYVSURF.{}D.txt".format(date)), 
            sep='\t', header=False, names=[ "SecurityID", "Date", "Days", 
            "Delta", "Flag", "IVol", "IStrike", "IPrem", "Dispersion", "Curr"],
            na_values=["", "NA", "-99.99"], usecols=["SecurityID", "Date", 
                "Days", "Delta", "IVol"])
    # vsurf = vsurf[(vsurf["SecurityID"].isin(IDs)) & (abs(vsurf["Delta"])==50)]
    vsurf = vsurf[(abs(vsurf["Delta"])==50)]
    vsurf = vsurf.groupby(["Date", "SecurityID", "Days"]).mean().reset_index()
    return vsurf[["SecurityID", "Date", "Days", "IVol"]]

def get_histvol(date, index_ID):
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    histvol = pd.read_csv(zf.open("INTL.IVYHISTVOL.{}D.txt".format(date)), 
                sep='\t', header=False, names=[ "SecurityID", "Date", "Days", 
                "Currency", "Vol"], na_values=["", "NA", "-99.99"], 
                usecols=["SecurityID", "Date", "Days", "Vol"])
    # histvol = histvol[(histvol["SecurityID"] == index_ID)]
    # return histvol[["Date", "Days", "Vol"]]
    return histvol

def get_price(date, index_ID):
    zf = zipfile.ZipFile("INTL.IVYDB.{}D.zip".format(date))
    secpr = pd.read_csv(zf.open("INTL.IVYSECPR.{}D.txt".format(date)), 
                sep='\t', header=False, names=[ "SecurityID", "Date", 
                    "Exchange", "Bid", "Ask", "High", "Low", "Open", "Close",
                    "TotalRet", "AskFactor", "CTotalRetFactor", "Currency", 
                    "Volume"], na_values=["", "NA", "-99.99"], 
                usecols=["SecurityID", "Date", "Close", "Exchange"])
    # Select the data we want
    # secpr = secpr[(secpr["SecurityID"] == index_ID) & (secpr["Exchange"] == 21)]
    secpr_STOXX = secpr[(secpr["SecurityID"] == 504880) & 
            (secpr["Exchange"] == 21)]
    secpr_FTSE = secpr[(secpr["SecurityID"] == 506528) & 
            (secpr["Exchange"] == 222)]
    secpr = pd.concat([secpr_STOXX, secpr_FTSE])
    return secpr[["SecurityID", "Date", "Close"]]


os.chdir(data_loc)
file_no = 0
print("Beginning to process data")
files = glob.glob("INTL.IVYDB.*.zip")
files.sort()
update_secnm(files[-1][-13:-5])
for file in files:
    date = file[-13:-5]
    print("Processing data for {}-{}-{} ".format(date[:4], date[4:6], date[6:]))
    try:
        # The file might be empty, which is no use to us.
        if os.stat("Selection{}D.temp".format(date)).st_size < 1:
            redo=True
        else:
            redo=False
    except:
        redo=True
    if redo:
        i = get_ivol(date)
        r = get_histvol(date, index_ID)
        p = get_price(date, index_ID)
        ir = pd.merge(i, r, on=["Date", "Days", "SecurityID"])
        # irp = pd.merge(ir, p, on=["Date", "SecurityID"])
        # irp = irp[["SecurityID", "Date", "Days", "IVol", "Vol","Close"]]
        ir = ir[["SecurityID", "Date", "Days", "IVol", "Vol"]]
        ir.to_csv("Selection{}D.temp".format(date), 
                index=False, header=False)
        p.to_csv("Price{}D.temp".format(date), 
                index=False, header=False)
        if os.stat("Selection{}D.temp".format(date)).st_size < 1:
            print("DOUBLE BAZOOKA!")
            raw_input()
            i["Vol"] = np.nan
            i["Close"] = np.nan
            i = i[["SecurityID", "Date", "Days", "IVol", "Vol","Close"]]
            i.to_csv("Selection{}D.temp".format(date), 
                index=False, header=False)
            print(" Historical price and volatility data were missing.")
            # raw_input()
    # Display progress
    file_no+=1
    print(" {:.2f}% complete.  \n".format(file_no*100./len(files)))

print("Writing data to Selection.csv")
with open("Selection.csv", 'w') as fout:
    fi = fileinput.input(files=glob.glob("Selection*.temp"))
    fout.write("SecurityID,Date,Days,IVol,HistVol\n")
    for line in fi:
        fout.write(line)
    fi.close()

with open("Price.csv", 'w') as fout:
    fi = fileinput.input(files=glob.glob("Price*.temp"))
    fout.write("SecurityID,Date,Close\n")
    for line in fi:
        fout.write(line)
    fi.close()
os.chdir(program_loc)
print("Optionmetrics data is ready to use.")


