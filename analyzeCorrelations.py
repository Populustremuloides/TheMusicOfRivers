import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib 
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 14}
matplotlib.rc('font', **font)


# Prepare the dataframe ***************************************************************

fdf = pd.read_csv("universallyAligned_powersTranpose.csv")
df = pd.read_csv("FullDatabase.csv")
newCats = []
for cat in df["grdc_no"]:
    try:
        newCats.append("X" + str(int(float(cat))))
    except:
        newCats.append(np.nan)
df["grdc_no"] = newCats

print(fdf)
fdf.columns = list(fdf.iloc[0])
fdf = fdf.drop(fdf.index[0])
fdf["grdc_no"] = fdf["scale"]
fdf = fdf.drop("scale", axis=1)
print(fdf)
print(df)

df = df.merge(fdf, on="grdc_no", how="inner")
print(df)


# prepare the color mapper ***************************************************************

import matplotlib.cm as cm
import matplotlib as mpl

#temps = list(df["MeanTempAnn"])
#minTemp = min(temps)
#maxTemp = max(temps)

#ords = list(df["gord"])
#minOrd = min(ords)
#maxOrd = max(ords)

precs = list(df["MeanPrecAnn"])
minPrec = min(precs)
maxPrec = max(precs)

#norm = mpl.colors.Normalize(vmin=minTemp, vmax=maxTemp)
#norm = mpl.colors.Normalize(vmin=minOrd, vmax=maxOrd)
norm = mpl.colors.Normalize(vmin=minPrec, vmax=maxPrec)

#cmap = cm.seismic # temperature
#cmap = cm.PiYG # stream order
cmap = cm.ocean # precip

m = cm.ScalarMappable(norm=norm, cmap=cmap)



#from matplotlib.lines import Line2D

#fig, ax = plt.subplots(figsize=(6, 1))
#fig.subplots_adjust(bottom=0.5)
#cmap = mpl.cm.seismic
#cmap = mpl.cm.PiYG
#cmap = mpl.cm.ocean

#norm = mpl.colors.Normalize(vmin=minTemp, vmax=maxTemp)
#norm = mpl.colors.Normalize(vmin=minOrd, vmax=maxOrd) #norm = mpl.colors.Normalize(vmin=minPrec, vmax=maxPrec)

#cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
#                                norm=norm,
#                                orientation='horizontal')

#cb1.set_label('mm precipitation')
#fig.show()
#plt.show()
#quit()


# plot! *********************************************************************************

print(df.columns[302:])

for i in range(len(df.columns[302:])):
    print(df.columns[302 + i])
    print()

#quit()
nums = list(range(len(df.columns[302:])))
rounded = []
for num in df.columns[302:]:
    rounded.append(int(round(float(num))))


#i = 0
#for col in df.columns:
#    print(str(i) + " " + str(col))
#    i = i + 1
    # 302 is the magic number

plt.rcParams["figure.figsize"] = (15,8)
for index, row in df.iterrows():
    data = row[302:]

    #colorVar = row["MeanTempAnn"]
    #colorVar = row["gord"]
    #colorVar = row["MeanPrecAnn"]
    colorVar = row["strmDrop"]

    if not pd.isna(colorVar):
        c = m.to_rgba(colorVar)
        #plt.plot(list(data), c=c, alpha=0.01) # temperature
        #plt.plot(list(data), c=c, alpha=0.2) # stream order
        #plt.plot(list(data), c=c, alpha=0.025) # precipitation
        #print(len(data))
        #print(len(nums))
        #print(len(rounded))

#plt.xticks(nums[::50], rounded[::50], rotation=45)
#plt.title("Global Distribution of Catchment Frequency Decompositions - by Temperature")
#plt.title("Global Distribution of Catchment Frequency Decompositions - by Stream Order")
#plt.title("Global Distribution of Catchment Frequency Decompositions - by Precipitation")

#plt.xlabel("period")
#plt.ylabel("time-averaged spectral power")
#plt.figure(figsize=(20,10))
#plt.show()



