from glob import glob
import time
import zipfile

import pandas as pd

data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"
data_loc = "/if/home/m1rab03/data/optionmetrics/"
output_loc = "/a/nas1-bt/space/if.udata/optionmetrics/temp/"

# STOXX 50, CAC 40, HSBC, SANOFI, BAYER
# market_security_ids = [504880, 998033, 411161, 699381, 10367293]
market_security_ids = [504880, 506497,  501988, 503861, 718015]

for file in glob(data_loc+"INTL.IVYDB.201501*D.zip"):
    print(file)
    start = time.time()
    zf = zipfile.ZipFile(file)
    date = file[-13:-5]
    secur = pd.read_csv(zf.open("INTL.IVYSECUR.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "VALOR", "Country", "Optionable", 
                    "IssueType", "DividendConvention"])
    secur = secur[(secur["SecurityID"].isin(market_security_ids))]

    secnm = pd.read_csv(zf.open("INTL.IVYSECNM.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "EffectiveDate", "VALOR", "Issuer", 
                    "SEDOL", "ISIN"])
    secnm = secnm[(secnm["SecurityID"].isin(market_security_ids))]
    distr = pd.read_csv(zf.open("INTL.IVYDISTR.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "RecordDate", "SequenceNumber", 
                    "Exate", "Amount", "AdjustmentFactor", "DeclareDate", 
                    "PaymentDate", "LinkSecurityID", "DistributionType", 
                    "Frequency", "Currency"])
    distr = distr[(distr["SecurityID"].isin(market_security_ids))]
    distrproj = pd.read_csv(zf.open("INTL.IVYDISTRPROJ.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "RunDate", "Exdate", "Yield"])
    distrproj = distrproj[(distrproj["SecurityID"].isin(market_security_ids))]
    secpr = pd.read_csv(zf.open("INTL.IVYSECPR.{}D.txt".format(date)), 
                sep='\t', header=False, names=[ "SecurityID", "Date", 
                    "Exchange", "Bid", "Ask", "High", "Low", "Open", "Close",
                    "TotalRet", "AskFactor", "CTotalRetFactor", "Currency", 
                    "Volume"], na_values=["", "NA", "-99.99"])
    secpr = secpr[(secpr["SecurityID"].isin(market_security_ids))]
    opinf = pd.read_csv(zf.open("INTL.IVYOPINF.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "OptionID", "Exchange", "Description", 
                    "Currency", "Strike", "Expiration", "CallPut", 
                    "UnderlyingValor", "ContractSize", "OptionStyle", 
                    "Version", "ExerciseStyle"])
    opinf = opinf[(opinf["SecurityID"].isin(market_security_ids))]
    ophst = pd.read_csv(zf.open("INTL.IVYOPHST.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "OptionID", "Exchange", "Description", 
                    "Currency", "Strike", "Expiration", "CallPut", 
                    "UnderlyingValor", "ContractSize", "OptionStyle", 
                    "Version", "ExerciseStyle", "StartDate"])
    ophst = ophst[(ophst["SecurityID"].isin(market_security_ids))]
    opprc = pd.read_csv(zf.open("INTL.IVYOPPRC.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "Date", "OptionID", "Exchange", 
                    "Currency", "Bid", "BidTime", "UnderlyingBid", "Ask", 
                    "AskTime", "UnderlyingAsk", "Last", "LastTime", 
                    "UnderlyingLast", "ImpliedVolatility", "Delta", "Gamma", 
                    "Vega", "Theta", "CalculationPrice", "Volume", 
                    "OpenInterest", "SpecialSettlement", "ReferenceExchange"])
    opprc = opprc[(opprc["SecurityID"].isin(market_security_ids))]
    zeroc = pd.read_csv(zf.open("INTL.IVYZEROC.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["CurrencyCode", "Date", "Days", "Rate"])
    idxdv = pd.read_csv(zf.open("INTL.IVYIDXDV.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "Date", "Expiration", "Rate"])
    idxdv = idxdv[(idxdv["SecurityID"].isin(market_security_ids))]
    vsurf = pd.read_csv(zf.open("INTL.IVYVSURF.{}D.txt".format(date)), 
            sep='\t', header=False, names=["SecurityID", "Date", "Days", 
            "Delta", "Flag", "IVol", "IStrike", "IPrem", "Dispersion", "Curr"],
            na_values=["", "NA", "-99.99"])
    vsurf = vsurf[(vsurf["SecurityID"].isin(market_security_ids))]
    stdop = pd.read_csv(zf.open("INTL.IVYSTDOP.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "Date", "Days", "ForwardPrice", 
                    "StrikePrice", "CallPutFlag", "Premium",
                    "ImpliedVolatility", "Delta", "Gamma", "Vega", 
                    "Theta", "Currency"])
    stdop = stdop[(stdop["SecurityID"].isin(market_security_ids))]
    histvol = pd.read_csv(zf.open("INTL.IVYHISTVOL.{}D.txt".format(date)), 
                sep='\t', header=False, names=[ "SecurityID", "Date", "Days", 
                "Currency", "Vol"], na_values=["", "NA", "-99.99"])
    histvol = histvol[(histvol["SecurityID"].isin(market_security_ids))]
    exchng = pd.read_csv(zf.open("INTL.IVYEXCHNG.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["ExchangeCode", "Symbol", "Country", "Name"])
    currency = pd.read_csv(zf.open("INTL.IVYCURRENCY.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["CurrencyCode", "Symbol", "Name"])
    country = pd.read_csv(zf.open("INTL.IVYCOUNTRY.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["CountryCode", "CountryName"])
    ticker = pd.read_csv(zf.open("INTL.IVYTICKER.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "Exchange", "EffectiveDate", "Ticker"])
    ticker = ticker[(ticker["SecurityID"].isin(market_security_ids))]
    future = pd.read_csv(zf.open("INTL.IVYFUTURE.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "FutureID", "Exchange", "Description", 
                    "Currency", "Expiration", "UnderlyingValor"])
    future = future[(future["SecurityID"].isin(market_security_ids))]
    futprc = pd.read_csv(zf.open("INTL.IVYFUTPRC.{}D.txt".format(date)), 
                na_values=["", "NA", "-99.99"], sep='\t', header=False, 
                names=["SecurityID", "Date", "FutureID", "Exchange",
                    "Currency", "ClosePrice", "Volume"])
    futprc = futprc[(futprc["SecurityID"].isin(market_security_ids))]
    mid = time.time()
    print("Writing files to output. {} ".format(mid-start))
    for df, name in zip([secur, secnm, distr, distrproj, secpr, opinf, ophst, 
        opprc, zeroc, idxdv, vsurf, stdop, histvol, exchng, currency, country, 
        ticker, future, futprc], ["secur", "secnm", "distr", "distrproj", 
            "secpr", "opinf", "ophst", "opprc", "zeroc", "idxdv", "vsurf", 
            "stdop", "histvol", "exchng", "currency", "country", "ticker", 
            "future", "futprc"]):
        df.to_csv(output_loc+name+date+".csv")
    print("Finished. Total time: {} ".format(time.time()-start))


