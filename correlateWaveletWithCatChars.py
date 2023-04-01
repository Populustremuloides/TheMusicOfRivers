import pandas as pd
from scipy.stats import spearmanr
import numpy as np
import os
import matplotlib.pyplot as plt
import tqdm

df1 = pd.read_csv("universallyAligned_powers.csv", encoding="latin-1")

newCols = []
for col in df1.columns:
    newCols.append(str(col)[1:])
oldToNew = dict(zip(list(df1.columns), newCols))
df1 = df1.rename(oldToNew, axis=1)


df2 = pd.read_csv("alldata_hemisphereCorrected.csv", encoding="latin-1")
df2 = df2[df2.columns[1:]]

newCats = []
for cat in df2["grdc_no"]:
    try:
        newCats.append(str(int(float(cat))))
    except:
        newCats.append(None)

df2["grdc_no"] = newCats

#df1 = df1.drop(df1.columns[0], axis=1)
df2 = df2.drop(df2.columns[0], axis=1)

cols = list(df1.columns)
cols[0] = "grdc_no"
df1 = df1.transpose()

cols = list(df1.iloc[0])
df1.columns = cols#df1.iloc[0]
df1 = df1.iloc[1:]
df1["grdc_no"] = list(df1.index)

df = df2.merge(df1, on="grdc_no")

#print(df1)
#print(df2)

for index, col in enumerate(df.columns):
    print(index, col)

upperBound = 1419
# 318 - 5980
# 198 - 317
loop = tqdm.tqdm(total=(311-198) * (upperBound - 318))
dataDict = {}
for index1 in range(198, 311):
    dataDict[df.columns[index1]] = []
    for index2 in range(318, upperBound):

        data1 = df[df.columns[index1]]
        data2 = df[df.columns[index2]]

        mask1 = np.array(~data1.isna())
        mask2 = np.array(~data2.isna())
        mask = np.logical_and(mask1, mask2)

        data1 = np.array(data1)[mask]
        data2 = np.array(data2)[mask]

        corr, pVal = spearmanr(data1, data2)
        dataDict[df.columns[index1]].append(corr)
        loop.update()
loop.close()

outDf = pd.DataFrame.from_dict(dataDict)
outDf.index = df.columns[318:upperBound]
outDf.to_csv("correlations_between_wavelet_and_cat_chars.csv")