#df = pd.read_csv("correlationsFrequencyToFlowMetrics.csv")
#df = pd.read_csv("frequency_to_flow_metrics_r_all_jan2021.csv")
df = pd.read_csv("frequency_to_flow_metrics_r_all_jan2021_universally_aligned.csv")
#df = pd.read_csv("original_flow_metrics_to_frequency_correlations.csv")
#df = pd.read_csv("original_flow_metrics_to_frequency_correlations.csv")


df["flowMetric"] = df[df.columns[0]]
df.index = df["flowMetric"]
df = df.drop(df.columns[0], axis=1)
df = df.drop("flowMetric", axis=1)
print(df)

corrDict = {}
maxes = []
absMaxes = []
for index, row in df.iterrows():
    row = [float(x) for x in row]
#    plt.plot(row)
#    plt.title(index)
#    plt.xticks()
#    plt.show()
    maxVal = max(row)
    minVal = min(row)
    diff = maxVal - minVal
    absrow = [abs(x) for x in row]
    maxes.append(row[np.argmax(absrow)])
    absMaxes.append(max(absrow)) 
    corrDict[row[np.argmax(absrow)]] = [index, df.columns[np.argmax(absrow)]]
#    maxes.append(diff)


print(np.mean(absMaxes))
plt.hist(maxes, bins=60)
plt.xlabel("coefficient of correlation")
plt.ylabel("count")
plt.title("Maximum Spearman Coefficient of Correlation between Flow Metrics and Spectral Power")
plt.show()

for index, row in df.iterrows():
    print(index)
#    if "dh" in index:
#        plt.plot(row, c="blue") 
#    if "dl" in index:
#        plt.plot(row, c="violet")
#    if "fh" in index:
#        plt.plot(row, c="crimson")
#    if "ma" in index:
#        plt.plot(row, c="green")
#    if "ml" in index:
#        plt.plot(row, c="gold")
    plt.plot(row, c="dimgrey", alpha=0.8)

nums = list(range(len(df.columns)))
rounded = []
for col in df.columns:
    rounded.append(int(round(float(col))))


#ax1.set_ylabel("mean spectral power")
#ax2.set_ylabel("coefficient of correlation")
plt.ylabel("coefficient of correlation")
plt.xlabel("period length (days)")
plt.title("Spearman Correlations between Flow Metrics and Spectral Power")
plt.xticks(nums[::50], rounded[::50], rotation=90)
plt.show()



df = pd.read_csv("frequency_to_catchment_attributes_r_all.csv")
df.index = df[df.columns[0]]
df = df.drop(df.columns[0], axis=1)
print(df)
#quit()
    #print(max(row))


precSeen = False
summerPrecSeen = False
ordSeen = False
tempSeen = False
summerTempSeen = False
damSeen = False
hydroSeen = False
for index, row in df.iterrows():
    row = [float(x) for  x in row]
    if "prec" in index.lower() and not "cum" in index.lower() and not ("06" in index.lower() or "07" in index.lower() or "08" in index.lower()):
        if not precSeen:
            plt.plot(row, label="precipitation", c="b")
            precSeen = True
        else:
             plt.plot(row,c="b")
    if "prec" in index.lower() and not "cum" in index.lower() and ("06" in index.lower() or "07" in index.lower() or "08" in index.lower()):
        if not summerPrecSeen:
            plt.plot(row, label="summer precipitation", c="c")
            summerPrecSeen = True
        else:
             plt.plot(row,c="c")
    if "cum" in index.lower() or "ord" in index.lower() or "mag" in index.lower():
        if not ordSeen:
            plt.plot(row, label="catchment size", c="g")
            ordSeen = True
        else:
            plt.plot(row, c="g")
    if "temp" in index.lower() and not ("06" in index.lower() or "07" in index.lower() or "08" in index.lower()):
         if not tempSeen:
            plt.plot(row, label="temperature", c="r")
            tempSeen = True
         else:
            plt.plot(row, c="r")            
    if "temp" in index.lower() and ("06" in index.lower() or "07" in index.lower() or "08" in index.lower()):
         if not summerTempSeen:
            plt.plot(row, label="summer temperature", c="orange")
            summerTempSeen = True
         else:
            plt.plot(row, c="orange")            
    if "drain_den" == index:
            plt.plot(row, label="drainage density", c="yellow")
    if "strmDrop" == index:
            plt.plot(row, label="stream drop", c="magenta")
    if "gelev_m" == index:
            plt.plot(row, label="elevation", c="k")


