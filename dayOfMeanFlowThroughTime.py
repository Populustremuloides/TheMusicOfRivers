import pandas as pd
import os
import math
import numpy as np

path = "/home/sethbw/Documents/GlobFlow/localWaterYear/"
segmentSize = 100

def divideByArea(flowData, area):
    newFlowData = []
    for i in range(len(flowData)):
        flow = flowData[i]
        newFlowData.append(float(flow) / float(area))
    return newFlowData


def getMaskAndVec(vec): vec = pd.Series(vec) mask = ~vec.isna()
    mask = np.asarray(mask)
    vec = np.asarray(vec)
    return mask, vec



def getCenterOfMass(flowData):
    dayInYear = list(range(1,len(flowData) + 1))

    numerator = np.sum(np.multiply(flowData, dayInYear))
    denominator = np.sum(flowData)

    if denominator == 0.0:
        centerOfMass = np.sum(dayInYear) / len(dayInYear)
    else:
        centerOfMass = numerator / denominator
    return centerOfMass


dataDf = pd.read_csv("alldata.csv")
dataDf = dataDf[~dataDf["grdc_no"].isna()] 
cats = list(dataDf["grdc_no"])
newCats = []
for cat in cats:
    newCats.append("X" + str(int(cat)))
dataDf["grdc_no"] = newCats

dataDf = dataDf[~dataDf["garea_sqkm"].isna()]

areas = dataDf["garea_sqkm"]
cats = dataDf["grdc_no"]

catToArea = dict(zip(cats, areas))


yearToSpecDisDf = {}
yearToCats = {}
for year in range(1987, 2017):
    for file in os.listdir(path):
        if str(year) in file:
            if "localWaterYear" in file: # FIXME:
                df = pd.read_csv(path + file)
                
                newDict = {}
                for cat in list(df.columns)[1:]:
                    if str("X" + cat) in catToArea.keys():
                        mask, data = getMaskAndVec(df[cat])
                        if len(data[mask]) > 364:
                            flowData = divideByArea(data[mask], catToArea["X" + str(cat)])
                        newDict["X" + cat] = [getCenterOfMass(flowData)]
                newDf = pd.DataFrame.from_dict(newDict)
                print(newDf)
                yearToSpecDisDf[year] = newDf
                yearToCats[year] = list(newDf.columns)

# pre-determined groupings:
# < 10 C
# 10 < x < 25
# > 25 C
cold = dataDf[dataDf["MeanTempAnn"] < 10]
med = dataDf[dataDf["MeanTempAnn"] >= 10]
med = med[med["MeanTempAnn"] < 24]
hot = dataDf[dataDf["MeanTempAnn"] >= 24]


coldAndLarge = cold[cold["gord"] > 5]
coldAndSmall = cold[cold["gord"] <= 5]

medAndLarge = med[med["gord"] > 5]
medAndSmall = med[med["gord"] <= 5]

hotAndLarge = hot[hot["gord"] > 5]
hotAndSmall = hot[hot["gord"] <= 5]

#hot = hot[hot["gord"] > 5] # fixme: I may want to remove this later

coldLargeCats = list(coldAndLarge["grdc_no"])
coldSmallCats = list(coldAndSmall["grdc_no"])

medLargeCats = list(medAndLarge["grdc_no"])
medSmallCats = list(medAndSmall["grdc_no"])

hotLargeCats = list(hotAndLarge["grdc_no"])
hotSmallCats = list(hotAndSmall["grdc_no"])

print()
print()
print("small")
print("num cold cats total: " + str(len(coldSmallCats)))
print("num med cats total: " + str(len(medSmallCats)))
print("num hot cats total: " + str(len(hotSmallCats)))
print("large")
print("num cold cats total: " + str(len(coldLargeCats)))
print("num med cats total: " + str(len(medLargeCats)))
print("num hot cats total: " + str(len(hotLargeCats)))
print()
print()

dataDict = {
        "day_of_mean_flow":[],
        "year":[],
        "catchment":[],
        "category":[]
        }

def updateDataDict(dataDict, df, year, category):
    for col in df.columns:
        dataDict["day_of_mean_flow"].append(df[col][0])
        dataDict["year"].append(year)
        dataDict["catchment"].append(col)
        dataDict["category"].append(category)
    return dataDict

for year in range(1988, 2017):
    df = yearToSpecDisDf[year]
#    coldDf = df[list(set(yearToCats[year]).intersection(set(coldCats)))]
#    medDf = df[list(set(yearToCats[year]).intersection(set(medCats)))]
#    hotDf = df[list(set(yearToCats[year]).intersection(set(hotCats)))]

    coldSmallDf = df[list(set(yearToCats[year]).intersection(set(coldSmallCats)))]
    medSmallDf = df[list(set(yearToCats[year]).intersection(set(medSmallCats)))]
    hotSmallDf = df[list(set(yearToCats[year]).intersection(set(hotSmallCats)))]

    coldLargeDf = df[list(set(yearToCats[year]).intersection(set(coldLargeCats)))]
    medLargeDf = df[list(set(yearToCats[year]).intersection(set(medLargeCats)))]
    hotLargeDf = df[list(set(yearToCats[year]).intersection(set(hotLargeCats)))]


    dataDict = updateDataDict(dataDict, coldSmallDf, year, "cold and small")
    dataDict = updateDataDict(dataDict, medSmallDf, year, "med and small")
    dataDict = updateDataDict(dataDict, hotSmallDf, year, "hot and small")

    dataDict = updateDataDict(dataDict, coldLargeDf, year, "cold and large")
    dataDict = updateDataDict(dataDict, medLargeDf, year, "med and large")
    dataDict = updateDataDict(dataDict, hotLargeDf, year, "hot and large")

outDf = pd.DataFrame.from_dict(dataDict)
outDf.to_csv("dayOfMeanFlowThroughTime.csv")

