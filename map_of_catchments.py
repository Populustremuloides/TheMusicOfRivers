import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
import math
import random
from scipy import stats

numDimensions = 2

df = pd.read_csv("dayOfMeanFlowThroughTime.csv")
cats = list(set(df["catchment"]))
cats.sort()

catToSlope = {
        "catchment":[],
        "dayOfMeanFlow_mean":[]
        }
for cat in cats:
    ldf = df[df["catchment"] == cat]
    years = ldf["year"]
    domf = ldf["day_of_mean_flow"]
    mean = np.mean(domf)
    #slope, intercept, rValue, pValue, stdErr = stats.linregress(years, domf)
    catToSlope["catchment"].append(cat)
    catToSlope["dayOfMeanFlow_mean"].append(mean)

df = pd.DataFrame.from_dict(catToSlope)

alldata = pd.read_csv("alldata.csv", encoding="latin-1")
for column in alldata.columns:
    print(column)

# fix alldata
catchments = []
for cat in alldata["grdc_no"]:
    try:
        catchments.append("X" + str(int(cat)))
    except:
        catchments.append(None)
alldata["catchment"] = catchments

df = df.merge(alldata, on="catchment")
print(df)
#quit()
# make a figure plotting catchment size against meanTempAnn, colored according to one-d

#maxVal = np.max([-1 * np.min(df["dayOfMeanFlow_mean"]), np.max(df["dayOfMeanFlow_mean"])])

minVal = np.min(df["dayOfMeanFlow_mean"])
maxVal = np.max(df["dayOfMeanFlow_mean"])

norm = mpl.colors.Normalize(vmin=minVal, vmax=maxVal) # keep it centered on 0
cmap = cm.seismic
m = cm.ScalarMappable(norm=norm, cmap=cmap)

print(minVal)
print(maxVal)
#quit()
colors = []
xs = []
ys = []
#zs = []
reds = []
blues = []
redMeans = []
blueMeans = []
for index, row in df.iterrows():
    if not math.isnan(row["MeanTempAnn"]) and not math.isnan(row["gord"]):
        #r, g, b, a = m.to_rgba(row["dayOfMeanFlow_mean"])
        #if r == 0 and g == 0 and b == 0 and a == 0:
        #    print(row[colorVar])
        colors.append(m.to_rgba(row["dayOfMeanFlow_mean"]))
        xs.append(row["new_lat.x"])
        ys.append(row["new_lon.x"])

ndf = df[~df["gord"].isna()]
gords = list(ndf["gord"])
temps = list(ndf["MeanTempAnn"])
precips = list(ndf["MeanPrecAnn"])
noise = np.random.normal(size = len(gords)) * 0.17
gords = np.add(gords, noise)
ncolors = []
for index, row in ndf.iterrows():
    ncolors.append(m.to_rgba(row["dayOfMeanFlow_mean"]))

import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
ax.set_extent([-180,180,-90,90], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
plt.scatter(x=df["new_lon.x"], y=df["new_lat.x"], s=0.1, alpha=1)
plt.title("Distribution of Study Catchments")
plt.show()

