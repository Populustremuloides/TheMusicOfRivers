import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.pyplot import figure
import os

generateMonths = False
lessThanYear = False

predictorToCategory = {
        "LINKNO":"other",
        "quality":"data quality",
        "strmOrder":"size",
        "Magnitude":"size",
        "strmDrop":"hydrography",
        "WSNO":"other",
        "length_km":"size",
        "area_sqkm":"size",
        "drain_den":"hydrography",
        "gelev_m":"hydrography",
        "garea_sqkm":"size",
        "gord":"size",
        "PathLength":"size",
        "TotalLength":"size",
        "yr10data":"data quality",
        "yr15data":"data quality",
        "MeanTemp01":"climate",
        "MeanTemp02":"climate",
        "MeanTemp03":"climate",
        "MeanTemp04":"climate",
        "MeanTemp05":"climate",
        "MeanTemp06":"climate",
        "MeanTemp07":"climate",
        "MeanTemp08":"climate",
        "MeanTemp09":"climate",
        "MeanTemp10":"climate",
        "MeanTemp11":"climate",
        "MeanTemp12":"climate",
        "MeanTempAnn":"climate",

        "MeanPrec01":"climate",
        "MeanPrec02":"climate",
        "MeanPrec03":"climate",
        "MeanPrec04":"climate",
        "MeanPrec05":"climate",
        "MeanPrec06":"climate",
        "MeanPrec07":"climate",
        "MeanPrec08":"climate",
        "MeanPrec09":"climate",
        "MeanPrec10":"climate",
        "MeanPrec11":"climate",
        "MeanPrec12":"climate",
        "MeanPrecAnn":"climate",

        "CumPrec01":"size",
        "CumPrec02":"size",
        "CumPrec03":"size",
        "CumPrec04":"size",
        "CumPrec05":"size",
        "CumPrec06":"size",
        "CumPrec07":"size",
        "CumPrec08":"size",
        "CumPrec09":"size",
        "CumPrec10":"size",
        "CumPrec11":"size",
        "CumPrec12":"size",
        "CumPrecTotal":"size",
        
        "bio1":"climate",
        "bio2":"climate",
        "bio3":"climate",
        "bio4":"climate",
        "bio5":"climate",
        "bio6":"climate",
        "bio7":"climate",
        "bio8":"climate",
        "bio9":"climate",
        "bio10":"climate",
        "bio11":"climate",
        "bio12":"climate",
        "bio13":"climate",
        "bio14":"climate",
        "bio15":"climate",
        "bio16":"climate",
        "bio17":"climate",
        "bio18":"climate",
        "bio19":"climate",

        "FEOW_ID":"other",
        "ID":"other",

        "Ecoregion_Name":"region",
        
        "cls1":"land cover",
        "cls2":"land cover",
        "cls3":"land cover",
        "cls4":"land cover",
        "cls5":"land cover",
        "cls6":"land cover",
        "cls7":"human footprint",
        "cls8":"land cover",
        "cls9":"human footprint",
        "cls10":"land cover",
        "cls11":"land cover",
        "cls12":"land cover",
        "cls1":"land cover",

        "Dam_SurfaceArea":"dams",
        "Dam_Count":"dams",
        "HydroLakes_Area_sqkm":"size",
        
        "MeanPopden_2000":"human footprint",
        "MeanPopden_2005":"human footprint",
        "MeanPopden_2010":"human footprint",
        "MeanPopden_2015":"human footprint",

        "MeanHumanFootprint":"human footprint",
        
        "meanPercentDC_Imperfectly":"data quality",
        "meanPercentDC_ModeratelyWell":"data quality",
        "meanPercentDC_ModeratelyWell":"data quality",  
        "meanPercentDC_Poor":"data quality",
        "meanPercentDC_SomewhatExcessive":"data quality",
        "meanPercentDC_VeryPoor":"data quality",
        "meanPercentDC_Well":"data quality",

        "Continent":"region",

        "BIOME":"region",
        "ECO_NAME":"region",
        "tempcv":"climate",
        "precipcv":"climate",
        "forest":"land cover",
        "otherveg":"land cover",
        "human":"human footprint",
        "water":"size",#"water",
        "damareaN":"dams",
        "damcountN":"dams",
        "strmsize":"size"
}


numFound = 0
for dfile in os.listdir():
    if dfile.startswith("ml_feature_importances_short"):
        df = pd.read_csv(dfile)
        if numFound == 0:
            bigDf = df
        if numFound > 0:
            bigDf = bigDf.append(df)

        numFound += 1
    if numFound >= 1:
        break
        #print(dfile)

category = []
timePeriod = []
for index, row in bigDf.iterrows():
    category.append(predictorToCategory[row["feature"]])
    if row["period"] < 40:
        #timePeriod.append("1: < 1 month")
        timePeriod.append("1")
    elif row["period"] < 180:
        #timePeriod.append("2: < several months")
        timePeriod.append("2")
    elif row["period"] < 365:
        #timePeriod.append("3: < 1 year")
        timePeriod.append("3")
    elif row["period"] < 1095:
        #timePeriod.append("4: < 3 years")
        timePeriod.append("4")
    elif row["period"] < 2190:
        #timePeriod.append("5: < 6 years")
        timePeriod.append("5")
    elif row["period"] < 10000:
        #timePeriod.append("6: < 10 years")
        timePeriod.append("6")
    else:
        print("error")
        print(row["period"])


bigDf["cateogry"] = category
bigDf["time_period"] = timePeriod

print(bigDf)
bigDf = bigDf[(bigDf["trial_no"] % 3) != 2] # remove the DTR models
print(bigDf)

bigDf.to_csv("ml_importances_with_categories.csv", index=False)
#print(bigDf)
