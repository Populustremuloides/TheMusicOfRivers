import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor

import random
from scipy import stats
import matplotlib.pyplot as plt
import time
removeSparse = True
copyNo = 0

df = pd.read_csv("universallyAligned_powers.csv")
df.index = df[df.columns[0]]
df = df.drop(df.columns[0], axis=1)
df = df.transpose()
df["grdc_no"] = df.index
print(df)
#quit()

cdf = pd.read_csv("alldata_hemisphereCorrected.csv")


# keep track of which columns have a lot of NaN values
tooSparseColumns = []
for column in cdf:
    num = np.sum(cdf[column].isna())
    if num > 500:
        tooSparseColumns.append(column)
    #print(str(column) + " " + str(num))

for column in cdf:
    column1 = column.replace("_","")
    if type(cdf[column][0]) == type("string") and column1.isalpha():
        codes, uniques = pd.factorize(cdf[column])
        cdf[column] = codes
        print(cdf[column])
#quit()

xcats = []
for cat in cdf["grdc_no"]:
    try:
        xcats.append("X" + str(int(cat))) 
    except:
        xcats.append(None)
cdf["grdc_no"] = xcats

df = df.merge(cdf, on="grdc_no")
print(df)


# normalize each column

#predictors = list(df.columns[1299:1413])

predictors = list(df.columns[1299:1413])

if removeSparse:
    predictors = set(predictors)
    tooSparseColumns = set(tooSparseColumns)
    predictors = list(predictors.difference(tooSparseColumns))
    tooSparseColumns = list(tooSparseColumns)

def splitTestTrain(data, seed1, seed2):
    random.seed(seed1 + seed2 + copyNo) # ensure different selections between periods, but consistent between runs
    
    nSamples, nFeatures = data.shape
    
    eightyPercent = int(0.8 * nSamples)
    indices = list(range(nSamples))
    random.shuffle(indices)
    
    train = indices[:eightyPercent]
    test = indices[eightyPercent:]
    
    return data[test], data[train]

def splitIntoXY(data):
    y = data[:,0]
    x = data[:,1:]
    return x, y


shortDict = {
        "period":[],
        "feature":[],
        "importancel":[],
        "trial_no":[]
        }
wideDict = {"period":[]}

rSquaredDict = {
        "trialNo":[],
        "period":[],
        "n_total":[],
        "n_validation":[],
        "n_test":[],
        "r_squared":[],
        "model_type":[]
        }

secondsTotal = time.time()
#seconds1 = time.time()
#seconds2 = time.time()

for trialNo in range(0,6):
    for i in range(0,1101):
        seconds1 = time.time()            
        #try:
        if True:
            # drop everything except the X and Y values
            period = [df.columns[i]]
            keepers = period + predictors     
    

            df1 = df.filter(keepers)
            df1 = df1.dropna()

            print("trial no: " + str(trialNo) + ". col: "  + str(df.columns[i]))

            scaler = StandardScaler()
            #print(df1.to_numpy().shape)
            #dataMatrix = scaler.fit_transform(X=df1.to_numpy())
            dataMatrix = df1.to_numpy()

            # split into train, test
            test, train = splitTestTrain(dataMatrix, i, trialNo)

            # split into X and Y 
            testX, testY = splitIntoXY(test)
            trainX, trainY = splitIntoXY(train)
            
            if trialNo % 3 == 0:
                model = GradientBoostingRegressor(n_estimators = 100)
                modelType = "GBR"
            elif trialNo % 3 == 1:
                model = RandomForestRegressor(n_estimators = 100)
                modelType = "RFR"
            elif trialNo % 3 == 2:
                model = DecisionTreeRegressor()
                modelType = "DTR"

            model.fit(trainX, trainY)
            importances = model.feature_importances_
            
            wideDict["period"].append(period[0])
            for j in range(len(importances)):
                importance = importances[j]
                feature = predictors[j]
                if feature not in wideDict.keys():
                    wideDict[feature] = []
                wideDict[feature].append(importance)
            
            for j in range(len(importances)):
                importance = importances[j]
                feature = predictors[j]

                shortDict["period"].append(period[0])
                shortDict["feature"].append(feature)
                shortDict["importancel"].append(importance)
                shortDict["trial_no"].append(trialNo)

            yHat = model.predict(testX) 
            
            slope, intercept, rValue, pValue, stdErr = stats.linregress(yHat,testY)

            rSquared = rValue * rValue
            rSquaredDict["trialNo"].append(trialNo)
            rSquaredDict["period"].append(period[0])
            rSquaredDict["r_squared"].append(rSquared)
            rSquaredDict["model_type"].append(modelType)
            rSquaredDict["n_total"].append(df1.shape[0])
            rSquaredDict["n_validation"].append(test.shape[0])
            rSquaredDict["n_test"].append(train.shape[0])

            print("r_squared: " + str(rSquared))

        #except:
        #    print("error")
        seconds2 = time.time()
        print("time")
        print(seconds2 - seconds1)

    shortDf = pd.DataFrame.from_dict(shortDict)
    wideDf = pd.DataFrame.from_dict(wideDict)
    rSquaredDf = pd.DataFrame.from_dict(rSquaredDict)

    shortDf.to_csv("ml_feature_importances_short.csv")
    wideDf.to_csv("ml_feature_importances_wide.csv")
    rSquaredDf.to_csv("ml_r_squared.csv")

print(secondsTotal)
#1299 - 1492
#for i in range(len(df.columns)):
#    print(str(i) + " " + str(df.columns[i]))

#quit()

# for each frequency
# grab all the predictors
# split into test/train
# train
# test
# grab importances

print(df)
print(cdf)



