import os
from subprocess import call

import pandas as pd

data_loc = "/lcl/data/scratch/m1rab03/impliedCorr/"
program_loc = os.getcwd()

print("Save http://www.stoxx.com/document/Bookmarks/CurrentComponents/SX5GT.pdf"
        "\n as SX5GT.pdf in the {} directory, then press enter.".format(
            data_loc))
raw_input()
os.chdir(data_loc)
call(["pdftotext", "SX5GT.pdf", "SX5GT.txt"])

with open("SX5GT.txt", 'r') as fi:
    lines = fi.readlines()
os.chdir(program_loc)

names = [name[:-1] for name in lines[8:8+50]]
weights = [float(x)/100. for x in lines[167:-2]]
print("Weights sum to {}".format(sum(weights)))
weight_df = pd.DataFrame(zip(names, weights), columns=["Name", "Weight"])

name_to_ISIN = pd.read_csv(data_loc+"NameToISIN_STOXX.csv")

df = pd.merge(weight_df, name_to_ISIN)
df.loc[len(weights)] = (["EURO STOXX 50 INDEX", 0, "EU0009658145"])


if len(set(names) - set(df.Name)) > 0:
    missing = set(names) - set(df.Name)
    for name in missing:
        print("{} is missing from NameToISIN.csv".format(name))
    raise Exception("NameToISIN is missing {} entries.".format(len(missing)))

df.to_csv(data_loc+"STOXX_weights_from_pdf.csv", index=False)


