import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

i = 0
for ifile in os.listdir():
    if ifile.startswith("ml_predict_flow_metrics_feature_importances_wide"):
        if ifile != "ml_predict_flow_metrics_feature_importances_wide.csv":
            print(ifile)
            if i == 0:
                bigDf = pd.read_csv(ifile)
            else:
                df = pd.read_csv(ifile)
                bigDf = bigDf.append(df)
        i = i + 1
print(bigDf)

# make the importances figure:
flowMetrics = set(list(bigDf["flow_metric"]))
for metric in flowMetrics:
    df = bigDf[bigDf["flow_metric"] == metric]
    df = df[df.columns[3:]]
    periods = list(df.columns)
    means = list(df.mean())
    
    for i in range(len(periods)):
        periods[i] = float(periods[i])
        means[i] = float(means[i])
    plt.plot(periods, means, c="k", alpha=0.5)

plt.title("feature importances vs. timescales")
plt.xlabel("period (days)")
plt.ylabel("importance")
plt.show()

    
# now do a similar thing with the p values and r-squareds
i = 0
for ifile in os.listdir():
    
    if ifile.startswith("ml_predict_flow_metrics_r_squared"):
        if ifile != "ml_predict_flow_metrics_r_squared.csv":
            if i == 0:
                bigDf = pd.read_csv(ifile)
            else:
                df = pd.read_csv(ifile)
                bigDf = bigDf.append(df)
        i = i + 1
        
print(bigDf)
bigDf = bigDf[bigDf["model_type"] != "DTR"]
print(bigDf)
print("number of metrics captured")
print(len(list(set(bigDf["flow_metric"]))))

print(np.mean(bigDf["r_squared"]))

#bigDf = bigDf[bigDf["r_squared"] > 0.1]
# make the importances figure:
numOriginal = float(len(bigDf["p_value"]))

proportions = []
thresholds = []
for i in range(350):
    diviser = 10 ** i
    threshold = 1 / diviser
    thresholds.append(threshold)
print(thresholds)

for threshold in thresholds:
    df = bigDf[bigDf["p_value"] < threshold]
    numLeft = float(len(df["p_value"]))
    proportionLeft = numLeft / numOriginal
    print(proportionLeft)
    proportions.append(proportionLeft)

plt.plot(thresholds, proportions)
plt.xscale('log')
plt.xlabel("p value threshold")
plt.ylabel("proportion")
plt.title("proportion of streamflow metrics with r-squareds below thresholds")
plt.show()



plt.hist(bigDf["r_squared"], bins=100)
plt.title("distribution of model r-squareds")
plt.xlabel("r-squared")
plt.ylabel("count")
plt.show()


numOriginal = float(len(bigDf["r_squared"]))

proportions = []
thresholds = []
for i in range(1000):
    thresholds.append(i * 0.001)
print(thresholds)

for threshold in thresholds:
    df = bigDf[bigDf["r_squared"] > threshold]
    numLeft = float(len(df["r_squared"]))
    proportionLeft = numLeft / numOriginal
    print(proportionLeft)
    proportions.append(proportionLeft)

plt.plot(thresholds, proportions)
#plt.xscale('log')
plt.xlabel("r squared threshold")
plt.ylabel("proportion")
plt.title("proportion of streamflow metrics with r-squareds above threshold")
plt.show()
print("mean r-squared value: " + str(np.mean(bigDf["r_squared"])))



