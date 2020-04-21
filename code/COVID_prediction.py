# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
整合所有的特征和疫情数据，利用随机森林等机器学方法建模预测
"""

import pandas as pd
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error #均方误差
from sklearn.metrics import mean_absolute_error #平方绝对误差
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold
import scipy
import math


# feature importance 特征重要性
def feture_importance(features, indices, importances):

    print("%%%%%% feature importances %%%%%%")

    '''
    for i in indices:
        print(features[i], importances[i])
    '''

    plt.barh(range(len(indices)), importances[indices], color='b', align='center', alpha=0.5)
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('feature Importance')
    plt.show()


# 评价指标
def evaluation(real_y, prediction_y):

    # rmse  mae r2
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(real_y, prediction_y)
    print("R-squared", r_value**2)
    print("R", r_value)

    mae = mean_absolute_error(real_y, prediction_y)
    print("mae", mae)

    rmse = mean_squared_error(real_y, prediction_y) ** 0.5
    print("rmse", rmse)


    figsize = 12, 8
    figure, ax = plt.subplots(figsize=figsize)

    plt.scatter(real_y, prediction_y, c='g', marker='o', label='', s=20, alpha=0.7, zorder=20)
    plt.plot([0, 50000], [0, 50000], '--', color='black', label='', linewidth=1.0)

    ############# 设置坐标刻度值的大小以及刻度值的字体 #############
    plt.xlim(0, 4000)
    plt.ylim(0, 4000)
    plt.tick_params(labelsize=25)

    labels = ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]

    labels = ax.get_xticklabels()
    [label.set_fontname('Times New Roman') for label in labels]

    ############# 设置图例并且设置图例的字体及大小 #############
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 25,
             }

    plt.ylabel('prediction', font1)
    plt.xlabel('real', font1)
    ax = plt.gca()
    ax.set_aspect(1)
    plt.show()


# 全时间段疫情建模
def covid_all_predict(df):

    real_y = []
    prediction_y = []

    kf = KFold(3, True)
    index = []
    for train_index, test_index in kf.split(df):
        index.append((train_index, test_index))

    clf = [RandomForestRegressor(n_estimators=10, min_samples_split=5, max_depth=5),
           RandomForestRegressor(n_estimators=10, min_samples_split=5, max_depth=5),
           RandomForestRegressor(n_estimators=10, min_samples_split=5, max_depth=5)]

    for i in range(len(index)):

        train_df = df.iloc[index[i][0], :]
        test_df = df.iloc[index[i][1], :]

        train_y_log = train_df['confirmed_log']
        train_y = train_df['confirmed']

        train_x = train_df.drop(['id', 'location', 'confirmed_log', 'confirmed', 'cured', 'dead'], axis=1)

        test_y = test_df['confirmed']
        test_x = test_df.drop(['id', 'location', 'confirmed_log', 'confirmed', 'cured', 'dead'], axis=1)

        clf[i].fit(train_x, train_y_log)

        predict_ytrain_log = clf[i].predict(train_x)
        predict_ytrain = np.trunc(np.exp(predict_ytrain_log) - 1)

        predict_ytest_log = clf[i].predict(test_x)
        predict_ytest = np.trunc(np.exp(predict_ytest_log) - 1)

        real_y.extend(test_y)
        prediction_y.extend(predict_ytest)

        print("train fold " + str(i+1))
        evaluation(train_y, predict_ytrain)

        print("test fold " + str(i+1))
        evaluation(test_y, predict_ytest)


    print("************* cv evaluation ***************")
    evaluation(real_y, prediction_y)

    for i, j in zip(real_y, prediction_y):
        if abs(i-j)>100:
            print(i, j)

    # feature importance
    train_y = df['confirmed_log']
    train_x = df.drop(['id', 'location', 'confirmed_log', 'confirmed', 'cured', 'dead'], axis=1)

    clf = RandomForestRegressor(n_estimators=10, min_samples_split=5, max_depth=5)
    clf.fit(train_x, train_y)

    features = list(train_x)
    importances = clf.feature_importances_
    indices = np.argsort(importances)
    feture_importance(features, indices, importances)

def get_feature_final():
    # 1000 hPa relative humidity
    rh = pd.read_csv("../data/ECMWF/zonal_statistics/city_rh_final.csv")

    # 2m temperature
    t2m = pd.read_csv("../data/ECMWF/zonal_statistics/city_t2m_final.csv")

    # npp
    npp = pd.read_csv("../data/npp/city_npp.csv")

    # rh t2m npp
    df_all = pd.merge(rh, t2m, how='inner', on='id')
    df_all = pd.merge(df_all, npp, how='left', on='id')


    # covid
    covid = pd.read_csv("../output/COVID_city_distinct.csv")

    # merge covid 缺失表示无疫情相关，用0替代
    df_all = pd.merge(df_all, covid, how='left', on='id')
    df_all = df_all.fillna(0)

    # add city_baidu_id
    china_location_id = pd.read_csv("../data/china_location_id_2015.csv")
    china_location_id = china_location_id[['id', 'city_baidu_id']]
    df_all = pd.merge(df_all, china_location_id, how='left', on='id')


    # 增加迁入迁徙规模指数、迁出迁徙规模指数和城内出行强度
    moveIn = pd.read_csv("../data/baidu_migration/city_migration.csv")
    df_all = pd.merge(df_all, moveIn, how='left', on='city_baidu_id')
    df_all = df_all.fillna(0)


    # add moveOut from Wuhan
    moveIn_sum = pd.read_csv("../data/baidu_migration/city_migration_in_from_WuHan_sum.csv")
    moveIn_sum = moveIn_sum.drop(['name', 'province_id'], axis=1)
    df_all = pd.merge(df_all, moveIn_sum, how='left', on='city_baidu_id')
    df_all = df_all.fillna(0)
    df_all = df_all.drop_duplicates()

    import collections
    print([item for item, count in collections.Counter(df_all['id']).items() if count > 1])

    df_all.to_csv("../output/COVID_final.csv", index=False)


# main
if __name__ == '__main__':

    #get_feature_final()

    df_all = pd.read_csv("/Users/shaoqi/Desktop/COVID-19/output/COVID_final.csv")
    df_all = df_all[~df_all['id'].isin(['371200', '710000', '810000'])]  # 去除台湾、香港和莱芜
    df_all = shuffle(df_all)
    for i in df_all.columns.values:
        print(i)

    # 全时间段建模
    df = df_all[['id', 'location',
                 'rh_mean', 'rh_max', 'rh_min',
                 't2m_mean', 't2m_max', 't2m_min',
                 'confirmed', 'cured', 'dead',
                 'moveIn_index_mean', 'moveIn_index_max', 'moveIn_index_min',
                 'moveOut_index_mean', 'moveOut_index_max', 'moveOut_index_min',
                 'travel_index_mean', 'travel_index_max', 'travel_index_min',
                 '420100_moveIn_mean', '420100_moveIn_max', '420100_moveIn_min', 'npp']]

    # label做log处理
    confirmed = df['confirmed'].to_list()
    confirmed = [np.log(i+1) for i in confirmed]
    df.loc[:, 'confirmed_log'] = confirmed

    # epidemic id 疫情灾区id，暂定武汉
    epidemicIds = [420100]
    df = df[~df['id'].isin(epidemicIds)]
    covid_all_predict(df)

    aaaaaa


    # 管控前建模
    df_before = df_all[['id', 'location',
                        'rh_mean_before','rh_max_before','rh_min_before',
                        't2m_mean_before','t2m_max_before','t2m_min_before',
                        'confirmed_before','cured_before','dead_before',
                        'moveIn_index_mean_before','moveIn_index_max_before','moveIn_index_min_before',
                        'moveOut_index_mean_before','moveOut_index_max_before','moveOut_index_min_before',
                        'travel_index_mean_before','travel_index_max_before','travel_index_min_before',
                        '420100_moveIn_mean_before','420100_moveIn_max_before','420100_moveIn_min_before', 'npp']]

    confirmed = df_before['confirmed_before'].to_list()
    confirmed = [np.log(i + 1) for i in confirmed]
    df_before.loc[:, 'confirmed_before_log'] = confirmed

    covid_control_before_predict(df_before)

    # 管控后建模
    df_after = df_all[['id', 'location',
                        'rh_mean_after', 'rh_max_after', 'rh_min_after',
                        't2m_mean_after', 't2m_max_after', 't2m_min_after',
                        'confirmed_after', 'cured_after', 'dead_after',
                        'moveIn_index_mean_after', 'moveIn_index_max_after', 'moveIn_index_min_after',
                        'moveOut_index_mean_after', 'moveOut_index_max_after', 'moveOut_index_min_after',
                        'travel_index_mean_after', 'travel_index_max_after', 'travel_index_min_after',
                        '420100_moveIn_mean_after', '420100_moveIn_max_after', '420100_moveIn_min_after',
                        'npp']]

    confirmed = df_after['confirmed_after'].to_list()
    confirmed = [np.log(i + 1) for i in confirmed]
    df_after.loc[:, 'confirmed_after_log'] = confirmed
    covid_control_after_predict(df_after)