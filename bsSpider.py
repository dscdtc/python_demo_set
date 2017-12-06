# -*- coding: utf-8 -*-
'''
Created on 2017年7月1日

@author: dscdtc
'''

# import sys 
# reload(sys) 
# sys.setdefaultencoding('utf8')
import re
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs

cookie = 'authid=2AF6BAB99891EE185309E19096C613B1634F30C99DCE170AAB168C4643AC879FD69A477843035A9A7B1A29E58D1CE249D9BA7D100DE1D5A5ECF463BBE79B04002B28EC21B3176A05E648E88B885C961F86F5134000051D8BEC6469DEFA2578AF37D902733EE5A2B90CACE859C6DCB750CB830B26D38713CA3B6C2F34F9DDF0786D3615AEEC7FCD13A101C511AAB2D3825B0BEC54081ABC7A2E26B54FF40AC7F8EE7CB7A99328EF6D13A5EA941F027717D288482BFF3C2CC2C0695377258BB666B767AC1E; domain=ppdai.com; path=/; HttpOnly'

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

class fuckPPD():

    def __init__(self):
        self.s = requests.Session()
        self.s.headers = headers
        requests.adapters.DEFAULT_RETRIES = 5

    def get_page(self,url):
        
        req = self.s.get(url)
        return req.content

    def run(self, name):
        # name = 'pdu7775878530'
        url = 'https://www.ppdai.com/user/%s?page=1' % name
        #page=requests.get(TARGET_URL,headers=headers)
        page = self.get_page(url)
        soup = bs(page, 'html5lib')
        print(soup)
        gender = soup.select(".user_li p span")[0].text.strip().strip("\n").encode('utf-8')
        age = soup.select(".user_li p span")[1].text.strip().strip(u'岁').strip("\n").encode('utf-8')
        signup_time = soup.select(".reg_login_li p")[0].text.strip().strip(u"注册时间：").strip("\n").encode('utf-8')


        t = time.strptime(signup_time, "%Y/%m/%d")
        y, m, d = t[0:3]
        signup_time = datetime(y,m,d).strftime('%Y年%m月%d日')

        try:
            history = soup.select(".my-f-r-m-tab #li3")[0].text.strip().strip("\n").encode('utf-8')
        except:
            history = None

        if history:
            bid_times = soup.select("td.cf7971a")[0].text.strip().strip("\n").encode('utf-8')
            badbid_rate = soup.select("td.cf7971a span")[0].text.encode('utf-8')
            bid_rate = soup.select("td.cf7971a span")[1].text.encode('utf-8')

            if '次' not in bid_times:
                bid_times = 0
            try:
                bid_times = int(bid_times.strip('次'))
            except:
                pass

            lt_info = {
                'gender' : gender,
                'signup_time' : signup_time,
                'bid_times' : bid_times,
                'badbid_rate' : badbid_rate,
                'bid_rate' : bid_rate
            }

        else:
            lt_info = {
                'gender' : gender,
                'signup_time' : signup_time,
                'bid_times' : 0,
                'badbid_rate' : '0.00',
                'bid_rate' : '0.00'
            }

        # print lt_info
        return lt_info

if __name__ == '__main__':
    crawler = fuckPPD()
    info = crawler.run('pdu7775878530')
    print(info)
