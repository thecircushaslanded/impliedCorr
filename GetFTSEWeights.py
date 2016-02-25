import os
from subprocess import call

import pandas as pd

data_loc2 = "/lcl/if/home/m1rab03/data/impliedCorr/"
program_loc = os.getcwd()

print("Go to http://www.ftse.com/analytics/factsheets/Home/ConstituentsWeights",
        "Download the FTSE 100 datasheet and save it as FTSE100.pdf in",
        "  the  {}".format(data_loc2),
        " directory; then press enter to continue.")
raw_input()

os.chdir(data_loc2)
call(["pdftotext", "FTSE100.pdf", "FTSE100.txt"])
os.chdir(program_loc)
with open(data_loc2+"FTSE100.txt", 'r') as fi:
    ll = fi.readlines()

ll = [l for l in ll if l != '\n']
ll = ll[ll.index("Constituent\n")+1: ll.index("1 of 2\n")]
ll = [l for l in ll if l != "UNITED\n"]
ll = [l for l in ll if l != "KINGDOM\n"]
ll.pop(ll.index("Index weight\n"))
ll.pop(ll.index("(%)\n"))
ll.pop(ll.index("Source: FTSE Group\n"))
ll.pop(ll.index("Country\n"))
ll.pop(ll.index("Constituent\n"))
ll.pop(ll.index("(%)\n"))
ll.pop(ll.index("Group\n"))
ll.pop(ll.index("Country\n"))
ll.pop(ll.index("Constituent\n"))
ll.pop(ll.index("Index weight\n"))
ll.pop(ll.index("(%)\n"))
ll.pop(ll.index("Index weight\n"))

ll.pop(ll.index("Country\n"))


weights = []
names = []
for l in ll:
    try:
        weights.append(float(l))
    except:
        names.append(l[:-1])


weight_df = pd.DataFrame(zip(names, weights), columns=["Name", "Weight"])


name_to_ISIN = pd.read_csv(data_loc2+"NameToISIN_FTSE.csv")

df = pd.merge(weight_df, name_to_ISIN)
df.loc[len(weights)] = (["FTSE 100", 0, "GB0001383545"])


if len(set(names) - set(df.Name)) > 0:
    missing = set(names) - set(df.Name)
    for name in missing:
        print("{} is missing from NameToISIN.csv".format(name))
    raise Exception("NameToISIN is missing {} entries.".format(len(missing)))

df.to_csv(data_loc2+"FTSE_weights_from_pdf.csv", index=False)



