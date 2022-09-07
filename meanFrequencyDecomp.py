import pandas as pd
from scipy.stats.stats import pearsonr
import seaborn as sns
import matplotlib.pyplot as plt
# Read in the metric information
import numpy as np

flowMetricsPath = "alldata.csv" # FIXME: only a portion of the sites were recoverable with the lat/lon information


metricDataDict = {}
metricDataDict["catchment"] = []
metricDataDict["metric1"] = []
metricDataDict["metric2"] = []
metricDataDict["metric3"] = []
metricDataDict["metric4"] = []
metricDataDict["metric5"] = []
metricDataDict["metric6"] = []
metricDataDict["metric7"] = []


with open(flowMetricsPath, "r+", encoding = "ISO-8859-1") as metricFile:
    i = 0
    for line in metricFile:
        if i > 0:
            line = line.replace("\n","")
            line = line.split(",")
            
            catchment = str(line[4])

            if catchment != "multipleFound":
                try:

                    catchment = str(catchment)
                    metric1 = float(line[-7])
                    metric2 = float(line[-6])
                    metric3 = float(line[-5])
                    metric4 = float(line[-4])
                    metric5 = float(line[-3])
                    metric6 = float(line[-2])
                    metric7 = float(line[-1])

                    metricDataDict["catchment"].append(catchment)
                    metricDataDict["metric1"].append(metric1)
                    metricDataDict["metric2"].append(metric2)
                    metricDataDict["metric3"].append(metric3)
                    metricDataDict["metric4"].append(metric4)
                    metricDataDict["metric5"].append(metric5)
                    metricDataDict["metric6"].append(metric6)
                    metricDataDict["metric7"].append(metric7)

                    print(catchment)
                except:
                    pass
        i = i + 1

print(len(metricDataDict["catchment"]))

metricDF = pd.DataFrame.from_dict(metricDataDict)


# Read in the wavelet transform information

flowPeriodsPath = "universallyAligned_powersTranpose.csv"
periodDataDict = {}


with open(flowPeriodsPath, "r+") as flowFile:
    i = 0
    for line in flowFile:
        line = line.replace("\n","")
        line = line.split(",")

        if i == 0:
            pass
        elif i == 1:
            periodDataDict["catchment"] = []
            periods = line[1:]
            for period in periods:
                periodDataDict[period] = []
        else:
            catchment = str(line[0])

            if "." not in catchment:
                catchment = catchment.replace("\"","")
                catchment = catchment.replace("X","")
                data = line[1:]
                data = [float(x) for x in data]
            
                periodDataDict["catchment"].append(str(catchment))
                for index in range(len(periods)):
                    period = periods[index]
                    datum = data[index]
                    periodDataDict[period].append(datum)

        i = i + 1

periodDF = pd.DataFrame.from_dict(periodDataDict)
#totalDF = metricDF.merge(periodDF, on="catchment", how="inner")
print("totalDf")


print("total df")

fdf = pd.read_csv("FullDatabase.csv")
fdf = fdf.drop(fdf.columns[0], axis=1)
for col in fdf.columns:
    print(col)
#print(fdf.columns)

newCats = []
for cat in fdf["grdc_no"]:
    try:
        newCat = str(int(float(cat)))
    except:
        newCat = None
    newCats.append(newCat)

fdf["catchment"] = newCats

#totalDF = totalDF.merge(fdf, on="catchment", how="inner")
totalDF = periodDF.merge(fdf, on="catchment", how="inner")




p = totalDF["MeanTempAnn"]
b15 = totalDF["bio18"]
m1 = np.asarray(~p.isna())
m2 = np.asarray(~b15.isna())
m = np.logical_and(m1, m2)
p = np.asarray(p)
b15 = np.asarray(b15)
p = p[m]
b15 = b15[m]
plt.scatter(p, b15, alpha=0.2)
plt.xlabel("temperature")
plt.ylabel("summer temperature")
plt.show()



p = totalDF["gord"]
b15 = totalDF["bio4"]
m1 = np.asarray(~p.isna())
m2 = np.asarray(~b15.isna())
m = np.logical_and(m1, m2)
p = np.asarray(p)
b15 = np.asarray(b15)
p = p[m]
b15 = b15[m]
plt.scatter(p, b15, alpha=0.2)
plt.xlabel("gord")
plt.ylabel("bio4")
plt.show()





print(totalDF["catchment"])
biomes = list(set(list(totalDF["BIOME"])))


temps = list(totalDF["MeanTempAnn"])
orders = list(totalDF["gord"])
prec = list(totalDF["MeanPrecAnn"])
seas = list(totalDF["bio15"])
seast = list(totalDF["bio4"])


stmin = np.min(seast)
stmax = np.max(seast)
strange = stmax - stmin
increment = strange / 3
st1 = stmin
st2 = stmin + increment
st3 = stmin + increment + increment
st4 = stmin + increment + increment + increment

print("in here")
stcats = []
for s in totalDF["bio4"]:
    s = float(s)
    if (s >= (st1 - 1)) and (s < st2):
        stcats.append("nonSeasonalTemp")
    elif (s >= st2) and (s < st3):
        stcats.append("med")
    elif (s >= st3) and (s <= (st4 + 1)):
        stcats.append("seasonalTemp")
    else:
        stcats.append(np.nan)
        print(s)
totalDF["seasTempCat"] = stcats



smin = np.min(seas)
smax = np.max(seas)
srange = smax - smin
increment = srange / 3
s1 = smin
s2 = smin + increment
s3 = smin + increment + increment
s4 = smin + increment + increment + increment

