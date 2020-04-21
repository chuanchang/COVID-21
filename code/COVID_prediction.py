# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
整合所有的特征和疫情数据，利用随机森林等机器学方法建模预测
"""

# load package
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
import geopandas as gp


threshold = 50

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

    # rmse  mae  r2  r
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(real_y, prediction_y)
    print("R-squared", r_value**2)
    print("R", r_value)

    mae = mean_absolute_error(real_y, prediction_y)
    print("mae", mae)

    rmse = mean_squared_error(real_y, prediction_y) ** 0.5
    print("rmse", rmse)

    ############# 设置图例并且设置图例的字体及大小 #############
    font1 = {'family': 'Times New Roman',
            'weight': 'normal',
            'size': 15,
            }
    
    figsize = 20,16
    figure, ax = plt.subplots(figsize=figsize)
    level = [50000, 5500, 1000, 200, 100, 80, 60, 40,20]
    for i in range(len(level)):

        plt.subplot(3,3,i+1)
        plt.scatter(real_y, prediction_y, c='b', marker='o', label='', s=10, alpha=0.7, zorder=20)
        plt.plot([0, 50000], [0, 50000], '--', color='black', label='', linewidth=1.0)
        
        ############# 设置坐标刻度值的大小以及刻度值的字体 #############
        plt.xlim(0, level[i])
        plt.ylim(0, level[i])
        plt.tick_params(labelsize=15)
        
        plt.ylabel('prediction', font1)
        plt.xlabel('real', font1)

        # x，y轴设置显示刻度一致
        ax = plt.gca()
        ax.set_aspect(1)
    
    plt.show()


# 全时间段疫情建模
def covid_all_predict(df, index):

    df = df[['id','location',
    'rhMean','rhMax','rhMin',
    't2mMean','t2mMax','t2mMin',
    'moveInMean','moveInMax','moveInMin',
    'moveOutMea','moveOutMax','moveOutMin',
    'travelMean','travelMax','travelMin',
    'WuhanMean','WuhanMax','WuhanMin',
    'confirmed','confirmLog','npp']]

    real_y = []
    prediction_y = []

    df_predict = []

    case = []

    clf = []
    for i in range(len(index)):
        clf.append(RandomForestRegressor(n_estimators=10, min_samples_split=5, max_depth=5))
    

    for i in range(len(index)):

        train_df = df.iloc[index[i][0], :]
        test_df = df.iloc[index[i][1], :]

        df_predict.extend(test_df['id'].to_list())

        train_y_log = train_df['confirmLog']
        train_y = train_df['confirmed']
        train_x = train_df.drop(['id', 'location', 'confirmLog', 'confirmed'], axis=1)

        test_y = test_df['confirmed']
        test_x = test_df.drop(['id', 'location', 'confirmLog', 'confirmed'], axis=1)

        clf[i].fit(train_x, train_y_log)

        predict_ytrain_log = clf[i].predict(train_x)
        predict_ytrain = np.trunc(np.exp(predict_ytrain_log) - 1)

        predict_ytest_log = clf[i].predict(test_x)
        predict_ytest = np.trunc(np.exp(predict_ytest_log) - 1)

        real_y.extend(test_y)
        prediction_y.extend(predict_ytest)

        print("train fold " + str(i+1))
        print("预测误差较大城市，绝对值误差阈值设置为" + str(threshold))
        predict_train_y = list(predict_ytrain)
        train_yy = train_y.to_list()
        for j in range(len(train_df)):
            if abs(train_yy[j]-predict_train_y[j])>threshold:
                print(train_df.iloc[j, 1] + "   real: " + str(train_yy[j]) + "   pre:" + str(predict_train_y[j]))
                case.append(train_df.iloc[j, 0])
        
        evaluation(train_y, predict_ytrain)


        print("#########################################")


        print("test fold " + str(i+1))
        print("预测误差较大城市，绝对值误差阈值设置为" + str(threshold))
        predict_test_y = list(predict_ytest)
        test_yy = test_y.to_list()
        for j in range(len(test_df)):
            if abs(test_yy[j]-predict_test_y[j])>threshold:
                print(test_df.iloc[j, 1] + "   real: " + str(test_yy[j]) + "   pre:" + str(predict_test_y[j]))
                case.append(test_df.iloc[j, 0])

        evaluation(test_y, predict_ytest)
    

    df_predict = pd.DataFrame(df_predict)
    df_predict.columns = ['id']
    df_predict['predict'] = prediction_y

    print("************* cv evaluation ***************")
    evaluation(real_y, prediction_y)

    # feature importance
    train_y = df['confirmLog']
    train_x = df.drop(['id', 'location', 'confirmLog', 'confirmed'], axis=1)

    clf = RandomForestRegressor(n_estimators=10, min_samples_split=5, max_depth=5)
    clf.fit(train_x, train_y)

    features = list(train_x)
    importances = clf.feature_importances_
    indices = np.argsort(importances)
    feture_importance(features, indices, importances)

    return case, df_predict

def get_feature_final():
    # 1000 hPa relative humidity
    rh = pd.read_csv("./data/ECMWF/zonal_statistics/city_rh_final.csv")

    # 2m temperature
    t2m = pd.read_csv("./data/ECMWF/zonal_statistics/city_t2m_final.csv")

    # npp
    npp = pd.read_csv("./data/npp/city_npp.csv")

    # rh t2m npp
    df_all = pd.merge(rh, t2m, how='inner', on='id')
    df_all = pd.merge(df_all, npp, how='left', on='id')

    # covid
    covid = pd.read_csv("./output/COVID_city_distinct.csv")

    # merge covid 缺失表示无疫情相关，用0替代
    df_all = pd.merge(df_all, covid, how='left', on='id')
    df_all = df_all.fillna(0)

    # 增加迁入迁徙规模指数、迁出迁徙规模指数和城内出行强度
    moveIn = pd.read_csv("./data/baidu_migration/city_migration.csv")
    df_all = pd.merge(df_all, moveIn, how='left', on='id')
    df_all = df_all.fillna(0)

    # add moveOut from Wuhan
    moveIn_sum = pd.read_csv("./data/baidu_migration/city_move_in_from_WuHan_sum.csv")
    moveIn_sum = moveIn_sum.drop(['name', 'city_baidu_id'], axis=1)
    df_all = pd.merge(df_all, moveIn_sum, how='left', on='id')
    df_all = df_all.fillna(0)
    df_all = df_all.drop_duplicates()

    # 去除台湾、香港和澳门
    df_all = df_all[~df_all['id'].isin(['710000', '810000', '820000'])]

    temp = df_all['confirmed'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'confirmed_log'] = temp

    temp = df_all['cured'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'cured_log'] = temp
    
    temp = df_all['dead'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'dead_log'] = temp


    temp = df_all['confirmed_before'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'confirmed_before_log'] = temp

    temp = df_all['cured_before'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'cured_before_log'] = temp
    
    temp = df_all['dead_before'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'dead_before_log'] = temp

    temp = df_all['confirmed_after'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'confirmed_after_log'] = temp

    temp = df_all['cured_after'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'cured_after_log'] = temp
    
    temp = df_all['dead_after'].to_list()
    temp = [math.log(i+1) for i in temp]
    df_all.loc[:, 'dead_after_log'] = temp

    import collections
    print([item for item, count in collections.Counter(df_all['id']).items() if count > 1])

    df_all.to_csv("./output/COVID_final.csv", index=False)


# main
if __name__ == '__main__':

    # 整合特征
    #get_feature_final()

    df = gp.GeoDataFrame.from_file("./shp/china_city_distinct_COVID19.shp")
    
    kf = KFold(3, True)
    index = []
    for train_index, test_index in kf.split(df):
        index.append((train_index, test_index))
    
    # epidemic id 疫情灾区id，暂定武汉
    epidemicIds = [420100]

    # 全时间段建模
    #df = df[~df['id'].isin(epidemicIds)]
    #case, df_predict = covid_all_predict(df, index)
    #df = pd.merge(df, df_predict, how='inner', on='id')
    #df = df[df['id'].isin(case)].sort_values(by='confirmed', ascending=False)

    # 管控前建模
    df_before = gp.GeoDataFrame.from_file("./shp/china_city_distinct_COVID19_before.shp")

    #covid_all_predict(df_before, index)

    # 管控后建模
    df_after = gp.GeoDataFrame.from_file("./shp/china_city_distinct_COVID19_after.shp")
    covid_all_predict(df_after, index)

