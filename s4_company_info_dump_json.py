#!/usr/bin/env python
# coding: utf-8
# 將公司資訊存成本地端json檔案

import json
import time
import os
from MyConnect import MyConnect
from Crawler import Crawler
import threading
import pymysql


# 從SQL讀取職缺連結
def CompanyInfoThread(category):
    # 建立SQL連線
    conn_cfg = {
        'host': '',
        'user': '',
        'password': '',
        'db': ''
    }
    conn = pymysql.connect(**conn_cfg)
    cursor = conn.cursor()
    # 原sql指令為Like '_____' %，在python最後要打兩個%，只打一個無法運作
    sql = "select distinct `公司連結` from db_104.job_link where `職類編號` LIKE '%s%%'" % category
    cursor.execute(sql)
    companylink = cursor.fetchall()
    companylink = [i[0] for i in companylink]  # 建立職缺連結list
    conn.close()

    # 依序讀取公司連結，將公司資訊存成json
    for l in companylink:
        try:
            url = "https://" + l
            content = Crawler.company_info(url)
            dn = "[directory]"
            fn = url.split("company/")[1].split("?")[0]
            if not os.path.exists(dn):
                os.makedirs(dn)
            f = open(dn + fn + ".json", "w", encoding="utf-8")
            json.dump(content, f)
            f.close()
            print(url)
            print("職務類型", category , "的公司:" , fn, "complete")

        except:
            pass

# 開始分工合作
if __name__ == "__main__":
    start = time.time()
    db = MyConnect()
    sql = "select distinct substring(職類編號, 1, 4) from db_104.job_category"  # 找出中類編號
    categorys = db.query(sql)
    db.close()

    threadList = list()
    for category in categorys:
        threadList.append(threading.Thread(target=CompanyInfoThread, args=(category)))

    for i in threadList:
        i.start()

    for i in threadList:
        i.join()

    # 計時
    end = time.time()
    print("處理完畢，耗時：", (end - start) // 3600, "小時", (end - start) % 3600 // 60, "分", end - start % 3600 % 60, "秒")

