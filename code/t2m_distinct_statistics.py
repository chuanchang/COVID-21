# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
区县级每日0：00~23：00的t2m数据

每日t2m数据求均值，得到每日的t2m值，之后计算2020-1-1~2020-3-31时间范围内的平均t2m、最大t2m和最小t2m
"""

# load package
import pandas as pd

# 区县级rh数据统计
def distinct_statistics(years, months, days, times, t2m, pac_class_id):
    cols = []

    for year in years:
        for month in months:
            for day in days:
                col = []
                for time in times:
                    col.append('t2m' + '_' + year + month + day + '_' + time)

                try:
                    t2m_temp = t2m[col]
                    cols.append(year + month + day)
                    # 按行求和
                    pac_class_id[year + month + day] = t2m_temp.apply(lambda x: x.mean(), axis=1)
                except:
                    pass

    t2m_temp = pac_class_id[cols]

    distinct_t2m = pac_class_id['id']
    distinct_t2m['t2m_mean'] = t2m_temp.apply(lambda x: x.mean(), axis=1)
    distinct_t2m['t2m_max'] = t2m_temp.apply(lambda x: x.max(), axis=1)
    distinct_t2m['t2m_min'] = t2m_temp.apply(lambda x: x.min(), axis=1)
    distinct_t2m.to_csv("../data/ECMWF/zonal_statistics/distinct_t2m.csv", index=False)


# main
if __name__ == '__main__':

    pac_class_id = pd.read_csv("../data/ECMWF/zonal_statistics/pac_class_id.csv", sep=',')

    t2m = pd.read_csv("../data/ECMWF/zonal_statistics/", sep=',')

    # year month day times
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
    times = [
        '0000', '0100', '0200',
        '0300', '0400', '0500',
        '0600', '0700', '0800',
        '0900', '1000', '1100',
        '1200', '1300', '1400',
        '1500', '1600', '1700',
        '1800', '1900', '2000',
        '2100', '2200', '2300',
    ]

    distinct_statistics(years, months, days, times, t2m, pac_class_id)