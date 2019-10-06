#!/usr/bin/env python
# coding: utf-8
# 將產業類型的資訊，存入MySQL
from sqlalchemy import create_engine
from MyConnect import MyConnect
from Crawler import Crawler
import time


if __name__ == "__main__":
    start = time.time()
    db = MyConnect()
    engine = create_engine('mysql+pymysql://[MySQLid]:[MySQLpassword]@localhost:3306/db_104')
    df = Crawler.industry_category("https://www.104.com.tw/jb/category/?cat=3&jobsource=indexpoc2018")
    df.to_sql('industry_category', engine, index=False, if_exists="replace")
    # table名稱、engine連結引擎、index是否有索引編號、if_exists ="fail"(回傳ValueError), "replace"(覆蓋檔案), "append"(添加檔案在後端)、dtype = {"欄位名稱", INT(CHAR)} 定義職缺數量欄位資料屬性為INT
    db.close()
    end = time.time()
    print("處理完畢，耗時：", (end - start), "秒")
