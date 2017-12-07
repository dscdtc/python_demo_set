#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2017年7月1日
@author: dscdtc
'''
# Python2 encoding setting
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup as bs

# Disable insecure warning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Spider():

    def __init__(self, url, cookie):
        headers={
            "Host": "",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            "Upgrade-Insecure-Requests": "1",
            'Connection': 'keep-alive',
            'Cookie': cookie
        }

        self.url = url
        self.s = requests.Session()
        self.s.headers = headers
        self.s.verify = False # Disable SSL verify
        requests.adapters.DEFAULT_RETRIES = 5

    def get_page(self,url):
        req = self.s.get(url)
        return req.content

    def run(self):
        try:
            page = self.get_page(self.url)
            soup = bs(page, 'html5lib')
            console_output = soup.select("pre.console-output")[0].text.strip().replace("\n", "\r\n").encode('utf-8')
            return console_output
        except Exception as e:
            print(e)


if __name__ == '__main__':

    TARGET_URL = ''
    COOKIE = ''
    crawler = Spider(TARGET_URL, COOKIE)
    info = crawler.run()
    with open('./console.txt', 'wb') as f:
        f.write(info)

    print("SUCCESS!!!")
