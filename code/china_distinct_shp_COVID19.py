# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
将中国2015的区县级、地级市、省级的shp文件加入COVID-19疫情属性
"""

import geopandas
import pandas as pd

'''
""" 
对中国2015的区县级shp文件加上 cityId 和 provinceId
"""
# 2015 China distinct shp
path = '../shp/china_all_8_dissolve.shp'
shp_df = geopandas.GeoDataFrame.from_file(path)
shp_df.rename(columns={'PAC': 'id'}, inplace=True)


# 2015 China location id
location_df = pd.read_csv('../data/china_location_id_2015.csv', sep=',')
location_df = location_df[['id', 'location', 'city_id', 'province_id']]
location_df.columns = ['id', 'location', 'cityId', 'proId']

city = location_df[['id', 'location']]
city.columns = ['cityId', 'cityName']

province = location_df[['id', 'location']]
province.columns = ['proId', 'proName']

shp_df = pd.merge(shp_df, location_df, how='left', on='id')
shp_df = pd.merge(shp_df, city, how='left', on='cityId')
shp_df = pd.merge(shp_df, province, how='left', on='proId')

shp_df.to_file("../shp/china_distinct.shp", encoding='utf-8')
aaaaaa
'''



# 2015 China distinct shp
path = '../shp/china_distinct.shp'
shp_distinct = geopandas.GeoDataFrame.from_file(path)

# 2015 China city shp
path = '../shp/china_city.shp'
shp_city = geopandas.GeoDataFrame.from_file(path)
shp_city.rename(columns={'cityId': 'id', 'cityName': 'location'}, inplace=True)

# 2015 China province shp
path = '../shp/china_province.shp'
shp_province = geopandas.GeoDataFrame.from_file(path)
shp_province.rename(columns={'proId': 'id', 'proName': 'location'}, inplace=True)


# COVID19 distinct
china_distinct = pd.read_csv("../data/COVID19_distinct.csv", sep=',')
china_distinct = china_distinct[['distinct_id', 'distinct_name', 'distinct_confirmedNum']]
china_distinct.columns = ['id', 'name', 'confirmedNum']

# COVID19 city
china_city = pd.read_csv("../data/COVID19_city.csv", sep=',')
china_city = china_city[['city_id', 'city_name', 'city_confirmedNum']]
china_city.columns = ['id', 'name', 'confirmedNum']

# COVID19 province
china_province = pd.read_csv("../data/COVID19_province.csv", sep=',')
china_province = china_province[['province_id', 'province_name', 'province_confirmedNum']]
china_province.columns = ['id', 'name', 'confirmedNum']

# merge
china = pd.concat([china_city, china_distinct])
shp_distinct = pd.merge(shp_distinct, china, how='left', on='id')
shp_distinct = shp_distinct.fillna(value=0)
shp_distinct.to_file("../shp/china_distinct_COVID19.shp", encoding='utf-8')

# display level
print("distinct display level:")
num = shp_distinct['confirmedNum'].to_list()

level = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 90, 150, 250, 500, 1000, 3000, 6000, 9000]
for i in range(1, len(level)):
    res=0
    for j in num:
        if j<=level[i] and j>level[i-1]:
            res+=1
    print(level[i-1], level[i], res)

# merge
shp_city = pd.merge(shp_city, china_city, how='left', on='id')
shp_city = shp_city.fillna(value=0)
shp_city.to_file("../shp/china_city_COVID19.shp", encoding='utf-8')

# display level
print("city display level:")
num = shp_city['confirmedNum'].to_list()

level = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 150, 200, 500, 1000, 5000, 60000]
for i in range(1, len(level)):
    res = 0
    for j in num:
        if j <= level[i] and j > level[i - 1]:
            res += 1
    print(level[i - 1], level[i], res)

# merge
shp_province = pd.merge(shp_province, china_province, how='left', on='id')
shp_province = shp_province.fillna(value=0)
shp_province.to_file("../shp/china_province_COVID19.shp", encoding='utf-8')

# display level
print("province display level:")
num = shp_province['confirmedNum'].to_list()

level = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 700000]
for i in range(1, len(level)):
    res = 0
    for j in num:
        if j <= level[i] and j > level[i - 1]:
            res += 1
    print(level[i - 1], level[i], res)


