from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sys
# ----------------------------------------------------

# 使用手冊:
#   和main.py同個路徑下放答案，答案名稱規則為a001.py a002.py ...以此類推


# ----------------------------------------------------
options = Options()
options.add_argument("--disable-notifications")

#如果有bug，請注意chromedriver與瀏覽器的版本
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
chrome.get("https://zerojudge.tw/Login")
time.sleep(20)#先登入

#作業環境判斷
system_os = sys.platform
if 'win' in system_os:
    path_slash = '\\'
else:
    path_slash = '/'

allFileList = os.listdir(os.getcwd())
for i in allFileList:
    try:
        if '.py' not in i or i == 'main.py' :
            continue
        try:
            url = 'https://zerojudge.tw/ShowProblem?problemid='+i[:4:]
            print(url)
            html = requests.get(url)
            html.encoding = 'UTF-8'
            sp = BeautifulSoup(html.text, 'html.parser')
            testlst = []
            title = sp.find('span', id='problem_title').text
            problem = sp.find_all('div', class_='panel-body')
        except:
            print({i}+'無此題目')
            continue

        chrome.get(f"https://zerojudge.tw/ShowProblem?problemid={i[:4:]}")
        time.sleep(3)
        submit_button = chrome.find_element(by="xpath", value="//button[@id='SubmitCode' and @class='btn btn-success']")
        submit_button.click()
        time.sleep(3)
        input_ans = chrome.find_element(by='xpath',value="//textarea[@id='code']")
        f = open(i, 'r',encoding="utf-8")
        input_ans.send_keys(f.read())
        f.close()
        time.sleep(1)
        upload = chrome.find_element(by="xpath", value="//button[@id='submitCode' and @class='btn btn-primary']")
        while 1:
            upload.click()
            time.sleep(1)
            try:
                wait_upload = chrome.find_element(by="xpath", value="//button[@id='btn-ok' and @class='btn btn-primary']")
            except:
                break
            wait_upload.click()
            time.sleep(1)
        time.sleep(3)
        
        os.remove(os.getcwd()+path_slash+i)
    except:
        print(i+'bug')
        continue
    
print('all finish')