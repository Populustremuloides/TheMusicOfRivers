import pandas as pd
import os
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
import copy
data_path = ''
targets = ['Metric1', 'Metric2', 'Metric3', 'Metric4', 'Metric5', 'Metric6', 'Metric7']


def get_data(for_training=False, pcaMetric=1):
    with open(os.path.join(data_path, 'alldata_hemisphereCorrected.csv'), 'r') as data_file:
        df = pd.read_csv(data_file)

    if for_training:

        targetsToDrop = targets[0:pcaMetric - 1] + targets[pcaMetric:]
        targetToKeep = targets[pcaMetric - 1]
        df = df.dropna(subset=[targetToKeep]) # if no target, drop
        df = df.drop(targetsToDrop, axis=1)

        return df


    else:
        return df

def numerifyCategory(data):
    data = copy.deepcopy(data)
    ''' converts a pandas dataframe of categorical variables into a pandas dataframe of numerical values '''

    for column in list(data.columns):
        categories = list(set(data[column]))
        indices = range(len(categories))
        categoryToIndex = dict(zip(categories, indices))
        newList = []
        for datum in list(data[column]):
            datumIndex = categoryToIndex[datum]
            newList.append(datumIndex)

        data[column] = newList

    return data



def preprocess(train, valid):

    # separate out the categorical variables (obj_train and obj_valid)
    train, obj_train = train.select_dtypes(exclude=['object']), train.select_dtypes(['object'])
    valid, obj_valid = valid.select_dtypes(exclude=['object']), valid.select_dtypes(['object'])

    # impute with median
    imputer = SimpleImputer(strategy='median')
    imp_train = pd.DataFrame(imputer.fit_transform(train))
    imp_train.columns = train.columns
    imp_train.index = train.index
    imp_valid = pd.DataFrame(imputer.transform(valid))
    imp_valid.columns = valid.columns
    imp_valid.index = valid.index

    imp_train_norm = ((imp_train - imp_train.min()) / (imp_train.max() - imp_train.min()))  # norm train 0-1
    imp_valid_norm = ((imp_valid - imp_train.min()) / (imp_train.max() - imp_train.min()))  # norm valid according to train

    # convert obj_train to categorical variables

    obj_train = numerifyCategory(obj_train)
    obj_valid = numerifyCategory(obj_valid)

    imp_train_norm = pd.concat([imp_train_norm, obj_train], axis=1)
    imp_valid_norm = pd.concat([imp_valid_norm, obj_valid], axis=1)

    return imp_train_norm, imp_valid_norm


def get_folds(data, k):
    #unique_sites = set(data['site'])  # get unique sites
    indexNums = list(data[data.columns[0]])
    groups = list(set([index % k for index in indexNums]))
    data = data.drop(data.columns[0], axis=1)
    #print(data)
    #print(list(data.index))

    kfolds = []
    for group in groups:
        indexList = [] #list(data.index)
        for index in data.index:
            if index % k == group:
                indexList.append(True)
            else:
                indexList.append(False)

        groupData = data.loc[indexList]
        kfolds.append(groupData)

    return kfolds


