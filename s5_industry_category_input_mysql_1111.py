#!/usr/bin/env python
# coding: utf-8
# 爬蟲主要功能在此

from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
import pandas as pd
import time
from MyConnect import MyConnect

### 爬取產業分類和編號 ###
# url: https://www.1111.com.tw/job-bank/category.asp?cat=3
def industry_category(url):
    df = pd.DataFrame(columns=["產業中類", "中類編號", "產業小類", "小類編號", "連結網址"])

    # 找到內容網址
    head = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=head)
    res.encoding = "utf8"  # 避免python以ISO-8859-1輸出亂碼
    html = BeautifulSoup(res.text)

    # 爬取產業類型資訊
    category_all_list = html.find("div", class_="dutyList").find("ul").find_all("ul")
    for all in category_all_list:
        category_m_list = all.find_all("a")
        for cate_m in category_m_list:
            url2 = "https://www.1111.com.tw" + cate_m["href"]
            res2 = requests.get(url2, headers=head)
            res2.encoding = "utf8"
            html2 = BeautifulSoup(res2.text)
            category_list = html2.find("div", class_="dutyList").find_all("a")
            for cate in range(1, len(category_list)):
                category_m = cate_m.text
                category_m_no = cate_m["href"].split("3&t=")[1]
                category = category_list[cate].text
                category_no = category_list[cate]["href"].split("3&t=")[1].split("&")[0]
                category_link = "https://www.1111.com.tw" + category_list[cate]["href"]
                data = {"產業中類": category_m,
                        "中類編號": category_m_no,
                        "產業小類": category,
                        "小類編號": category_no,
                        "連結網址": category_link
                        }

                print("中類", category_m, "小類", category, "完成")

                # 放入表格中
                df = df.append(data, ignore_index=True)
    return df


if __name__ == "__main__":
    start = time.time()
    db = MyConnect()
    engine = create_engine('mysql+pymysql://[MySQLid]:[MySQLpassword]@localhost:3306/db_1111')
    df = industry_category("https://www.1111.com.tw/job-bank/category.asp?cat=3")
    df.to_sql('industry_category', engine, index=False, if_exists="replace")
    db.close()
    end = time.time()
    print("處理完畢，耗時：", (end - start), "秒")
