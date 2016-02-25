import glob
import os

import pandas as pd

dates = glob.glob("/a/nas1-bt/space/rsma.markit_sf/src/20*am")
dates = glob.glob("/rsma/markit_sf/src/20*am")

dates = [date for date in dates if date[-10:-4] == "201510"]
program_dir = os.getcwd()

dfs = []

for date in dates:
    print date
    positions = pd.read_csv(glob.glob(date+"/*PositionsUSD.tsv.gz")[0], 
            delimiter='\t')
    inventory = pd.read_csv(glob.glob(date+"/*InventoryUSD.tsv.gz")[0], 
            delimiter='\t')
    characteristics = pd.read_csv(glob.glob(date+"/*CharsLkUp.tsv.gz")[0], 
            delimiter='\t')
    """currencies = pd.read_csv(glob.glob(date+"/*Currencies.tsv.gz")[0], 
            delimiter='\t')"""
    instruments = pd.read_csv(glob.glob(date+"/*Instruments.tsv.gz")[0], 
            delimiter='\t', usecols=["InstrumentID", "ISIN", "FullDescription"])

    # We should check to be sure that we don't have multiple IDs mapping
    # to a single ISIN that we are interested in.
    """df = pd.merge(positions, instruments, 
            left_on=["InstrumentId"], right_on=["InstrumentID"])
    df = pd.merge(df, characteristics)"""

    quantity = positions[["InstrumentId", "Quantity"]].groupby("InstrumentId"
            ).sum().reset_index()
    quantity.columns = ["InstrumentId", "LoanQuantity"]

    df = pd.merge(inventory, instruments, 
            left_on=["InstrumentId"], right_on=["InstrumentID"])
    df = pd.merge(df, characteristics)
    df = pd.merge(df, quantity)
    df["date"] = date[-10:-2]


    df["first_two"] = map(lambda x: str(x)[:2], df.ISIN)
    df["has_percent"] = map(lambda x: str(x).find("%")>0, df.FullDescription)
    df = df[(df.FiscalLocation == "FR") & (df.first_two == "FR") & (~df.has_percent)]

    del df["has_percent"]
    del df["first_two"]
    dfs.append(df)

result = pd.concat(dfs)
result.to_csv("Oct2015.csv", index=False)
