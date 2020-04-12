# -*- coding: utf-8 -*-
# @Author  : Qi Shao

"""
区县级每日0：00~23：00的rh数据

每日rh数据求均值，得到每日的rh值，之后计算2020-1-1~2020-3-31时间范围内的平均rh、最大rh和最小rh
"""

# load package
import pandas as pd

# 区县级rh数据统计
def distinct_statistics(years, months, days, times, rh, pac_class_id):
    cols = []

    for year in years:
        for month in months:
            for day in days:
                col = []
                for time in times:
                    col.append('rh' + '_' + year + month + day + '_' + time)

                try:
                    rh_temp = rh[col]
                    cols.append(year + month + day)
                    # 按行求和
                    pac_class_id[year + month + day] = rh_temp.apply(lambda x: x.mean(), axis=1)
                except:
                    print(col)

    rh_temp = pac_class_id[cols]

    distinct_rh = pac_class_id['id']
    distinct_rh['rh_mean'] = rh_temp.apply(lambda x: x.mean(), axis=1)
    distinct_rh['rh_max'] = rh_temp.apply(lambda x: x.max(), axis=1)
    distinct_rh['rh_min'] = rh_temp.apply(lambda x: x.min(), axis=1)
    distinct_rh.to_csv("../data/ECMWF/zonal_statistics/distinct_rh.csv", index=False)


# main
if __name__ == '__main__':

    pac_class_id = pd.read_csv("../data/ECMWF/zonal_statistics/pac_class_id.csv", sep=',')

    rh = pd.read_csv("../data/ECMWF/zonal_statistics/", sep=',')

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

    distinct_statistics(years, months, days, times, rh, pac_class_id)