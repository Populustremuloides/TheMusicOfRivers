import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import spearmanr
import numpy as np

from tqdm import tqdm

df = pd.read_csv("glob_flow_fourier_decomposition_blackman_mini.csv")
#df = df.drop(df.columns[0], axis=1)

# figure out where the nans get really bad
#for index, row in df.iterrows():
#    print(index, np.sum(row.isna()))

#df = df.iloc[:274]
#df = df[1:]

#periods = df[df.columns[0]].to_numpy()
#periods = np.flip(periods)
#df[df.columns[0]] = periods

for col in df.columns:
    df[col] = np.abs(df[col])

correlations = {}

loop = tqdm(total= len(df) ** 2)
for index1, row1 in df.iterrows():
    power1 = row1[0]
    correlations[power1] = []
    for index2, row2 in df.iterrows():
        powers1 = row1[1:]
        powers2 = row2[1:]

        mask1 = np.array(~powers1.isna())
        mask2 = np.array(~powers2.isna())
        mask = np.logical_and(mask1, mask2)

        powers1 = np.array(powers1)[mask]
        powers2 = np.array(powers2)[mask]

        corr, pVal = spearmanr(powers1, powers2)
        correlations[power1].append(corr)
        
        loop.update()

print(correlations)
correlationsDf = pd.DataFrame.from_dict(correlations)
print(correlationsDf)
correlationsDf = correlationsDf.set_index(correlationsDf.columns)
print(correlationsDf.columns)
print(correlationsDf.index)
print(correlationsDf)
correlationsDf.to_csv("fourierCorrelations_blackman_mini.cvs")

