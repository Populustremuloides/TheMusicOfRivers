import pandas as pd
from scipy.stats.stats import pearsonr
import seaborn as sns
import matplotlib.pyplot as plt
# Read in the metric information
import numpy as np

# Read in the wavelet transform information

flowPeriodsPath = "universallyAligned_powers.csv"
df = pd.read_csv(flowPeriodsPath)
scale = df["scale"]
df = df.drop("scale", axis=1)
df = df.transpose()
corrDf = df.corr()
sns.heatmap(corrDf, center=0, vmin=-1, vmax=1, square=True)
plt.title("Correlation between Spectral Powers of Different Frequencies", wrap=True)
plt.ylabel("period length (days)")
plt.xlabel("period length (days)")
plt.tight_layout()
plt.show()

quit()

def getCorrelationMatrix(df):
    metricToPeriodCorrelations = {}
    i = 0
    for period1 in periods:
        periodVals1 = list(df[period1])
        correlations = []
        for period2 in periods:
            periodVals2 = list(df[period2])
            correlation, pVal = pearsonr(periodVals1, periodVals2)
            correlations.append(correlation)
        if i % 100 == 0:
            print(period1)
        metricToPeriodCorrelations[period1] = correlations
        i = i + 1

    shortPeriods = [int(round(float(x))) for x in periods]
    metricToPeriodDF = pd.DataFrame.from_dict(metricToPeriodCorrelations, orient="index", columns=shortPeriods)
    return metricToPeriodDF

