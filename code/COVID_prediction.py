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
#import catboost as cb
import scipy


# feature box 特征箱型图
def feature_box(df, feature):
    for i in feature:
        print(i)
        df[i].plot(kind='box')
        plt.show()


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

    figsize = 12, 9
    figure, ax = plt.subplots(figsize=figsize)
    color = ['limegreen', 'mediumslateblue', 'dodgerblue', 'darkorange']
    marker = ['X', 'o', 'd', '<']

    plt.scatter(real_y, prediction_y, c=color[0], marker=marker[1], label='', s=100, alpha=0.7, zorder=20)
    plt.plot([0, 50000], [0, 50000], '--', color='black', label='', linewidth=1.0)

    ############# 设置坐标刻度值的大小以及刻度值的字体 #############
    #plt.xlim(0, 2000)
    #plt.ylim(0, 2000)
    plt.xlim(0, 800)
    plt.ylim(0, 800)
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


# 所有城市疫情建模
def covid_all_predict(df):

    real_y = []
    prediction_y = []

    kf = KFold(3, False, random_state=123)
    index = []
    for train_index, test_index in kf.split(df):
        index.append((train_index, test_index))

    clf = [RandomForestRegressor(n_estimators=8, min_samples_split=5, max_depth=5),
           RandomForestRegressor(n_estimators=8, min_samples_split=5, max_depth=5),
           RandomForestRegressor(n_estimators=8, min_samples_split=5, max_depth=5)]

    for i in range(len(index)):

        train_df = df.iloc[index[i][0], :]
        test_df = df.iloc[index[i][1], :]

        #train_y = train_df['confirmed']
        #train_y = train_df['confirmed_before']
        train_y = train_df['confirmed_after']

        #train_y = train_df['dead']
        #train_x = train_df.drop(['id', 'location', 'confirmed', 'cured', 'dead'], axis=1)
        #train_x = train_df.drop(['id', 'location', 'confirmed_before', 'cured_before', 'dead_before'], axis=1)
        train_x = train_df.drop(['id', 'location', 'confirmed_after', 'cured_after', 'dead_after'], axis=1)


        #test_y = test_df['confirmed']
        #test_y = test_df['confirmed_before']
        test_y = test_df['confirmed_after']
        #test_y = test_df['dead']
        #test_x = test_df.drop(['id', 'location', 'confirmed', 'cured', 'dead'], axis=1)
        #test_x = test_df.drop(['id', 'location', 'confirmed_before', 'cured_before', 'dead_before'], axis=1)
        test_x = test_df.drop(['id', 'location', 'confirmed_after', 'cured_after', 'dead_after'], axis=1)


        clf[i].fit(train_x, train_y)
        predict_y = clf[i].predict(test_x)

        real_y.extend(test_y)
        prediction_y.extend(predict_y)

        print("train fold " + str(i+1))
        evaluation(train_y, clf[i].predict(train_x))

        print("test fold " + str(i+1))
        evaluation(test_y, predict_y)

    print("************* cv evaluation ***************")
    evaluation(real_y, prediction_y)

    # feature importance
    #train_y = df['confirmed']
    #train_y = df['confirmed_before']
    train_y = df['confirmed_after']
    # train_y = train_df['dead']
    #train_x = df.drop(['id', 'location', 'confirmed', 'cured', 'dead'], axis=1)
    #train_x = df.drop(['id', 'location', 'confirmed_before', 'cured_before', 'dead_before'], axis=1)
    train_x = df.drop(['id', 'location', 'confirmed_after', 'cured_after', 'dead_after'], axis=1)


    clf = RandomForestRegressor(n_estimators=10)
    clf.fit(train_x, train_y)

    features = list(train_x)
    importances = clf.feature_importances_
    indices = np.argsort(importances)
    feture_importance(features, indices, importances)
    aaaaaa

# 分时间段建模疫情
def covid_control_date_predict(df):
    pass


# 湖北外其他城市建模疫情
def covid_predict_except_hubei(df):
    pass



