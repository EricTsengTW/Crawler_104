#!/usr/bin/env python
# coding: utf-8
# 將職務類型的資訊，存入MySQL
from MyConnect import MyConnect
from sqlalchemy import create_engine
from sqlalchemy import INT
from Crawler import Crawler


db = MyConnect()
# 輸入你MySQL的id、password、db名稱
engine = create_engine('mysql+pymysql://[MySQLid]:[MySQLpassword]@localhost:3306/[MySQLdb]')
df = Crawler.job_category("https://www.104.com.tw/jb/category/?cat=1&jobsource=indexpoc2018")
df.to_sql('job_category', engine, index=False, if_exists="replace", dtype={"職缺數量": INT})
db.close()
# table名稱、engine連結引擎、index是否有索引編號、if_exists ="fail"(回傳ValueError), "replace"(覆蓋檔案), "append"(添加檔案在後端)、dtype = {"欄位名稱", INT(CHAR)} 定義職缺數量欄位資料屬性為INT
