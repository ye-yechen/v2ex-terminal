# -*- coding:utf-8 -*-
import requests
import time
import termcolor
import os

headers = {
        "Host": "www.v2ex.com",
        "Referer": "https://www.v2ex.com/signin",
        "Origin": "https://www.v2ex.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
session = requests.session()
login_url = 'https://v2ex.com/signin'
home_page_url = 'https://www.v2ex.com'
mission_url = 'https://www.v2ex.com/mission/daily'


def format_time(seconds):
    local_time = time.localtime(seconds)
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time)


def clear():
    i = os.system("cls") # windows linux->clear

