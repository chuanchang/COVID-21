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

# city 迁入迁徙规模指数
def moveIn_migration_index(city_baidu_ids, years, months, days):

    moveIn = []

    for id in city_baidu_ids:
        url = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id=' + str(id) + '&type=move_in'
        try:
            city_data = requests.get(url).content.decode('utf-8')[3:-1]
            city_data = json.loads(city_data)['data']['list']

            moveIn_index = []
            for year in years:
                for month in months:
                    for day in days:
                        if year + month + day in city_data.keys():
                            moveIn_index.append(city_data[year + month + day])
                        else:
                            print(year + month + day)

            moveIn.append([id, sum(moveIn_index), max(moveIn_index), min(moveIn_index)])
        except:
            pass

    moveIn = pd.DataFrame(moveIn)
    moveIn.columns = ['city_baidu_id', 'moveIn_index_sum', 'moveIn_index_max', 'moveIn_index_min']

    return moveIn


# city 迁出迁徙规模指数
def moveOut_migration_index(city_baidu_ids, years, months, days):

    moveOut = []

    for id in city_baidu_ids:
        url = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id=' + str(id) + '&type=move_out'
        try:
            city_data = requests.get(url).content.decode('utf-8')[3:-1]
            city_data = json.loads(city_data)['data']['list']

            moveOut_index = []
            for year in years:
                for month in months:
                    for day in days:
                        if year + month + day in city_data.keys():
                            moveOut_index.append(city_data[year + month + day])
                        else:
                            print(year + month + day)

            moveOut.append([id, sum(moveOut_index), max(moveOut_index), min(moveOut_index)])
        except:
            pass

    moveOut = pd.DataFrame(moveOut)
    moveOut.columns = ['city_baidu_id', 'moveOut_index_sum', 'moveOut_index_max', 'moveOut_index_min']
    return moveOut


# city 城市出行强度
def travel_intensity(city_baidu_ids, years, months, days):

    travel = []

    for id in city_baidu_ids:
        url = 'http://huiyan.baidu.com/migration/internalflowhistory.jsonp?dt=city&id=' + str(id) + '&date=20200408'
        try:
            city_data = requests.get(url).content.decode('utf-8')[3:-1]
            city_data = json.loads(city_data)['data']['list']

            travel_index = []
            for year in years:
                for month in months:
                    for day in days:
                        if year + month + day in city_data.keys():
                            travel_index.append(city_data[year + month + day])
                        else:
                            print(year + month + day)

            travel.append([id, sum(travel_index), max(travel_index), min(travel_index)])
        except:
            pass

    travel = pd.DataFrame(travel)
    travel.columns = ['city_baidu_id', 'travel_index_sum', 'travel_index_max', 'travel_index_min']
    return travel

# main
if __name__ == '__main__':

    # China location id
    china_location = pd.read_csv("../data/china_location_id_2015.csv", sep=',')
    city_baidu_ids = list(set(china_location['city_baidu_id'].to_list()))
    print(len(city_baidu_ids))

    # year month day
    years = ['2020']
    months = ['01', '02', '03', '04']
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

    # city moveIn moveOut travel
    moveIn = moveIn_migration_index(city_baidu_ids, years, months, days)
    print("china city moveIn: " + str(len(moveIn)))

    moveOut = moveOut_migration_index(city_baidu_ids, years, months, days)
    print("china city moveOut: " + str(len(moveOut)))

    travel = travel_intensity(city_baidu_ids, years, months, days)
    print("china city travel: " + str(len(travel)))


    id1 = moveIn['city_baidu_id'].to_list()
    id2 = moveOut['city_baidu_id'].to_list()
    id3 = travel['city_baidu_id'].to_list()

    print(list(set(city_baidu_ids).difference(set(id1))))
    print(list(set(city_baidu_ids).difference(set(id2))))
    print(list(set(city_baidu_ids).difference(set(id3))))


    # city migration
    china_city = pd.merge(moveIn, moveOut, how='left', on='city_baidu_id')
    china_city = pd.merge(china_city, travel, how='left', on='city_baidu_id')
    china_city = china_city.fillna(value=0)
    china_city.to_csv("../data/baidu_migration/city_migration.csv", index=False)