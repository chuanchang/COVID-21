# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
整合区县级所有的特征和疫情数据，利用随机森林等机器学方法建模预测
"""

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error #均方误差
from sklearn.metrics import mean_absolute_error #平方绝对误差
from sklearn.metrics import r2_score#R square
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import cross_val_score


def rf(df_all):

    x = df_all.drop(['id', 'confirmedNum', 'deathsNum', 'curesNum', 'city_baidu_id', 'location'], axis=1)
    y = df_all['deathsNum']

    print("###########################")
    print("7:3 train and test")

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

    clf = RandomForestRegressor(n_estimators=20)
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)

    print("-----------------")
    # rmse  mae r2
    r2 = r2_score(y_test, predict)
    print("R2", r2)

    mae = mean_absolute_error(y_test, predict)
    print("mae", mae)

    rmse = mean_squared_error(y_test, predict) ** 0.5
    print("rmse", rmse)


    features = list(x)
    importances = clf.feature_importances_
    indices = np.argsort(importances)

    print("%%%%%% feature importances %%%%%%")
    for i in indices:
        print(features[i], importances[i])

    plt.figure(1)
    plt.barh(range(len(indices)), importances[indices], color='b', align='center', alpha=0.5)
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.show()

    print("###########################")
    print("k fold cross validation k=10")
    rf = RandomForestRegressor(n_estimators=20)
    scores = cross_val_score(rf, x_train, y_train, cv=10, scoring='r2')
    print(scores)


# main
if __name__ == '__main__':

    # 1000 hPa relative humidity
    rh = pd.read_csv("../data/ECMWF/zonal_statistics/distinct_rh.csv")

    # 2m temperature
    t2m = pd.read_csv("../data/ECMWF/zonal_statistics/distinct_t2m.csv")

    # rh t2m
    df_all = pd.merge(rh, t2m, how='inner', on='id')

    # covid
    covid = pd.read_csv("../data/COVID19_distinct.csv")
    covid = covid[['id', 'confirmedNum', 'deathsNum', 'curesNum']]

    # merge covid 缺失表示区县无疫情相关，用0替代
    df_all = pd.merge(df_all, covid, how='left', on='id')
    df_all = df_all.fillna(0)

    china_location_id = pd.read_csv("../data/china_location_id_2015.csv")
    china_location_id = china_location_id[['id', 'city_baidu_id', 'location']]

    # add city_baidu_id
    df_all = pd.merge(df_all, china_location_id, how='left', on='id')

    # 增加迁入迁徙规模指数、迁出迁徙规模指数和城内出行强度
    moveIn = pd.read_csv("../data/baidu_migration/city_migration.csv")
    df_all = pd.merge(df_all, moveIn, how='left', on='city_baidu_id')
    df_all = df_all.fillna(0)
    id1 = set(df_all['id'].to_list())

    # add moveOut from Wuhan
    moveIn_sum = pd.read_csv("../data/baidu_migration/city_migration_in_from_WuHan_sum.csv")
    moveIn_sum = moveIn_sum[['city_baidu_id', 'moveIn_sum']]
    df_all = pd.merge(df_all, moveIn_sum, how='left', on='city_baidu_id')


    import collections

    print([item for item, count in collections.Counter(df_all['id']).items() if count > 1])


    # add moveOut from Wuhan
    moveOut_sum = pd.read_csv("../data/baidu_migration/city_migration_out_from_WuHan_sum.csv")
    moveOut_sum = moveOut_sum[['city_baidu_id', 'moveOut_sum']]
    df_all = pd.merge(df_all, moveOut_sum, how='left', on='city_baidu_id')
    df_all = df_all.fillna(0)
    df_all = df_all.drop_duplicates()

    df_all.to_csv("../output/COVID.csv", index=False)

    print("***********************")
    print("dataset size:")
    print(len(df_all))

    rf(df_all)


