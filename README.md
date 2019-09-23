# Crawler_104
功能描述(Description):\
Crawler.py: 爬蟲主要功能在此\
MyConnect.py: 存取MySql功能在此\
s1: 將職類的資訊和網址，存入本地端MySQL\
s2: 將每個職類所擁有的職缺連結，全數存入本地端MySQL\
s3: 將職缺的資訊爬取下來，存成json檔至本地端\
s4: 將公司的資訊爬取下來，存成json檔至本地端

自行調整(You should modify):\
s1: egine = create_engine()內的MySQL資訊\
s2: egine = create_engine()內的MySQL資訊\
s3: dn = [directory] 要存放檔案的資料夾位置\
s4: dn = [directory] 要存放檔案的資料夾位置

注意(Attention)：\
s2未考慮同一職缺有多個職類所導致的連結重複問題，需自行在MySQL刪除重複的職缺連結
