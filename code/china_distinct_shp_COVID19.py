# -*- coding: utf-8 -*-
# @Author  : Qi Shao

import geopandas
import pandas as pd

# 2015 China distinct shp
path = '../shp/china_all_dissolve.shp'
shp_df = geopandas.GeoDataFrame.from_file(path)
shp_df.rename(columns={'PAC': 'id'}, inplace=True)

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
china = pd.concat([china_province, china_city, china_distinct])
shp_df = pd.merge(shp_df, china, how='left', on='id')
shp_df = shp_df.fillna(value=0)
shp_df.to_file("../shp/china_all_dissolve_COVID19.shp", encoding='utf-8')

# display level
num = shp_df['confirmedNum'].to_list()

level = [5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 90, 150, 250, 500, 1000, 3000, 6000, 9000]
for i in range(1, len(level)):
    res=0
    for j in num:
        if j<=level[i] and j>level[i-1]:
            res+=1
    print(level[i-1], level[i], res)


