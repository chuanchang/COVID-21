# COVID-19

## COVID-19中国各行政级数据获取

```shell
# 今日头条APP的疫情地图获取疫情数据：省级，地级市，区县级，输出 /data/COVID19_province.csv，/data/COVID19_city.csv，/data/COVID19_distinct.csv

cd code

python COVID19_from_TouTiao.py
```

#### 数据说明

```shell
中国2015年省级、地级市、区县级行政编码
/data/china_location_id_2015.csv

省级疫情数据
/data/COVID19_province.csv   

地级市疫情数据
/data/COVID19_city.csv

区县级疫情数据
/data/COVID19_distinct.csv
```


## 2015中国区县级shp文件COVID-19属性加入

```shell
# 将上面COVID-19中国各行政级数据获取数据加进2015年中国区县级shp文件的属性表里

cd code

python china_distinct_shp_COVID19.py
```

#### 数据说明

```shell
中国2015年区县级shp文件
/shp/china_all_dissolve.shp  

中国2015年区县级shp文件（含有COVID19累计确诊人数属性）
/shp/china_all_dissolve_COVID19.shp
```