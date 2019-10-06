#!/usr/bin/env python
# coding: utf-8
# 將各職類擁有的職缺連結，存入MySQL

from MyConnect import MyConnect
from Crawler import Crawler
from sqlalchemy import create_engine
import time

if __name__ == "__main__":
    # 從SQL讀取職務類型編號，作為爬取職缺url的資訊
    db = MyConnect()
    # 輸入你MySQL的id、password、db名稱
    engine = create_engine('mysql+pymysql://[MySQLid]:[MySQLpassword]@localhost:3306/[MySQLdb]')
    sql = "select 職類編號 from job_category"
    jobcategory = db.query(sql)
    jobcategory = [i[0] for i in jobcategory]  # 職類編號list

    # 開始計時
    start = time.time()

    # 將職缺連結的資訊，存入DB
    for l in jobcategory:
        url = "https://www.104.com.tw/jobs/search/?ro=1&jobcat=" + l + "&order=11&asc=0&page=1&mode=s&jobsource=2018indexpoc"
        pages = Crawler.job_page(url)  # 計算本職類有幾頁

        for i in range(1, pages+1):
            try:
                url = "https://www.104.com.tw/jobs/search/?ro=1&jobcat=" + l + "&order=11&asc=0&page=" + str(i) + "&mode=s&jobsource=2018indexpoc"
                df = Crawler.job_link(url)
                df.to_sql('job_link_raw', engine, index=False, if_exists="append")
                print("職類:", l , "page:" , i, "complete")

            except:
                pass

    # 結束計時
    end = time.time()
    print("處理完畢，耗時：", (end - start) // 3600, "小時", (end - start) % 3600 // 60, "分", format(end - start % 3600 % 60, '.2f'), "秒")
    db.close()