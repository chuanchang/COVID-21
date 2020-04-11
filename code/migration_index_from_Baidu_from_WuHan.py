# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
百度迁徙数据平台：http://qianxi.baidu.com/?from=baiduse

爬取武汉迁入各个城市的比例和迁徙指数
"""

# load package
import pandas as pd
import json
import requests
import numpy as np

# city 迁出、迁入迁徙规模指数
def move_migration_index(id):
    url = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id=' + str(id) + '&type=move_out'
    moveOut = requests.get(url).content.decode('utf-8')[3:-1]
    moveOut = json.loads(moveOut)['data']['list']

    url = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id=' + str(id) + '&type=move_in'
    moveIn = requests.get(url).content.decode('utf-8')[3:-1]
    moveIn = json.loads(moveIn)['data']['list']

    return moveOut, moveIn


# city 迁出比例
def epidemic_migration(china_city, china_distinct, epidemicIds, years, months, days):

    china_city_name = china_city['name'].to_list()
    china_distinct_name = china_distinct['name'].to_list()
    distinct_name = set()

    for id in epidemicIds:
        moveOut, moveIn = move_migration_index(id)

        for year in years:
            for month in months:
                for day in days:

                    date = year + month + day

                    china_city[date + '_moveOut'] = 0
                    china_city[date + '_moveIn'] = 0

                    china_distinct[date + '_moveOut'] = 0
                    china_distinct[date + '_moveIn'] = 0

                    url = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=' + str(id) + '&type=move_out' + '&date=' + date
                    try:
                        city_data = requests.get(url).content.decode('utf-8')[3:-1]
                        city_data = json.loads(city_data)['data']['list']
                        for i in range(len(city_data)):
                            name = city_data[i]['city_name']
                            value = city_data[i]['value']

                            if name in china_city_name:
                                china_city.loc[china_city['name'] == name, date + '_moveOut'] = moveOut[date] * value
                                china_city.loc[china_city['name'] == name, date + '_moveIn'] = moveIn[date] * value

                            elif name in china_distinct_name:
                                distinct_name.add(name)
                                china_distinct.loc[china_distinct['name'] == name, date + '_moveOut'] = moveOut[date] * value
                                china_distinct.loc[china_distinct['name'] == name, date + '_moveIn'] = moveIn[date] * value
                            else:
                                print(name)

                    except:
                        print(url)

    china_distinct = china_distinct[china_distinct['name'].isin(list(distinct_name))]

    return china_city, china_distinct


# main
if __name__ == '__main__':

    # China location id
    china_location = pd.read_csv("../data/china_location_id_2015.csv", sep=',')

    # china city
    china_city = china_location.loc[china_location['city'] == 1, ['id', 'location', 'province_id']]
    china_city.columns = ['id', 'name', 'province_id']
    print("china city num: " + str(len(china_city)))

    # china distinct
    china_distinct = china_location.loc[china_location['distinct'] == 1, ['id', 'location', 'province_id']]
    china_distinct.columns = ['id', 'name', 'province_id']

    print("china distinct num: " + str(len(china_distinct)))

    # epidemic id 疫情灾区id，暂定武汉
    epidemicIds = [420100]

    # year month day
    years = ['2020']
    months = ['01', '02', '03']
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

    # migration
    china_city, china_distinct = epidemic_migration(china_city, china_distinct, epidemicIds, years, months, days)
    epidemic_distinct = pd.concat([china_city, china_distinct])
    # city migration
    epidemic_distinct.to_csv("../data/baidu_migration/city_migration_from_WuHan.csv", index=False)
