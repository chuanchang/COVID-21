[TOC]

# COVID-19

## COVID-19中国各行政级数据获取

```shell
# 今日头条APP的疫情地图获取疫情数据：省级，地级市，区县级，输出 /data/COVID19_province.csv，/data/COVID19_city.csv，/data/COVID19_distinct.csv

cd code

python COVID19_from_TouTiao.py
```

### 数据说明

```shell
中国2015年省级、地级市、区县级行政编码
/data/china_location_id.csv
/data/china_location_id_2015.csv

省级疫情数据
/data/COVID19_province.csv   

地级市疫情数据
/data/COVID19_city.csv

区县级疫情数据
/data/COVID19_distinct.csv
```


### 2015中国区县级shp文件COVID-19属性加入

```shell
# 将上面COVID-19中国各行政级数据获取数据加进2015年中国区县级shp文件的属性表里

cd code

python china_shp_COVID19.py
```

#### 数据说明

```shell
中国2015年区县级shp文件
/shp/china_distinct.shp

中国2015年地级市shp文件
/shp/china_city.shp  

中国2015年省级shp文件
/shp/china_province.shp  
  


中国2015年区县级shp文件（含有COVID19累计确诊人数属性）
/shp/china_distinct_COVID19.shp

中国2015年地级市shp文件（含有COVID19累计确诊人数属性）
/shp/china_city_COVID19.shp

中国2015年省级shp文件（含有COVID19累计确诊人数属性）
/shp/china_province_COVID19.shp



中国2015年shp文件（含有COVID19累计确诊人数属性）mxd文件——软件是ArcMap10.2
/shp/COVID19_2015_COVID19.mxd

中国2015年区县级COVID19空间自相关分析——软件是GeoDa
```

## ECMWF ERA5数据获取

```shell
cd code

# 2m temperature
python t2m_from_ECMWF_ERA5.py

# 1000hPa relative humidity
python rh_from_ECMWF_ERA5.py
```

### 数据说明

```shell
中国 2m temperature
/data/ECMWF/t2m/

t2m_20200101_0000.nc   2020年1月1日 00:00  netCDF  2m temperature


中国 1000hPa relative humidity
/data/ECMWF/rh/

rh_20200101_0000.nc   2020年1月1日 00:00  netCDF  1000hPa relative humidity
```


## 百度迁徙数据获取

```shell
cd code

# 城市迁入迁徙规模指数、迁出迁徙规模指数和城内出行强度
python migration_index_from_Baidu.py

# 城市迁入迁徙规模指数、迁出迁徙规模指数和城内出行强度
python migration_index_from_Baidu_from_WuHan.py
```

### 数据说明

```shell

# 城市迁入迁徙规模指数、迁出迁徙规模指数和城内出行强度
/data/baidu_migration/city_migration.csv

/data/baidu_migration/distinct_migration.csv

# 城市迁入迁徙规模指数、迁出迁徙规模指数和城内出行强度
/data/baidu_migration/city_migration.csv

/data/baidu_migration/distinct_migration.csv
```