#    if "cls7" in index.lower():
#        plt.plot(row, label="cultivated land", c="fuchsia")
    print(index)


nums = list(range(len(df.columns)))
rounded = []
for col in df.columns:
    rounded.append(int(round(float(col))))



#plt.legend()
plt.ylim(-0.6,0.6)
plt.xticks(nums[::50], rounded[::50], rotation=90)
plt.ylabel("coefficient of correlation")
plt.xlabel("period length (days)")
plt.title("Spearman Correlations between Topological/Climatic Characteristics and Spectral Power")
plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
plt.show()


damSeen = False
for index, row in df.iterrows():
    row = [float(x) for  x in row]
    if "cls1" == index.lower():
        plt.plot(row, label="Evergreen Needle Trees", c="green")
    if "cls2" == index.lower():
        plt.plot(row, label="Evergreen Broadleaf", c="lime")
    if "cls3" == index.lower():
        plt.plot(row, label="Deciduous Broadleaf", c="fuchsia")
    if "cls4" == index.lower():
        plt.plot(row, label="Mixed Other Trees", c="cyan")
    if "cls5" == index.lower():
        plt.plot(row, label="Shrubs", c="darkorange")
    if "cls6" == index.lower():
        plt.plot(row, label="Herbaceous Vegetation", c="gold")
    if "cls7" == index.lower():
        plt.plot(row, label="Cultivated and Managed Vegetation", c="red")
    if "cls8" == index.lower():
        plt.plot(row, label="Regularly Flooded Vegetation", c="lightpink")
    if "cls9" == index.lower():
        plt.plot(row, label="Urban", c="grey")
    if "cls10" == index.lower():
        plt.plot(row, label="Snow Ice", c="lavender")
    if "cls11" == index.lower():
        plt.plot(row, label="Barren", c="tab:brown")
    if "cls12" == index.lower() or "hydro" in index.lower():
        if "hydro" in index.lower():
            plt.plot(row, label="Open Water / lakes (not \nnormalized by catchment size)", c="blue")
        else:
            plt.plot(row, c="blue")

    if "dam" in index.lower():
        print(index)
        if not damSeen:
            plt.plot(row, label="dams", c="k")
            damSeen = True
        else:
            plt.plot(row, c="k")

plt.style.use("seaborn-poster")
#plt.legend()
plt.ylim(-0.6,0.6)
plt.xticks(nums[::50], rounded[::50], rotation=90)
plt.ylabel("coefficient of correlation")
plt.xlabel("period length (days)")
plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
plt.title("Spearman Correlations between Land Cover/Use Characteristics and Spectral Power")
plt.show()
#quit()




#    row = [abs(x) for x in row]
#    maxes.append(max(row))
#   #print(max(row))
#    
#    print(str(index) + ", " + str(row[np.argmax(absrow)]))
#    maxVal = max(row)
#    minVal = min(row)
#    diff = maxVal - minVal
#    absrow = [abs(x) for x in row]
#    maxes.append(row[np.argmax(absrow)])
#    absMaxes.append(max(absrow)) 
#    if index != "quality":
#        corrDict[row[np.argmax(absrow)]] = [index, df.columns[np.argmax(absrow)], np.mean(absrow)]






#plt.hist()
print(np.sum([x > 0.5 for x in absMaxes]))
print(len(absMaxes))
print(np.sum([x > 0.5 for x in absMaxes]) / len(absMaxes))
print(np.mean(absMaxes))

