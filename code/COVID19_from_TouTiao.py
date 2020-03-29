# -*- coding: utf-8 -*-
# @Author  : Qi Shao
'''
从今日头条APP的疫情地图获取疫情数据：省级，地级市，区县级
'''


# load package
import pandas as pd
import urllib.request
import json


# data url
url = "https://i.snssdk.com/forum/ncov_data/?activeWidget=1&data_type=%5B2%2C4%5D"
with urllib.request.urlopen(url) as f:
    data = json.loads(f.read().decode('utf-8'))
    data = json.loads(data['ncov_nation_data'])
    data = data['provinces']


# 省级数据
def save_province(data):
    province = []

    for i in range(len(data)):
        temp = data[i]
        province_id = temp['id']
        province_name = temp['name']

        # 累计确诊人数
        province_confirmedNum = temp['confirmedNum']

        # 累计死亡人数
        province_deathsNum = temp['deathsNum']

        # 累计治愈人数
        province_curesNum = temp['curesNum']

        province.append([province_id, province_name, province_confirmedNum, province_deathsNum, province_curesNum])

    province = pd.DataFrame(province)
    province.columns = ['province_id', 'province_name', 'province_confirmedNum', 'province_deathsNum', 'province_curesNum']
    province.to_csv("../data/COVID19_province.csv", index=False)


# 地级市数据
def save_city(data):
    city = []

    for i in range(len(data)):
        temp = data[i]
        province_id = temp['id']
        province_name = temp['name']

        temp = temp['cities']

        for j in range(len(temp)):
            city_id = temp[j]['id']
            city_name = temp[j]['name']

            # 累计确诊人数
            city_confirmedNum = temp[j]['confirmedNum']

            # 累计死亡人数
            city_deathsNum = temp[j]['deathsNum']

            # 累计治愈人数
            city_curesNum = temp[j]['curesNum']

            city.append([city_id, city_name, city_confirmedNum, city_deathsNum, city_curesNum, province_name, province_id])

    city = pd.DataFrame(city)
    city.columns = ['city_id', 'city_name', 'city_confirmedNum', 'city_deathsNum', 'city_curesNum', 'province_name', 'province_id']
    city.to_csv("../data/COVID19_city.csv", index=False)


# 区县级数据
def save_distinct(data):
    distinct = []

    for i in range(len(data)):
        temp = data[i]
        province_id = temp['id']
        province_name = temp['name']

        temp = temp['cities']

        for j in range(len(temp)):
            city_id = temp[j]['id']
            city_name = temp[j]['name']

            if city_id.isdigit() and len(city_id) < 6:

                # data url
                distinct_url = "https://i.snssdk.com/toutiao/normandy/pneumonia_trending/district_stat/?local_id=" + city_id.ljust(6,'0')
                with urllib.request.urlopen(distinct_url) as f:
                    distinct_data = json.loads(f.read().decode('utf-8'))
                    distinct_data = distinct_data['data']['list']

                    for k in range(len(distinct_data)):
                        distinct_id = distinct_data[k]['local_id']
                        distinct_name = distinct_data[k]['name']

                        # 累计确诊人数
                        distinct_confirmedNum = distinct_data[k]['confirmed_count']

                        # 累计死亡人数
                        distinct_deathsNum = distinct_data[k]['death_count']

                        # 累计治愈人数
                        distinct_curesNum = distinct_data[k]['cured_count']

                        distinct.append([distinct_id, distinct_name, distinct_confirmedNum, distinct_deathsNum,
                                         distinct_curesNum, city_name, city_id, province_name, province_id])

    distinct = pd.DataFrame(distinct)
    distinct.columns = ['distinct_id', 'distinct_name', 'distinct_confirmedNum', 'distinct_deathsNum', 'distinct_curesNum',
                        'city_name', 'city_id', 'province_name', 'province_id']
    distinct.to_csv("../data/COVID19_distinct.csv", index=False)



# province data
print("start save province data")
save_province(data)
print("end!")


# city data
print("start save city data")
save_city(data)
print("end!")


# dictinct data
print("start save distinc data")
save_distinct(data)
print("end!")
