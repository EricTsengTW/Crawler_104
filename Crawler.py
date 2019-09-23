#!/usr/bin/env python
# coding: utf-8
# 爬蟲主要功能在此

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import time


class Crawler:

    ### 爬取職類資訊、各種職類的網址(針對一個url)|output:DataFrame ###
    def job_category(url):
        # 準備空表格
        df = pd.DataFrame(columns=["職務大類", "職務中類", "中類網址", "職類名稱", "職類網址", "職缺數量", "職類編號"])

        # 找到內容網址
        head = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=head)
        res.encoding = "utf8"  # 避免python以ISO-8859-1輸出亂碼
        html = BeautifulSoup(res.text)

        # 先找出各職業大類下，有多少職務中類，以及各類的網址
        cate_title = html.find("ul", class_="cate-title").find_all("h3")  # 職務大類 name list
        cate_list_1 = html.find_all("ul", class_="cate-list")  # 職務中類 data list

        for i in range(len(cate_title)):
           for li in cate_list_1[i].find_all("li"):
                # 職務大類名稱
                title0 = cate_title[i].text
                # 職務中類名稱、網址
                title1 = li.find("a").text
                href1 = "https://www.104.com.tw/" + li.find("a")["href"]

                # 進入中類網址，找到各種職類名稱及其網址
                res2 = requests.get(href1, headers=head)
                res2.encoding = "utf8"
                html2 = BeautifulSoup(res2.text)
                cate_list_2 = html2.find("div", class_="second-step").find_all("li")

                for li2 in cate_list_2:
                    title2 = li2.find("a").text
                    href2 = "www.104.com.tw/" + li2.find("a")["href"]
                    num = li2.find("span", class_="num").text
                    cate_id = href2.split("no=")[1].split("&")[0]
                    data = {"職務大類": title0,
                            "職務中類": title1,
                            "中類網址": href1,
                            "職類名稱": title2,
                            "職類網址": href2,
                            "職缺數量": num,
                            "職類編號": cate_id
                            }

                    # 放入表格中
                    df = df.append(data, ignore_index=True)
        return df

    ### 計算各職類的職缺頁數|output:int ###
    def job_page(url):
        head = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=head)
        res.encoding = "utf8"
        html = BeautifulSoup(res.text)
        script = html.find("body").find_all("script")[3].text
        num = int(script.split("var")[3].split(":")[-1].split("}")[0])
        page = num // 20 + 1
        return page


    ### 爬取職缺網址(針對單一url)|output:DataFrame ###
    def job_link(url):
        head = {'User-Agent':'Mozilla/5.0'}
        res = requests.get(url, headers=head)
        time.sleep(0.5) # 休息供網頁讀取
        res.encoding = "utf8"
        html = BeautifulSoup(res.text)
        df = pd.DataFrame(columns=["職類編號", "職務名稱", "職缺連結", "公司名稱", "公司連結"])

        # 找到每個職缺資訊的內容位置
        job_link = html.find_all("article", class_="job-list-item")
        # html.find("div", id="js-job-list").

        for j in job_link:
            # 職務名稱
            jobtitle = j.find("a", class_="js-job-link").text
            # 職缺連結
            joblink = j.find("a", class_="js-job-link")["href"].replace("//","")
            # 公司名稱
            companyname = j.find("ul", class_="b-list-inline").find("a").text.strip()
            # 公司連結
            companylink = j.find("ul", class_="b-list-inline").find("a")["href"].replace("//","")
            # 職務類型
            jobcategory = url.split("jobcat=")[1].split("&")[0]

            data = {"職類編號": jobcategory,
                    "職務名稱": jobtitle,
                    "職缺連結": joblink,
                    "公司名稱": companyname,
                    "公司連結": companylink,
                    }

            df = df.append(data, ignore_index=True)

        return df

    ### 爬取職缺的網頁資訊(針對一個url)|output:dictionary ###
    def job_content(url):
        # 找到內容網址
        head = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=head)
        time.sleep(0.3)  # 休息供網頁讀取
        html = BeautifulSoup(res.text)
        saved = {}

        # 資料區塊
        sec = html.find_all("section", class_="info")  # 主要區塊list
        s1 = sec[0]  # 工作內容區塊
        s2 = sec[1]  # 條件要求區塊
        s3 = sec[2]  # 公司福利區塊
        s4 = sec[3]  # 聯絡方式區塊

        # 開始抓資料囉：公司名稱、職稱、應徵人數
        comp = html.find("a", class_="cn").text
        compl = html.find("a", class_="cn")["href"]
        title = html.find("title").text.split("｜")[0]
        vol = html.find("div", class_="sub").find_all("a")[0].text.replace("\n", "")

        saved["職缺網址"] = url
        saved["公司名稱"] = comp
        saved["職務名稱"] = title
        saved["資料來源"] = "104"

        # 開始抓資料囉：工作內容
        workcont = {}
        wclc = s1.find_all("dt")  # [欄位]list
        wcl = s1.find_all("dd")  # [資料]list

        wc = s1.find("div", class_="content").find("p")
        wc = wc.prettify().replace("<p>", "").replace("</p>", "").replace("<br/>", "").replace("\n", "").strip()
        workcont["工作內容"] = wc

        for i in range(len(wclc)):
            if "職務類別" in wclc[i].text:
                jc = wcl[i].find_all("span", class_="")
                jc = str(jc).replace("<span>", "").replace("</span>", "").replace("[", "").replace("]", "")
                workcont["職務類別"] = jc
            elif "工作待遇" in wclc[i].text:
                sa = wcl[i].text.split("\n")[0].strip()
                workcont["工作待遇"] = sa
            elif "上班地點" in wclc[i].text:
                lc = wcl[i].prettify().split("\n")[1].strip()
                workcont["上班地點"] = lc
            else:
                culumn = wclc[i].text.replace("：", "")
                workcont[culumn] = wcl[i].text.replace("\n", "").strip()

        saved["工作內容"] = workcont

        # 開始抓資料囉：條件要求
        workreq = {}
        wqc = s2.find_all("dt")  # [欄位]list
        wql = s2.find_all("dd")  # [資料]list

        # 條件列表與內容(每個職缺不同，故寫迴圈)
        for i in range(len(wql)):
            culumn = wqc[i].text.replace("：", "")
            workreq[culumn] = wql[i].text.replace("\n", "").replace("\r", "").strip()

        saved["條件要求"] = workreq

        # 開始抓資料囉：公司福利
        bn = s3.find("div", class_="content").find("p")
        bn = bn.prettify().replace("<br>", "").replace("<br/>", "").replace("<p>", "").replace("</p>", "").replace("\n", "").strip()
        saved["公司福利"] = bn

        # 開始抓資料囉：聯絡方式
        ct = s4.find("dd").text
        saved["聯絡方式"] = ct

        # 開始抓資料囉：資料更新時間
        ud = html.find("time", class_="update").text.replace("更新日期：", "")
        saved["更新時間"] = ud

        # 開始抓資料囉：公司連結、資料來源
        saved["公司連結"] = compl
        saved["應徵人數"] = vol

        return saved

    ### 爬取公司的資訊(針對一個url)|output:dictionary ###
    def company_info(url):
        saved = {}

        # 找到內容網址
        json_url = "https://www.104.com.tw/company/ajax/content/" + url.split("/")[4].split("?")[0]
        res = urlopen(json_url)
        time.sleep(0.3)
        data = json.load(res)
        # res2 = requests.get(json_url)  也可以用這種方式requests
        # print(res2.json())

        # 找到資料位置
        saved["公司網址"] = url
        saved["公司名稱"] = data["data"]["custName"]
        saved["產業類型"] = data["data"]["industryDesc"]
        saved["產業描述"] = data["data"]["indcat"]
        saved["資本額"] = data["data"]["capital"]
        saved["員工人數"] = data["data"]["empNo"]
        saved["聯絡人"] = data["data"]["hrName"]
        saved["電話"] = data["data"]["phone"]
        saved["傳真"] = data["data"]["fax"]
        saved["地址"] = data["data"]["address"]
        saved["官網連結"] = data["data"]["custLink"]
        saved["公司介紹"] = data["data"]["profile"].replace("\n", "").replace("\t", "").replace("\r", "").strip()
        saved["主要商品"] = data["data"]["product"].replace("\n", "").replace("\t", "").replace("\r", "").strip()
        saved["福利制度"] = data["data"]["welfare"].replace("\n", "").replace("\t", "").replace("\r", "").strip()

        return saved