# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
生成GCN的feature矩阵，经过归一化处理
"""

# load packages
import pandas as pd
import os


# gcn feature normalize

def feature_normalize():
    pass


# main
if __name__ == '__main__':

    #获取当前目录的绝对路径
    path = os.path.realpath(os.curdir)

    # China location id
    china_location = pd.read_csv(os.path.join(path, "data/china_location_id_2015.csv"))
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
    days = ['03']

    for year in years:
        for month in months:
            for day in days:
                date = year + month + day
                
                # rh
                rh = pd.read_csv(os.path.join(path, "data/ECMWF/zonal_statistics/city_rh_day.csv"))
                rh = rh[['id', date]]

                # t2m
                t2m = pd.read_csv(os.path.join(path, "data/ECMWF/zonal_statistics/city_t2m_day.csv"))
                t2m = t2m[['id', date]]

                city_feature = pd.merge(rh, t2m, how='inner', on='id')

                # moveIn
                moveIn = pd.read_csv(os.path.join(path, "data/baidu_migration/city_moveIn.csv"))
                moveIn = moveIn[['id', date + '_moveIn']]

                city_feature = pd.merge(city_feature, moveIn, how='left', on='id')

                # moveOut
                moveOut = pd.read_csv(os.path.join(path, "data/baidu_migration/city_moveOut.csv"))
                moveOut = moveOut[['id', date + '_moveOut']]

                city_feature = pd.merge(city_feature, moveOut, how='left', on='id')

                # travel
                travel = pd.read_csv(os.path.join(path, "data/baidu_migration/city_travel.csv"))
                travel = travel[['id', date + '_travel']]

                city_feature = pd.merge(city_feature, travel, how='left', on='id')

                # 武汉迁入人口比例
                epidemic_moveIn = pd.read_csv(os.path.join(path, "data/baidu_migration/city_migration_in_from_WuHan.csv"))
                epidemic_moveIn = epidemic_moveIn[['city_baidu_id', '420100_' + date + '_moveIn']]

                city_feature = pd.merge(city_feature, epidemic_moveIn, how='left', on='id')


                # 1.26 COVID疫情
                covid_19_history_all = pd.read_csv(os.path.join(path, "output/COVID_history_city.csv"))

                # 获取累计到2020-1-26的疫情数据
                control_date = '2020-02-06'
                control_date_before = '2020-02-05'
                covid_19_history_before = covid_19_history_all[(covid_19_history_all['date'] == control_date) or (covid_19_history_all['date'] == control_date_before)]
                covid_19_history_before = covid_19_history_before[['cityCode', 'confirmed', 'cured', 'dead']]
                covid_19_history_before.columns = ['id', 'confirmed_before', 'cured_before', 'dead_before']
                print(covid_19_history_before)


                aaa


                feature_normalize()

