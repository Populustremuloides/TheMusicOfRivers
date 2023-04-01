import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import blackman

maxLength = 3561
dt = 1.
periods = 1. / np.fft.rfftfreq(maxLength, d=dt)


# find the minimum length and shorten all the values to be within that range
flowData = pd.read_csv("universallyAlignedGlobalFlow_DailyQ2_column.csv")
newDataDict = {}
minColLength = 10000000
for col in flowData.columns:
    mask = np.array(~flowData[col].isna())
    if np.sum(mask) < minColLength:
        minColLength = np.sum(mask)
    newData = np.array(flowData[col])[mask]
    newDataDict[col] = newData

for key in newDataDict.keys():
    newDataDict[key] = newDataDict[key][:minColLength]

flowData = pd.DataFrame.from_dict(newDataDict)


maxLength = minColLength #flowData[]#11326
print(maxLength / (2 * np.pi))
dt = 1.
#periods = np.fft.rfftfreq(maxLength, d=dt) * 2 * np.pi
#print(periods)

maxLength = periods.shape[0]
#print(periods)
#quit()
#flowData = pd.read_csv("universallyAlignedGlobalFlow_DailyQ2_column.csv")

print(flowData.columns)

catchmentToFourier = {} 
catchmentToFourier["period_days"] = periods
print(catchmentToFourier["period_days"])
#quit()
#print(1. / periods)
lengths = []
l = 0
for column in flowData:
    
    if column.isnumeric(): 
        data = flowData[column]
        # get rid of everything past the first "none"

        # get the first bit of data:
        startIndex = 0
        for i in range(len(data)):
            if ~np.isnan(data[i]):
                startIndex = i
#                print(startIndex)
                break
        

        stopIndex = len(data)
        for i in range(startIndex, len(data)):
#            print(data[i])
#            sdata = pd.Series(data[i])
#            if pd.isna(sdata[0]):
#                stopIndex = i
#                break
            if np.isnan(data[i]):
                stopIndex = i
                break
        
        keptData = data[startIndex:stopIndex]

#        print(keptData)
#        keptData = pd.Series(keptData)
        keptData = np.array([float(x) for x in keptData])
        keptData = keptData - np.mean(keptData)
        keptData = keptData / np.max(keptData)
        catchment = column


        w = blackman(keptData.shape[0])
        result = np.fft.rfft(keptData * w)

        #real = np.real(result) ** 2
        #imaginary = np.imag(result) ** 2
        magnitudes = np.abs(result) ** 2
        #fig, axs = plt.subplots(1, 2)
        #axs[0].plot(keptData)
        #axs[1].plot(1. / periods[:magnitudes.shape[0]], magnitudes)
        #plt.show()


        lengths.append(magnitudes.shape[0])
       

        diff = maxLength - magnitudes.shape[0]
        extra = [None] * diff
        magnitudes = np.concatenate((magnitudes, extra), axis=0)

        catchmentToFourier[catchment] = magnitudes
        #print(catchmentToFourier)
    percentDone = float(l) / float(len(flowData.columns) - 5)

    print(percentDone)

    l = l + 1

#for key in catchmentToFourier.keys():
#    print(len(catchmentToFourier[key]))

for cat in catchmentToFourier.keys():
    print(cat, len(catchmentToFourier[cat]))

df = pd.DataFrame.from_dict(catchmentToFourier)
df.to_csv("glob_flow_fourier_decomposition_blackman.csv")
print(max(lengths))
