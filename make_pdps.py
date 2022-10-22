from matplotlib import pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import KFold
from data import *
from scipy import stats
import os

def writeImportances(importances, index, columns, target, modelType, outputFolder):
    ''' take the column importances and save them to a csv file '''

    colsToImportances = dict(zip(columns, importances))

    cols = list(colsToImportances.keys())
    imps = list(colsToImportances.values())

    cols = [str(col) for col in cols]
    imps = [str(imp) for imp in imps]
    colsStr = ",".join(cols)
    impsStr = ",".join(imps)

    fileName = outputFolder + "/columnImportances_metric_" + str(target) + "_" + modelType + ".csv"

    if index == 0:
        with open(fileName, "w+") as importanceFile:
            importanceFile.write(colsStr + str("\n"))

    with open(fileName, "a+") as importanceFile:
        importanceFile.write(impsStr + str("\n"))


def run(model, target, logfile, modelType, outputFolder):
    print('Using model: {}'.format(model), file=logfile)
    df = get_data(for_training=True, pcaMetric=target)

    targetName = "Metric" + str(target)

    kfolds = get_folds(df, 10)
    test_preds_total = []
    test_ys_total = []
    for f_ind, fold in enumerate(kfolds):  # for each fold

        training, testing = preprocess(pd.concat(kfolds[:f_ind] + kfolds[f_ind + 1:]), fold)

        X_train, y_train = training.drop(targetName, axis=1), training[targetName]
        X_test, y_test = testing.drop(targetName, axis=1), testing[targetName]

        model.fit(X_train, y_train)
        pred_train = model.predict(X_train)
        pred_test = model.predict(X_test)
        L1_tr = np.average(np.abs(np.subtract(pred_train, y_train.values.ravel())))
        L1_ts = np.average(np.abs(np.subtract(pred_test, y_test.values.ravel())))

        test_preds_total = np.append(test_preds_total, pred_test)
        test_ys_total = np.append(test_ys_total, y_test.values.ravel())
        print('fold {}: trL1: {} tsL1: {}'.format(f_ind+1, round(L1_tr, 3), round(L1_ts, 3)), file=logfile)

        imp = model.feature_importances_
        cols = list(X_test.columns)
        writeImportances(imp, f_ind, cols, target, modelType, outputFolder)
        inds = np.argsort(imp)[::-1]

        cols = list(X_test.columns)
        impToCols = dict(zip(imp, cols))
        #print(imp)
        imp.sort()
        imp = list(imp)
        imp.reverse()
        #for importance in imp:
        #    print(str(importance) + ": " + str(impToCols[importance]))


    print(test_preds_total)
    print(test_ys_total)
    r, p = stats.pearsonr(test_preds_total, test_ys_total)
    plt.scatter(x=test_preds_total, y=test_ys_total, alpha=0.5)
    plt.title(str(r * r))
    plt.show()
    print('r_squared {}'.format(r * r), file=logfile)


if __name__ == '__main__':

    outputFolder = "output_new"
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)

    model1 = GradientBoostingRegressor(n_estimators=100) # did the best so far
    modelType1 = "GBR"
    model2 = RandomForestRegressor(random_state=0, n_estimators=100)  # Keeper
    modelType2 = "RFR"
    model3 = DecisionTreeRegressor(random_state=0)
    modelType3 = "DTR"
    models = [model1, model2, model3]
    modelTypes = [modelType1, modelType2, modelType3]

    for i in range(len(models)):
        model = models[i]
        modelType = modelTypes[i]
        for target in range(1,8):
            logfilename = outputFolder + '/{}_{}_zlog.txt'.format(target, modelType)
            with open(logfilename, 'w+') as logfile:
                run(model, target, logfile, modelType, outputFolder)
