# Crawler_104
功能描述(Description):\
Crawler.py: 爬蟲主要功能在此\
MyConnect.py: 存取MySql功能在此\
s1: 將職類的資訊和網址，存入本地端MySQL\
s2: 將每個職類所擁有的職缺連結，存入本地端MySQL\
s3: 將職缺的資訊爬取下來，存成json檔至本地端\
s4: 將公司的資訊爬取下來，存成json檔至本地端\
S5: 將產業類型的資訊爬取下來，存入至本地端MySQL

自行調整(You should modify):\
s1: egine = create_engine()內的MySQL資訊\
s2: egine = create_engine()內的MySQL資訊\
s3: dn = [directory] 要存放檔案的資料夾位置\
s4: dn = [directory] 要存放檔案的資料夾位置\
s5: dn = [directory] 要存放檔案的資料夾位置

注意(Attention)：\
一個職缺中，會有指向多個職業類型
但本爬蟲方式會導致「多個職類」皆有同一職缺連結，需自行在MySQL刪除重複的職缺連結
