import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import os 


outputDir = "paper1Figures"
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

df = pd.read_csv("alldata.csv")

# incorperate frequency data *********************************
newLabels = []
for grdc_no in df["grdc_no"]:
    try:
        newLabels.append("X" + str(int(grdc_no)))
    except:
        newLabels.append(None)
df["grdc_no"] = newLabels
df = df[~df["grdc_no"].isna()]

fdf = pd.read_csv("universallyAligned_powersTranpose.csv")
scale = fdf.iloc[0][1:]
scale = [float(item) for item in scale]
scale = np.array(scale)

df = df.merge(fdf, left_on="grdc_no", right_on=fdf.columns[0])

# utility for dealing with NAs in the data

def maskNAs(pandasSeries1, pandasSeries2):
    mask0 = []
    for item in pandasSeries1:
        try:
            item = float(item)
            mask0.append(True)
        except:
            mask0.append(False)

    mask0 = np.array(mask0)
    pandasSeries1 = pandasSeries1[mask0]
    pandasSeries2 = pandasSeries2[mask0]

    mask1 = np.array(~pandasSeries1.isna())
    mask2 = np.array(~pandasSeries2.isna())

    array1 = np.array(pandasSeries1, dtype=np.float32)
    array2 = np.array(pandasSeries2, dtype=np.float32)

    mask = np.logical_and(mask1, mask2)

    array1 = array1[mask]
    array2 = array2[mask]

    return array1, array2

# utility for calculating correlations between columns

def getCorrelations(ldf, targetCol, sort=True):
    damcountN = ldf[targetCol]
    keptColumns = []
    damcountStats = []
    for col in ldf.columns:
        if col != targetCol:
            a1, a2 = maskNAs(ldf[col], damcountN)
            if a1.shape[0] > 10:
                stat, pval = spearmanr(a1,a2)
                damcountStats.append(stat)
                keptColumns.append(col)
    
    damcountStats = np.array(damcountStats)
    if sort:
        indices = np.argsort(damcountStats)
        keptColumns = np.array(keptColumns)[indices]
        damcountStats = damcountStats[indices]
    return keptColumns, damcountStats

# Calculate the correlations

# 8 - 197 metrics
# 196 - 312 chars
# 312:319 PCA metrics
# 320:-1 frequency decomposition

targetCol = "damcountN"

metricCols = list(df.columns[8:197])
metricCols.append(targetCol)
charCols = list(df.columns[197:312])
pcaCols = list(df.columns[312:319])
pcaCols.append(targetCol)

freqCols = list(df.columns[320:])
freqCols.append(targetCol)

keptColumnsMetrics, damcountStatsMetrics = getCorrelations(df[metricCols], targetCol)
keptColumnsPCA, damcountStatsPCA = getCorrelations(df[pcaCols], targetCol)
keptColumnsChar, damcountStatsChar = getCorrelations(df[charCols], targetCol)
keptColumnsFreq, damcountStatsFreq = getCorrelations(df[freqCols], targetCol, sort=False)

# make figures to show the results *********************************


otherMask = []
damMask = []
humanMask = []
areaMask = []
for item in keptColumnsChar:
    print(item)
    if "dam" in item.lower():
        damMask.append(True)
    else:
        damMask.append(False)

    if "CumPrec" in item or "area" in item.lower() or "length" in item.lower() or "ord" in item:
        areaMask.append(True)
    else:
        areaMask.append(False)

    if "opden" in item or "uman" in item:
        humanMask.append(True)
    else:
        humanMask.append(False)
    
    otherMask.append(True) 

otherMask = np.array(otherMask)
damMask = np.array(damMask) 
humanMask = np.array(humanMask)
areaMask = np.array(areaMask)


plt.scatter(np.arange(damcountStatsChar.shape[0])[otherMask], damcountStatsChar[otherMask], c="grey", label="other")
plt.scatter(np.arange(damcountStatsChar.shape[0])[areaMask], damcountStatsChar[areaMask], c="g", label="catchment area")
plt.scatter(np.arange(damcountStatsChar.shape[0])[humanMask], damcountStatsChar[humanMask], c="b", label="human impact")
plt.scatter(np.arange(damcountStatsChar.shape[0])[damMask], damcountStatsChar[damMask], c="k", label="other dam info")
plt.ylim(-0.5, 1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("index of characteristic (arbitrary)", fontsize=16)
plt.ylabel("Pearson correlation coefficient", fontsize=16)
plt.legend()
#plt.title("Correlations between Catchment Characteristics and # Dams", fontsize=20, wrap=True)
plt.tight_layout()
plt.savefig(os.path.join(outputDir, "dams_chars.png"))
plt.show()

roundedScale = scale.astype(np.int)
plt.plot(damcountStatsFreq)
plt.ylim(-0.5, 1)
plt.ylabel("Pearson correlation coefficient", fontsize=16)
#plt.xticks(ticks=np.arange(scale.shape[0]), labels=scale)
nums = np.arange(roundedScale.shape[0])
plt.xticks(nums[::60], roundedScale[::60], rotation=90, fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("period length (days)", fontsize=16)
plt.tight_layout()
#plt.title("Correlations between Wavelet Decomposition and # Dams",fontsize=18, wrap=True)
plt.savefig(os.path.join(outputDir, "dams_freq.png"))
plt.show()

plt.plot(damcountStatsMetrics)
plt.ylim(-0.5, 1)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("index of flow metric (arbitrary)", fontsize=16)
plt.ylabel("Pearson correlation coefficient", fontsize=16)
#plt.title("Correlations between Flow Metrics and # Dams", fontsize=18, wrap=True)
plt.tight_layout()
plt.savefig(os.path.join(outputDir, "dams_metrics.png"))
plt.show()

plt.plot(damcountStatsPCA)
plt.ylim(-0.5, 1)
plt.xticks(ticks=np.arange(keptColumnsPCA.shape[0]), labels=keptColumnsPCA,fontsize=14, rotation=330)
plt.yticks(fontsize=14)
plt.ylabel("Pearson correlation coefficient", fontsize=16)
#plt.title("Correlations between PCA Flow Metrics and # Dams", fontsize=18, wrap=True)
plt.tight_layout()
plt.savefig(os.path.join(outputDir, "dams_pca.png"))
plt.show()

