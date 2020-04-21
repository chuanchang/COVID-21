# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
百度迁徙数据平台：http://qianxi.baidu.com/?from=baiduse

爬取各个城市的迁入迁徙规模指数、迁出迁徙规模指数及城内出行强度
"""

# load package
import pandas as pd
import json
import requests
import time
import numpy as np
import os


# city 迁入迁徙规模指数
def moveIn_migration_index(city_baidu_ids, years, months, days, control_date):

    china_city_moveIn = pd.DataFrame(city_baidu_ids)
    china_city_moveIn.columns = ['id']

    for id in city_baidu_ids:

        url = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=' + str(id) + '&type=move_in'
        try:
            city_data = requests.get(url).content.decode('utf-8')[3:-1]
            city_data = json.loads(city_data)['data']['list']

            for year in years:
                for month in months[year]:
                    for day in days:
                        if year + month + day in city_data.keys():
                            china_city_moveIn.loc[china_city_moveIn['id'] == id, year + month + day + '_moveIn'] = city_data[year + month + day]
                        else:
                            print(year + month + day)
        except:
            print(url)

    china_city_moveIn.to_csv(os.path.join(path, "data/baidu_migration/city_moveIn.csv"), index=False)

    return china_city_moveIn


# city 迁出迁徙规模指数
def moveOut_migration_index(city_baidu_ids, years, months, days, control_date):

    china_city_moveOut = pd.DataFrame(city_baidu_ids)
    china_city_moveOut.columns = ['id']

    for id in city_baidu_ids:

        url = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=' + str(id) + '&type=move_out'
        try:
            city_data = requests.get(url).content.decode('utf-8')[3:-1]
            city_data = json.loads(city_data)['data']['list']

            for year in years:
                for month in months[year]:
                    for day in days:
                        if year + month + day in city_data.keys():
                            china_city_moveOut.loc[china_city_moveOut['id'] == id, year + month + day + '_moveOut'] = city_data[year + month + day]
                        else:
                            print(year + month + day)
        except:
            print(url)

    china_city_moveOut.to_csv(os.path.join(path, "data/baidu_migration/city_moveOut.csv"), index=False)

    return china_city_moveOut


# city 城市出行强度
def travel_intensity(city_baidu_ids, years, months, days, control_date):

    china_city_travel = pd.DataFrame(city_baidu_ids)
    china_city_travel.columns = ['id']

    for id in city_baidu_ids:
        url = 'http://huiyan.baidu.com/migration/internalflowhistory.jsonp?dt=city&id=' + str(id) + '&date=' + time.strftime("%Y%m%d")

        try:
            city_data = requests.get(url).content.decode('utf-8')[3:-1]
            city_data = json.loads(city_data)['data']['list']

            for year in years:
                for month in months[year]:
                    for day in days:
                        if year + month + day in city_data.keys():
                            china_city_travel.loc[china_city_travel['id'] == id, year + month + day + '_travel'] = city_data[year + month + day]
                        else:
                            print(year + month + day)
        except:
            print(url)

    china_city_travel.to_csv(os.path.join(path, "data/baidu_migration/city_travel.csv"), index=False)

    return china_city_travel

# main
if __name__ == '__main__':

    #获取当前目录的绝对路径
    path = os.path.realpath(os.curdir)

    # China location id
    china_location = pd.read_csv(os.path.join(path, "data/china_location_id_2015.csv"))
    city_baidu_ids = list(set(china_location['city_baidu_id'].to_list()))
    print(len(city_baidu_ids))

    # year month day
    years = ['2020']
    months = {'2020': ['01', '02', '03']}
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

    control_date = '20200126'

    # city moveIn moveOut travel
    moveIn = moveIn_migration_index(city_baidu_ids, years, months, days, control_date)
    print("china city moveIn: " + str(len(moveIn)))

    moveOut = moveOut_migration_index(city_baidu_ids, years, months, days, control_date)
    print("china city moveOut: " + str(len(moveOut)))

    travel = travel_intensity(city_baidu_ids, years, months, days, control_date)
    print("china city travel: " + str(len(travel)))


    id1 = moveIn['id'].to_list()
    id2 = moveOut['id'].to_list()
    id3 = travel['id'].to_list()

    print(list(set(city_baidu_ids).difference(set(id1))))
    print(list(set(city_baidu_ids).difference(set(id2))))
    print(list(set(city_baidu_ids).difference(set(id3))))
    
    # city migration moveIn
    city_moveIn = moveIn[['id']].copy()

    # 只保留特征值
    moveIn = moveIn.dropna(axis=1).iloc[:, 1::]

    # 管控日期之前
    moveIn_before = moveIn.loc[:, moveIn.columns.values <= control_date + '_moveIn']

    # 管控日期之后
    moveIn_after = moveIn.loc[:, moveIn.columns.values > control_date + '_moveIn']

    # 整个时间段
    city_moveIn.loc[:, 'moveIn_index_mean'] = moveIn.apply(lambda x: x.mean(), axis=1).to_list()
    city_moveIn.loc[:, 'moveIn_index_max'] = moveIn.apply(lambda x: x.max(), axis=1).to_list()
    city_moveIn.loc[:, 'moveIn_index_min'] = moveIn.apply(lambda x: x.min(), axis=1).to_list()

    # 管控日期之前
    city_moveIn.loc[:, 'moveIn_index_mean_before'] = moveIn_before.apply(lambda x: x.mean(), axis=1).to_list()
    city_moveIn.loc[:, 'moveIn_index_max_before'] = moveIn_before.apply(lambda x: x.max(), axis=1).to_list()
    city_moveIn.loc[:, 'moveIn_index_min_before'] = moveIn_before.apply(lambda x: x.min(), axis=1).to_list()

    # 管控日期之后
    city_moveIn.loc[:, 'moveIn_index_mean_after'] = moveIn_after.apply(lambda x: x.mean(), axis=1).to_list()
    city_moveIn.loc[:, 'moveIn_index_max_after'] = moveIn_after.apply(lambda x: x.max(), axis=1).to_list()
    city_moveIn.loc[:, 'moveIn_index_min_after'] = moveIn_after.apply(lambda x: x.min(), axis=1).to_list()



    # city migration moveOut
    city_moveOut = moveOut[['id']].copy()

    # 只保留特征值
    moveOut = moveOut.dropna(axis=1).iloc[:, 1::]

    # 管控日期之前
    moveOut_before = moveOut.loc[:, moveOut.columns.values <= control_date + '_moveOut']

    # 管控日期之后
    moveOut_after = moveOut.loc[:, moveOut.columns.values > control_date + '_moveOut']

    # 整个时间段
    city_moveOut.loc[:, 'moveOut_index_mean'] = moveOut.apply(lambda x: x.mean(), axis=1).to_list()
    city_moveOut.loc[:, 'moveOut_index_max'] = moveOut.apply(lambda x: x.max(), axis=1).to_list()
    city_moveOut.loc[:, 'moveOut_index_min'] = moveOut.apply(lambda x: x.min(), axis=1).to_list()

    # 管控日期之前
    city_moveOut.loc[:, 'moveOut_index_mean_before'] = moveOut_before.apply(lambda x: x.mean(), axis=1).to_list()
    city_moveOut.loc[:, 'moveOut_index_max_before'] = moveOut_before.apply(lambda x: x.max(), axis=1).to_list()
    city_moveOut.loc[:, 'moveOut_index_min_before'] = moveOut_before.apply(lambda x: x.min(), axis=1).to_list()

    # 管控日期之后
    city_moveOut.loc[:, 'moveOut_index_mean_after'] = moveOut_after.apply(lambda x: x.mean(), axis=1).to_list()
    city_moveOut.loc[:, 'moveOut_index_max_after'] = moveOut_after.apply(lambda x: x.max(), axis=1).to_list()
    city_moveOut.loc[:, 'moveOut_index_min_after'] = moveOut_after.apply(lambda x: x.min(), axis=1).to_list()
    
    # city migration travel
    city_travel = travel[['id']].copy()

    # 只保留特征值
    travel = travel.dropna(axis=1).iloc[:, 1::]

    # 管控日期之前
    travel_before = travel.loc[:, travel.columns.values <= control_date + '_travel']

    # 管控日期之后
    travel_after = travel.loc[:, travel.columns.values > control_date + '_travel']

    # 整个时间段
    city_travel.loc[:, 'travel_index_mean'] = travel.apply(lambda x: x.mean(), axis=1).to_list()
    city_travel.loc[:, 'travel_index_max'] = travel.apply(lambda x: x.max(), axis=1).to_list()
    city_travel.loc[:, 'travel_index_min'] = travel.apply(lambda x: x.min(), axis=1).to_list()

    # 管控日期之前
    city_travel.loc[:, 'travel_index_mean_before'] = travel_before.apply(lambda x: x.mean(), axis=1).to_list()
    city_travel.loc[:, 'travel_index_max_before'] = travel_before.apply(lambda x: x.max(), axis=1).to_list()
    city_travel.loc[:, 'travel_index_min_before'] = travel_before.apply(lambda x: x.min(), axis=1).to_list()

    # 管控日期之后
    city_travel.loc[:, 'travel_index_mean_after'] = travel_after.apply(lambda x: x.mean(), axis=1).to_list()
    city_travel.loc[:, 'travel_index_max_after'] = travel_after.apply(lambda x: x.max(), axis=1).to_list()
    city_travel.loc[:, 'travel_index_min_after'] = travel_after.apply(lambda x: x.min(), axis=1).to_list()

    china_city_migration = pd.merge(city_moveIn, city_moveOut, how='inner', on='id')
    china_city_migration = pd.merge(china_city_migration, city_travel, how='inner', on='id')

    china_city_migration.to_csv(os.path.join(path, "data/baidu_migration/city_migration.csv"), index=False)