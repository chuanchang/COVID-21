# -*- coding: utf-8 -*-
# @Author  : Qi Shao


import akshare as ak
covid_19_history_df = ak.covid_19_history()
print(covid_19_history_df)

covid_19_history_df.to_csv("../output/try.csv", index=False)