print(corrDict)
correlations = list(corrDict.keys())
correlations.sort()
#with open("correlations_frequency_to_metrics.csv", "w+") as ofile:
#    ofile.write("index,correlation,metric,frequency\n")
#
#    j = 0
#    for cor in correlations:
#        print(str(cor) + " " + corrDict[cor][0])
#        ofile.write(str(j) + "," + str(cor) + "," + corrDict[cor][0] + "," + str(round(float(corrDict[cor][1]))) + "\n")
#        j = j + 1
#quit()

'''





df = pd.read_csv("correlationsFrequencyToCatchmentChars.csv")

df["flowMetric"] = df[df.columns[0]]
df.index = df["flowMetric"]
df = df.drop(df.columns[0], axis=1)
df = df.drop("flowMetric", axis=1)
print(df)

maxes = []
absMaxes = []
corrDict = {}

precSeen = False
ordSeen = False
tempSeen = False
damSeen = False
hydroSeen = False
for index, row in df.iterrows():
    row = [float(x) for  x in row]
    if "prec" in index.lower() and not "cum" in index.lower():
        if not precSeen:
            plt.plot(row, label="precipitation", c="b")
            precSeen = True
        else:
            plt.plot(row,c="b")
    if "cum" in index.lower() or "ord" in index.lower() or "mag" in index.lower():
        if not ordSeen:
            plt.plot(row, label="catchment size", c="g")
            ordSeen = True
        else:
            plt.plot(row, c="g")
    if "temp" in index.lower() and not ("06" in index.lower() or "07" in index.lower() or "08" in index.lower()):
        if not tempSeen:
            plt.plot(row, label="temperature", c="r")
            tempSeen = True
        else:
            plt.plot(row, c="r")            
    if "temp" in index.lower() and ("06" in index.lower() or "07" in index.lower() or "08" in index.lower()):
        if not tempSeen:
            plt.plot(row, label="summer temperature", c="orange")
            tempSeen = True
        else:
            plt.plot(row, c="r")            


    if "dam" in index.lower():
        if not damSeen:
            plt.plot(row, label="dams", c="k")
            damSeen = True
        else:
            plt.plot(row, c="k")

    if "hydro" in index.lower() or "water" in index.lower() or "cls12" in index.lower():
        if not hydroSeen:
            plt.plot(row, label="water cover", c="c")
            hydroSeen = True
        else:
            plt.plot(row, c="c")


#    row = [abs(x) for x in row]
    maxes.append(max(row))
    #print(max(row))
    
    print(str(index) + ", " + str(row[np.argmax(absrow)]))
    maxVal = max(row)
    minVal = min(row)
    diff = maxVal - minVal
    absrow = [abs(x) for x in row]
    maxes.append(row[np.argmax(absrow)])
    absMaxes.append(max(absrow)) 
    if index != "quality":
        corrDict[row[np.argmax(absrow)]] = [index, df.columns[np.argmax(absrow)], np.mean(absrow)]

nums = list(range(len(df.columns)))
rounded = []
for col in df.columns:
    rounded.append(int(round(float(col))))


plt.legend()
plt.xticks(nums[::50], rounded[::50], rotation=90)
plt.ylabel("coefficient of correlation")
plt.xlabel("period length")
plt.title("correlations between catchment characteristics and frequencies")
plt.show()

print(np.sum([x > 0.5 for x in absMaxes]))
print(len(absMaxes))
print(np.sum([x > 0.5 for x in absMaxes]) / len(absMaxes))
print(np.mean(absMaxes))

print(corrDict)
correlations = list(corrDict.keys())
correlations.sort()
with open("correlations_frequency_to_catchment_chars.csv", "w+") as ofile:
    ofile.write("index,greatestCorrelation,averageCorrelation,metric,frequency\n")

    j = 0
    for cor in correlations:
        print(str(cor) + " " + corrDict[cor][0])
        ofile.write(str(j) + "," + str(cor) + "," + str(corrDict[cor][2]) + "," + str(corrDict[cor][0]) + "," + str(round(float(corrDict[cor][1]))) + "\n")
        j = j + 1


plt.hist(maxes, bins=15)
plt.xlabel("coefficient of correlation")
plt.ylabel("count")
plt.title("maximum correlation between frequency domain and catchment characteristics")
plt.show()

'''
