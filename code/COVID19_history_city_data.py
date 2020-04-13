# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
AkShare平台 https://akshare.readthedocs.io/zh_CN/latest/data/event/event.html

世界历史疫情数据，提取中国地级市的历史疫情数据，2019-12-1~2020-4-13
"""

# load package
import akshare as ak
import time
import pandas as pd


# China location id
china_location = pd.read_csv("../data/china_location_id_2015.csv", sep=',')
china_location = china_location[['id', 'location', 'province', 'city', 'distinct',
                                 'province_id', 'city_id']]

china_city = china_location[china_location['city']==1]
china_city = china_city[['id', 'location']]
print("china city number: " + str(len(china_city)))


china_distinct = china_location[(china_location['distinct']==1) and (china_location['city_id']==-999)]
china_distinct = china_distinct[['id', 'location']]
print("china distinct number: " + str(len(china_distinct)))


china_city_distinct = pd.concat([china_city, china_location])
print("china city and distinct number: " + str(len(china_city) + len(china_distinct)))


# get data
covid_19_history_df = ak.covid_19_history()
covid_19_history_df = covid_19_history_df[covid_19_history_df['country'] == '中国']
covid_19_history_df = covid_19_history_df[['date', 'province', 'provinceCode', 'city', 'cityCode',
                                           'confirmed', 'cured', 'dead']]

# 去除nan
covid_19_history_df = covid_19_history_df.dropna()


# 获取累计到2020-1-26的疫情数据
date = '2020-1-26'
covid_19_history_20200126 = covid_19_history_df[covid_19_history_df['date' == date]]
print(len(covid_19_history_20200126))

id = set(china_city_distinct['id'].to_list())
print(len(id))

id2 = set(covid_19_history_20200126['cityCode'].to_list())
print(len(id2))

print(id2.difference(id))


china_city_distinct = pd.merge(china_city_distinct, covid_19_history_20200126, how='left', on='id')


# 获取累计到今天的疫情数据
covid_19_history_today = covid_19_history_df[covid_19_history_df['date' == time.strftime("%Y-%m-%d")]]



china_city_distinct = pd.merge(china_city_distinct, covid_19_history_today, how='left', on='id')

china_city_distinct[''] = china_city_distinct[''] - china_city_distinct['']

china_city_distinct.to_csv("../output/try.csv", index=False)