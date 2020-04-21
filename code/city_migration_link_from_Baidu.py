# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
百度迁徙数据平台：http://qianxi.baidu.com/?from=baiduse

爬取中国每天的城市迁徙link，输出到文件里，文件格式如下：

512000 520200

表示城市520200迁徙到512000，link关系为：520200->512000
"""

# load package
import pandas as pd
import json
import requests
import numpy as np
import time


# city 迁出比例
def city_migration_link(china_city_distinct, years, months, days):

    city_baidu_ids = china_city_distinct['city_baidu_id'].to_list()
    city_link = []
    city_name = china_city_distinct['name'].to_list()

    for year in years:
        for month in months[year]:
            for day in days:
                date = year + month + day

                for id in city_baidu_ids:

                    url = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=' + str(id) + '&type=move_out' + '&date=' + date
                    try:
                        city_data = requests.get(url).content.decode('utf-8')[3:-1]
                        city_data = json.loads(city_data)['data']['list']

                        for i in range(len(city_data)):
                            name = city_data[i]['city_name']
                            if name not in city_name:
                                print(name)
                            city_link.append([china_city_distinct.loc[china_city_distinct['name']==name, ['id']].values[0][0],
                                              china_city_distinct.loc[china_city_distinct['city_baidu_id']==id, ['id']].values[0][0]])
                    except:
                        print(url)

                city_link = pd.DataFrame(city_link)
                city_link.to_csv("../output/city_migration_link_" + date + ".csv", index=False, sep=' ', header=None)

# main
if __name__ == '__main__':

    # China location id
    china_location = pd.read_csv("../data/china_location_id_2015.csv", sep=',')

    # china city
    china_city = china_location.loc[china_location['city'] == 1, ['id', 'city_baidu_id', 'location']]
    china_city.columns = ['id', 'city_baidu_id', 'name']
    print("china city num: " + str(len(china_city)))

    # china distinct
    china_distinct = china_location.loc[(china_location['distinct'] == 1) & (china_location['city_id'] == -999), ['id', 'city_baidu_id', 'location']]
    china_distinct.columns = ['id', 'city_baidu_id', 'name']
    print("china distinct num: " + str(len(china_distinct)))

    china_city_distinct = pd.concat([china_city, china_distinct])
    china_city_distinct = china_city_distinct[china_city_distinct['city_baidu_id']!=-999]

    # year month day
    years = ['2020']
    months = {'2020': ['01']}
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
    days = ['22']

    # migration link
    city_migration_link(china_city_distinct, years, months, days)