print("in here")
scats = []
for s in totalDF["bio15"]:
    s = float(s)
    if (s >= (s1 - 1)) and (s < s2):
        scats.append("nonSeasonalPrec")
    elif (s >= s2) and (s < s3):
        scats.append("med")
    elif (s >= s3) and (s <= (s4 + 1)):
        scats.append("seasonalPrec")
    else:
        scats.append(np.nan)
        print(s)
totalDF["seasCat"] = scats


pmin = np.min(prec)
pmax = np.max(prec)
prange = pmax - pmin
increment = prange / 3
p1 = pmin
p2 = pmin + increment
p3 = pmin + increment + increment
p4 = pmin + increment + increment + increment


print("in here")
pcats = []
for p in totalDF["MeanPrecAnn"]:
    p = float(p)
    if (p >= (p1 - 1)) and (p < p2):
        pcats.append("dry")
    elif (p >= p2) and (p < p3):
        pcats.append("med")
    elif (p >= p3) and (p <= (p4 + 1)):
        pcats.append("wet")
    else:
        pcats.append(np.nan)
        print(p)
totalDF["precCat"] = pcats



tmin = np.min(temps)
tmax = np.max(temps)
trange = tmax - tmin
increment = trange / 3
t1 = tmin
t2 = tmin + increment
t3 = tmin + increment + increment
t4 = tmin + increment + increment + increment
print(tmin)
print(t1)
print(t2)
print(t3)
print(t4)
print(tmax)

print("in here")
tcats = []
for t in totalDF["MeanTempAnn"]:
    t = float(t)
    if (t >= (t1 - 1)) and (t < t2):
        tcats.append("cold")
    elif (t >= t2) and (t < t3):
        tcats.append("med")
    elif (t >= t3) and (t <= (t4 + 1)):
        tcats.append("hot")
    else:
        tcats.append(np.nan)
        print(t)



cold = 0
med = 0
hot = 0
for cat in tcats:
    if cat == "cold":
        cold += 1
    elif cat == "med":
        med += 1
    elif cat == "hot":
        hot += 1
print("cold: " + str(cold))
print("med: " + str(med))
print("hot: " + str(hot))

totalDF["tempCat"] = tcats

#print(totalDF["tempCat"])



omin = np.min(orders)
omax = np.max(orders)
orange = omax - omin
increment = orange / 3
o1 = omin
o2 = omin + increment
o3 = omin + increment + increment
o4 = omin + increment + increment + increment
print(omin)
print(o1)
print(o2)
print(o3)
print(o4)
print(omax)

#print("in here")
ocats = []
for o in totalDF["gord"]:
    o = float(o)
    if (o >= (o1 - 1)) and (o < o2):
        ocats.append("small")
    elif (o >= o2) and (o < o3):
        ocats.append("med")
    elif (o >= o3) and (o <= (o4 + 1)):
        ocats.append("large")
    else:
        ocats.append(np.nan)
        print(p)

small = 0
med = 0
large = 0
for cat in ocats:
    if cat == "small":
        small += 1
    elif cat == "med":
        med += 1
    elif cat == "large":
        large += 1
print("small: " + str(small))
print("med: " + str(med))
print("large: " + str(large))

totalDF["gordCat"] = ocats

#print(totalDF["gordCat"])

#quit()

#plt.hist(temps)
#plt.show()
#plt.hist(orders)
#plt.show()
#print(temps)
#print(orders)
#quit()

for biome in biomes:
    print(biome)
    if type(biome) == type("string"):
        subDF = totalDF[totalDF["BIOME"] == biome]
        biome = biome.replace(" ","-")
        biome = biome.replace("/","-")
        biome = biome.replace("\\","-")
        biome = biome.replace(",","-")
        print(biome + " " + str(len(subDF["catchment"])))

#print(totalDF)
#quit()

# for each metric, go through all the other periods and take the correlation
#metrics = ["metric1","metric2","metric3","metric4","metric5","metric6","metric7"]


def getLongMatrix(df):
    dataDict = {"period":[],"power":[], "temp":[], "order":[], "precip":[], "seasonality":[], "biome":[]}
    for period1 in periods:
        periodVals1 = list(df[period1])
        
        for index, row in df.iterrows():
            dataDict["period"].append(period1)
            dataDict["power"].append(row[period1])
            dataDict["order"].append(row["gordCat"])
            dataDict["temp"].append(row["tempCat"])
            dataDict["precip"].append(row["precCat"])
            dataDict["seasonality"].append(row["seasCat"])
            dataDict["biome"].append(row["BIOME"])

        print(period1)
    return dataDict


dataDict = getLongMatrix(totalDF)
dataDF = pd.DataFrame.from_dict(dataDict)
dataDF.to_csv("long_matrix_temp_order_seas_prec.csv", index=False)



#dataDict = {"period":[],"power":[], "type":[]}
#for biome in biomes:
#    print(biome)
#    subDF = totalDF[totalDF["BIOME"] == biome]
#    print(subDF)
#    dataDict = getLongMatrix(subDF, dataDict, biome)

#dataDF = pd.DataFrame.from_dict(dataDict)
#dataDF.to_csv("long_matrix_biome.csv", index=False)

#    print(biome + " " + str(len(subDF["catchment"])))



#print(metricToPeriodDF)
#sns.heatmap(metricToPeriodDF, xticklabels=48, center=0, yticklabels=False)
#plt.xlabel("period length (days)")
#plt.title("Correlation Between Mean Period Strengths")
#plt.show()


#vals = metricToPeriodDF.transpose().values
#print(vals.shape)
#print(np.linalg.matrix_rank(vals))