def get_feature_final():
    # 1000 hPa relative humidity
    rh = pd.read_csv("../data/ECMWF/zonal_statistics/city_rh_final.csv")

    # 2m temperature
    t2m = pd.read_csv("../data/ECMWF/zonal_statistics/city_t2m_final.csv")

    # rh t2m
    df_all = pd.merge(rh, t2m, how='inner', on='id')

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
    print(len(df_all))

    # add moveOut from Wuhan
    moveIn_sum = pd.read_csv("../data/baidu_migration/city_migration_in_from_WuHan_sum.csv")
    moveIn_sum = moveIn_sum.drop(['name', 'province_id'], axis=1)
    df_all = pd.merge(df_all, moveIn_sum, how='left', on='city_baidu_id')
    df_all = df_all.fillna(0)
    df_all = df_all.drop_duplicates()

    import collections
    print([item for item, count in collections.Counter(df_all['id']).items() if count > 1])

    # add moveOut from Wuhan
    moveOut_sum = pd.read_csv("../data/baidu_migration/city_migration_out_from_WuHan_sum.csv")
    moveOut_sum = moveOut_sum.drop(['name', 'province_id'], axis=1)
    df_all = pd.merge(df_all, moveOut_sum, how='left', on='city_baidu_id')
    df_all = df_all.fillna(0)
    df_all = df_all.drop_duplicates()

    df_all.to_csv("../output/COVID_final.csv", index=False)

# main
if __name__ == '__main__':

    #get_feature_final()

    #df_all = pd.read_csv("../output/COVID.csv")
    #df = shuffle(df_all)

    df_all = pd.read_csv("../output/COVID_final.csv")
    df_all = shuffle(df_all)

    epidemicIds = [420100, 420200, 420300, 420500, 420600, 420700, 420800, 420900,
                   421000, 421100, 421200, 421300, 422800, 429005, 429004, 429006, 429021]

    feature = ['rh_mean', 'rh_max', 'rh_min', 't2m_mean', 't2m_max', 't2m_min',
                 'confirmed', 'cured', 'dead',
                 'moveIn_index_sum', 'moveIn_index_max', 'moveIn_index_min',
                 'moveOut_index_sum', 'moveOut_index_max', 'moveOut_index_min',
                 'travel_index_sum', 'travel_index_max', 'travel_index_min',
                 '420100_moveIn_sum', '420100_moveOut_sum']

    df = df_all[['id', 'location',
                 'rh_mean', 'rh_max', 'rh_min', 't2m_mean', 't2m_max', 't2m_min',
                 'confirmed', 'cured', 'dead',
                 'moveIn_index_sum', 'moveIn_index_max', 'moveIn_index_min',
                 'moveOut_index_sum', 'moveOut_index_max', 'moveOut_index_min',
                 'travel_index_sum', 'travel_index_max', 'travel_index_min',
                 '420100_moveIn_sum', '420100_moveOut_sum']]

    df = df_all[['id', 'location', 'rh_mean_before', 'rh_max_before', 'rh_min_before', 't2m_mean_before',
                 't2m_max_before', 't2m_min_before', 'confirmed_before', 'cured_before', 'dead_before',
                 'moveIn_index_sum_before',
                 'moveIn_index_max_before', 'moveIn_index_min_before', 'moveOut_index_sum_before',
                 'moveOut_index_max_before',
                 'moveOut_index_min_before', 'travel_index_sum_before', 'travel_index_max_before',
                 'travel_index_min_before',
                 '420100_moveIn_sum_before', '420100_moveOut_sum_before']]

    df = df_all[['id', 'location', 'rh_mean_after', 'rh_max_after', 'rh_min_after', 't2m_mean_after',
                 't2m_max_after', 't2m_min_after', 'confirmed_after', 'cured_after', 'dead_after',
                 'moveIn_index_sum_after',
                 'moveIn_index_max_after', 'moveIn_index_min_after', 'moveOut_index_sum_after',
                 'moveOut_index_max_after',
                 'moveOut_index_min_after', 'travel_index_sum_after', 'travel_index_max_after',
                 'travel_index_min_after',
                 '420100_moveIn_sum_after', '420100_moveOut_sum_after']]


    #feature_box(df, feature)

    df = df[~df['id'].isin(epidemicIds)]

    covid_all_predict(df)