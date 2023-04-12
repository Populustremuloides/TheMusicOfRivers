import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib 
import math

# Prepare the dataframe ***************************************************************

df = pd.read_csv("correlations_between_wavelet_and_cat_chars.csv")
df.index = df[df.columns[0]]
df = df.drop(df.columns[0], axis=1)

# flow metric columns:
for index, col in enumerate(df.columns):
    print(index, col)

corrDict = {}
maxes = []
absMaxes = []
for col in df.columns[113:]:
    corrs = df[col]
    maxes.append(np.max(corrs))
    absMaxes.append(np.max(np.abs(corrs)))

fig, ax = plt.subplots(figsize=(10,2))

for col in df.columns:
    data = df[col]
    data = [float(x) for x in data]
    ax.plot(data, c="dimgrey", alpha=0.8)

samplingRate = 50
rounded = []
for col in df.index:
    #rounded.append(float(format(float(col), ".2f")))
    rounded.append(int(math.ceil(col)))


ax.set_ylabel("coefficient of correlation")
ax.set_xlabel("period length (days)")
ax.set_title("Spearman Correlations between Flow Metrics and Spectral Power")
ax.set_xticks(list(range(len(rounded)))[::samplingRate], rounded[::samplingRate], rotation=90)
plt.tight_layout()
plt.show()


precSeen = False
summerPrecSeen = False
ordSeen = False
tempSeen = False
summerTempSeen = False
damSeen = False
hydroSeen = False
fig, ax = plt.subplots(figsize=(10,6))
for col in df.columns:
    row = np.array(df[col])
    #row = [float(x) for  x in row]
    if "prec" in col.lower() and not "cum" in col.lower() and not ("06" in col.lower() or "07" in col.lower() or "08" in col.lower()):
        if not precSeen:
            ax.plot(row, label="precipitation", c="b")
            precSeen = True
        else:
             ax.plot(row,c="b")
    if "prec" in col.lower() and not "cum" in col.lower() and ("06" in col.lower() or "07" in col.lower() or "08" in col.lower()):
        if not summerPrecSeen:
            ax.plot(row, label="summer precipitation", c="c")
            summerPrecSeen = True
        else:
             ax.plot(row,c="c")
    if "cum" in col.lower() or "ord" in col.lower() or "mag" in col.lower():
        if not ordSeen:
            ax.plot(row, label="catchment size", c="g")
            ordSeen = True
        else:
            ax.plot(row, c="g")
    if "temp" in col.lower() and not ("06" in col.lower() or "07" in col.lower() or "08" in col.lower()):
        print("red: ", col)
        if col == "tempcv":
            ax.plot(row, label="temperature cv", c="tan")
            tempSeen = True
        elif not tempSeen:
            ax.plot(row, label="temperature", c="r")
            tempSeen = True
        else:
            ax.plot(row, c="r")            
    if "temp" in col.lower() and ("06" in col.lower() or "07" in col.lower() or "08" in col.lower()):
        if not summerTempSeen:
            ax.plot(row, label="summer temperature", c="orange")
            summerTempSeen = True
        else:
            ax.plot(row, c="orange")            
    if "drain_den" == col:
            ax.plot(row, label="drainage density", c="yellow")
    if "strmDrop" == col:
            ax.plot(row, label="stream drop", c="magenta")
#    if "gelev_m" == col:
#            ax.plot(row, label="elevation", c="olive")

    if "dam" in col.lower():
        if not damSeen:
            ax.plot(row, label="dams", c="k", linestyle="--")
            damSeen = True
        else:
            ax.plot(row, c="k", linestyle="--")

samplingRate = 50
ax.set_ylim(-0.6,0.6)
ax.set_xticks(list(range(len(rounded)))[::samplingRate], rounded[::samplingRate], rotation=90)
ax.set_ylabel("coefficient of correlation")
ax.set_xlabel("period length (days)")
ax.set_title("Spearman Correlations between Catchment Characteristics and Spectral Power", wrap=True)
plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
plt.tight_layout()
plt.savefig("cat_chars_1_wavelet.png")
plt.show()

hydroSeen = False
fig, ax = plt.subplots(figsize=(10,6))
damSeen = False
for col in df.columns:
    row = np.array(df[col])    
    if "cls1" == col.lower():
        ax.plot(row, label="Evergreen Needle Trees", c="green")
    if "cls2" == col.lower():
        ax.plot(row, label="Evergreen Broadleaf", c="lime")
    if "cls3" == col.lower():
        ax.plot(row, label="Deciduous Broadleaf", c="fuchsia")
    if "cls4" == col.lower():
        ax.plot(row, label="Mixed Other Trees", c="cyan")
    if "cls5" == col.lower():
        ax.plot(row, label="Shrubs", c="darkorange")
    if "cls6" == col.lower():
        ax.plot(row, label="Herbaceous Vegetation", c="gold")
    if "cls7" == col.lower():
        ax.plot(row, label="Cultivated and Managed Vegetation", c="red")
    if "cls8" == col.lower():
        ax.plot(row, label="Regularly Flooded Vegetation", c="lightpink")
    if "cls9" == col.lower():
        ax.plot(row, label="Urban", c="grey")
    if "cls10" == col.lower():
        ax.plot(row, label="Snow Ice", c="lavender")
    if "cls11" == col.lower():
        ax.plot(row, label="Barren", c="tab:brown")
    if "cls12" == col.lower() or "hydro" in col.lower():
        if "hydro" in col.lower():
            ax.plot(row, label="Open Water / lakes (not \nnormalized by catchment size)", c="blue")
        else:
            ax.plot(row, c="blue")

    if "dam" in col.lower():
        print(index)
        if not damSeen:
            ax.plot(row, label="dams", c="k", linestyle="--")
            damSeen = True
        else:
            ax.plot(row, c="k", linestyle="--")

#plt.style.use("seaborn-poster")
#plt.legend()
ax.set_ylim(-0.6,0.6)
ax.set_xticks(list(range(len(rounded)))[::samplingRate], rounded[::samplingRate], rotation=90)
ax.set_ylabel("coefficient of correlation")
ax.set_xlabel("period length (days)")
plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
ax.set_title("Spearman Correlations between Land Cover Characteristics and Spectral Power")
plt.tight_layout()
plt.savefig("cat_chars_2_wavelet.png")
plt.show()

