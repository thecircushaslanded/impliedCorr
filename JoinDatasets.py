import glob
import os

import pandas as pd

data_loc = "/a/nas1-bt/space/if.udata/optionmetrics/"
data_loc2 = "/if/home/m1rab03/data/impliedCorr/"
program_loc = os.getcwd()

# Join optionmetrics datasets with weights
def join_datasets(index):
    """
    Joins weights data with the volatility data and
    names data from OptionMetrics.

    Parameters:
    -----------
    index: str
       'FTSE' or 'STOXX'.  Other indices must be
       added by changing the code below.
    """
    if index == "FTSE":
        FTSE = True
        STOXX = False
    elif index == "STOXX":
        FTSE = False
        STOXX = True
    else:
        raise Exception(ValueError)
    # Load the data.
    df = pd.read_csv(data_loc+"csv/Vol.csv")
    SECNM = pd.read_csv(data_loc+"csv/IVYSECNM.csv")
    SECNM.drop_duplicates(inplace=True)
    if STOXX:
        weights = pd.read_csv(data_loc2+"STOXX_weights_from_pdf.csv") 
    elif FTSE:
        weights = pd.read_csv(data_loc2+"FTSE_weights_from_pdf.csv")

    # Join the weights onto the name file, then onto the Optionmetrics file.
    baseline = len(weights.ISIN)
    temp = pd.merge(weights, SECNM, on=["ISIN"])
    check1 = len(temp.ISIN.unique())
    comb = pd.merge(temp, df, on=["SecurityID"])
    check2 = len(comb.ISIN.unique())

    if baseline == check1 == check2:
        pass
    else:
        m = set(weights.ISIN) - set(comb.ISIN.unique())
        if FTSE:
            """missing_weight = sum([weights[weights["ISIN"] == ISIN]["Weight"].values[
                0] for ISIN in m])
            comb["Weight"] = comb["Weight"]*10/(100-missing_weight)"""

            def new_weight(x):
                if sum(x.Weight) == 0:
                    tot = 1
                else:
                    tot = sum(x.Weight)
                return x.Weight/tot

            adj  = comb.groupby(["Date", "Days"]).apply(new_weight).reset_index()
        
            # adjust weights
            """adj  = comb.groupby(["Date", "Days"]).apply(lambda x: 
                    x.Weight/sum(x.Weight)).reset_index()"""
            adj = adj.set_index("level_2")
            adj = adj[["Weight"]]
            del comb["Weight"]
            comb = pd.merge(adj, comb, left_index=True, right_index=True)  
            print("Data was not available for {} firms.".format(len(m)))
            print("Weights were adjusted accordingly.")

        else:
            for k in list(m): print k
            raise Exception("Some firms were lost while merging data.")

    if STOXX:
        comb.to_csv(data_loc2+"STOXXCombinedData.csv", index=False)
    if FTSE:
        comb.to_csv(data_loc2+"FTSECombinedData.csv", index=False)

join_datasets("STOXX")
join_datasets("FTSE")

