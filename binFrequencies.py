import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("glob_flow_fourier_decomposition_blackman.csv")
#plt.plot(df["period"])
#plt.show()

# grab 5,
# then 10,
# then 20
# then 40

chunkSize = 1
newData = np.array(["empty"])
numRowsSeen = 0
while numRowsSeen < len(df):

    littleData = df.iloc[numRowsSeen:(numRowsSeen + chunkSize)].to_numpy()
    means = np.nanmean(littleData, axis=0)

    if newData[0] == "empty":
        newData = means
        newData = np.expand_dims(newData, axis=0)
    else:

        newData = np.vstack([newData, means])

    numRowsSeen = numRowsSeen + chunkSize
    chunkSize = chunkSize * 2

print(newData)
print(newData.shape)

dataDict = {}
for index, col in enumerate(df.columns):
    dataDict[col] = newData[:,index]

outDf = pd.DataFrame.from_dict(dataDict)
outDf = outDf.drop(outDf.columns[0], axis=1)
outDf.index = outDf[outDf.columns[0]]
outDf = outDf.drop(outDf.columns[0], axis=1)
print(outDf)
outDf.to_csv("glob_flow_fourier_decomposition_blackman_mini.csv")


