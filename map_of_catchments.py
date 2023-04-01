import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np
import math
import random
from scipy import stats


df = pd.read_csv("alldata.csv", encoding="latin-1")

# make a figure plotting catchment size against meanTempAnn, colored according to one-d


import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure(figsize=(16,8))
ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
ax.set_extent([-180,180,-58,83], crs=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE)
plt.scatter(x=df["new_lon.x"], y=df["new_lat.x"], s=2, alpha=1, c="r")
plt.title("Distribution of Study Catchments", fontsize=20)
plt.savefig("map_of_all_catchments.png", dpi=400)
plt.show()

