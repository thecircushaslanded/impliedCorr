import datetime as dt
from itertools import permutations

import pandas as pd


data_loc2 = ""

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


    idx = df[df["Weight"] == 0].copy()
    idx.loc[:,"s2"] = idx[vol]**2
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

