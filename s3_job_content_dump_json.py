#!/usr/bin/env python
# coding: utf-8
# 將工作內容存成本地端json檔案

import json
import time
import os
from MyConnect import MyConnect
from Crawler import Crawler
import threading
import pymysql


# 從SQL讀取職缺連結
def JobContentThread(category):
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
    sql = "select `職缺連結` from db_104.job_link where `職類編號` LIKE '%s%%'" % category
    cursor.execute(sql)
    joblink = cursor.fetchall()
    joblink = [i[0] for i in joblink]  # 建立職缺連結list
    conn.close()

    # 依序讀取職缺連結，將職缺資訊存成json
    for l in joblink:
        try:
            url = "https://" + l
            content = Crawler.job_content(url)
            dn = "[directory]"
            fn = url.split("job/")[1].split("?")[0]
            if not os.path.exists(dn):
                os.makedirs(dn)
            f = open(dn + fn + ".json", "w", encoding="utf-8")
            json.dump(content, f)
            f.close()
            print(url)
            print("職務類型", category , "的檔案:" , fn, "complete")

        except:
            pass

# 開始分工合作
if __name__ == "__main__":
    start = time.time()
    db = MyConnect()
    sql = "select distinct substring(職類編號, 1, 4) from db_104.job_category"  # 找出中類編號
    categorys = db.query(sql)  # 得到tuple list
    db.close()

    threadList = list()
    for category in categorys:
        threadList.append(threading.Thread(target=JobContentThread, args=(category)))  # args要丟tuple

    for i in threadList:
        i.start()

    for i in threadList:
        i.join()

    # 計時
    end = time.time()
    print("處理完畢，耗時：", (end - start) // 3600, "小時", (end - start) % 3600 // 60, "分", end - start % 3600 % 60, "秒")

