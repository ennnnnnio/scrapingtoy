################インポート################
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import random
import re
################インポート################



################可変値################
# ターゲットURL
targetUrl = 'https://www.youtube.com/watch?v=gSl2ex-3Abc'
# この時間(秒)でターゲットURLにアクセスできないプロキシは使わない
PermissionTime = 5
# スクレイピングするインターバルタイム(秒)
# intervalTime = random.randint(900,10800)　15分～3時間のランダム
intervalTime = 600
# chromedriverパス
chromePath = r"/WebDrivers/chromedriver"
################可変値################



################固定値################
# プロキシサイトのURL
proxyUrl = 'http://www.cybersyndrome.net/plr6.html'
################固定値################



################関数群################
# プロキシのリストをスクレイピングする関数
def getProxy():
    # seleniumの設定、ヘッダーレスモードとクロームのパスを指定
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chromePath,chrome_options=options)
    # サイトへアクセス
    driver.get(proxyUrl)

    # BeautifulSoupさんにhtmlのソースを見やすくしてもらう
    soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
    data = soup.find_all('td', id=re.compile("^n")) #正規表現でIDを取得

    # クローム閉じる
    driver.close()

    # プロキシを整形して配列に入れる
    proxyList = []
    for proxyT in data:
        proxyList.append('http://'+proxyT.text)
    return proxyList

# プロキシの選定関数
def is_bad_proxy(pip):
    try:
        # seleniumの設定、プロキシを通してクロームのパスを指定
        options = Options()
        options.add_argument("--proxy-server=" + pip)
        # options.add_argument('--headless') stackflow曰くヘッダーレスとプロキシは同時で使用できないらしい
        driver = webdriver.Chrome(chromePath,chrome_options=options)
        # webサイトへのタイムアウト時間を設定。もしこの時間内にアクセスできないならexceptに入る
        driver.set_page_load_timeout(PermissionTime)
        # アクセスして閉じる
        driver.get(targetUrl)
        driver.close()
    except:
        driver.close()
        print("タイムアウト")
        return True
    return False

# プロキシのリストをまわして、いいプロキシを見つける。見つからなかったらNoneを返す
def checkProxy(proxys):
    temp = None
    for item in proxys:
        if is_bad_proxy(item):
            print("Bad Proxy:", item)
        else:
            print("Nice Proxy:", item)
            temp = item
            break
    else:
        return None
    return temp
################関数群################



################メイン################
# 無限ループ
while(True):
    # プロキシを取得していいプロキシを見つける
    proxys = getProxy()
    good_proxy = checkProxy(proxys)

    # いいプロキシがあったら処理する
    if good_proxy is not None:

        ################スクレイピングする処理(javascriptない場合)################
        proxies = {'http': good_proxy}
        html = requests.get(targetUrl, proxies=proxies)
        soup = BeautifulSoup(html.content, 'html.parser')
        # ちゃんとスクレイピング出来てるか表示
        print(soup)
        ################スクレイピングする処理(javascriptない場合)################



        ################スクレイピングする処理(javascriptある場合################
        # options = Options()
        # options.add_argument("--proxy-server=" + good_proxy)
        # # options.add_argument('--headless') stackflow曰くヘッダーレスとプロキシは同時で使用できないらしい
        # driver = webdriver.Chrome(chromePath,chrome_options=options)
        # driver.get(targetUrl)
        # soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')
        # driver.close()
        # # ちゃんとスクレイピング出来てるか表示
        # print(soup)
        ################スクレイピングする処理(javascriptある場合)################

    else:
        print("条件にマッチするプロキシがありません。")
    sleep(intervalTime)
################メイン################
