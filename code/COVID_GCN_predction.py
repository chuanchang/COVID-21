# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
生成GCN的feature矩阵，经过归一化处理
"""

# load packages
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.utils import shuffle


# gcn feature normalize
def feature_normalize(city_feature):
    id = city_feature[['id']]
    Y = city_feature[['confirmed']]
    X = city_feature.drop(['id', 'confirmed'], axis=1)

    X = X.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))

    city_feature = pd.concat([id, X], axis=1)

    city_feature = pd.concat([city_feature, Y], axis=1)

    city_feature = shuffle(city_feature)
    
    city_feature.to_csv("./code/pygcn-master/data/covid/covid.content", index=False, header=None, sep='\t')


# main
if __name__ == '__main__':

    # China location id
    china_location = pd.read_csv("./data/china_location_id_2015.csv")
    china_location = china_location[['id', 'location', 'city', 'distinct', 'city_id']]

    china_city = china_location[china_location['city'] == 1]
    china_city = china_city[['id', 'location']]
    print("china city number: " + str(len(china_city)))

    china_distinct = china_location[(china_location['distinct'] == 1) & (china_location['city_id'] == -999)]
    china_distinct = china_distinct[['id', 'location']]
    print("china distinct number: " + str(len(china_distinct)))

    china_city_distinct = pd.concat([china_city, china_distinct])
    print("china city and distinct number: " + str(len(china_city_distinct)))


    # year month day
    years = ['2020']
    months = ['02']
    days = ['01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31']
    days = ['02']

    for year in years:
        for month in months:
            for day in days:
                date = year + month + day
                
                # rh
                rh = pd.read_csv("./data/ECMWF/zonal_statistics/city_rh_day.csv")
                rh = rh[['id', date]]
                rh.columns = ['id', 'rh']

                # t2m
                t2m = pd.read_csv("./data/ECMWF/zonal_statistics/city_t2m_day.csv")
                t2m = t2m[['id', date]]
                t2m.columns = ['id', 't2m']

                city_feature = pd.merge(rh, t2m, how='inner', on='id')

                # moveIn
                moveIn = pd.read_csv("./data/baidu_migration/city_moveIn.csv")
                moveIn = moveIn[['id', date + '_moveIn']]

                city_feature = pd.merge(city_feature, moveIn, how='left', on='id')

                # moveOut
                moveOut = pd.read_csv("./data/baidu_migration/city_moveOut.csv")
                moveOut = moveOut[['id', date + '_moveOut']]

                city_feature = pd.merge(city_feature, moveOut, how='left', on='id')

                # travel
                travel = pd.read_csv("./data/baidu_migration/city_travel.csv")
                travel = travel[['id', date + '_travel']]

                city_feature = pd.merge(city_feature, travel, how='left', on='id')

                # 武汉迁入人口比例
                epidemic_moveIn = pd.read_csv("./data/baidu_migration/city_move_in_from_WuHan.csv")
                epidemic_moveIn = epidemic_moveIn[['id', '420100_' + date + '_moveIn']]

                city_feature = pd.merge(city_feature, epidemic_moveIn, how='left', on='id')

                # 1.26 COVID疫情
                covid_19_history_all = pd.read_csv("./output/COVID_history_city.csv")

                # 获取累计到2020-1-28的疫情数据
                covid_19_20200128 = covid_19_history_all[covid_19_history_all['date'] == '2020-02-08']
                covid_19_20200128 = covid_19_20200128[['cityCode', 'confirmed', 'cured', 'dead']]
                covid_19_20200128.columns = ['id', 'confirmed0128', 'cured0128', 'dead0128']

                covid_19_20200127 = covid_19_history_all[covid_19_history_all['date'] == '2020-02-07']
                covid_19_20200127 = covid_19_20200127[['cityCode', 'confirmed', 'cured', 'dead']]
                covid_19_20200127.columns = ['id', 'confirmed0127', 'cured0127', 'dead0127']

                city_feature = pd.merge(city_feature, covid_19_20200128, how='left', on='id')
                city_feature = city_feature.fillna(0)

                city_feature = pd.merge(city_feature, covid_19_20200127, how='left', on='id')
                city_feature = city_feature.fillna(0)

                city_feature['confirmed'] = city_feature['confirmed0128'] - city_feature['confirmed0127']
                #city_feature['cured'] = city_feature['cured0128'] - city_feature['cured0127']
                #city_feature['dead'] = city_feature['dead0128'] - city_feature['dead0127']

                temp = city_feature['confirmed'].to_list()
                temp = [np.log(i+1) for i in temp]
                city_feature.loc[:, 'confirmed'] = temp

                city_feature = city_feature.drop(['confirmed0127', 'cured0127', 'dead0127', 'confirmed0128', 'cured0128', 'dead0128'], axis=1)

                city_feature = city_feature[~city_feature['id'].isin(['710000', '810000', '820000', '659006', '659007', '659008', '460300'])]
                feature_normalize(city_feature)
