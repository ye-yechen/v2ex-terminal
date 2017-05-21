# -*- coding:utf-8 -*-
import requests
import time
import cookielib
import os

headers = {
        "Host": "www.v2ex.com",
        "Referer": "https://www.v2ex.com/signin",
        "Origin": "https://www.v2ex.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
session = requests.session()
session.cookies = cookielib.LWPCookieJar('cookies')
login_url = 'https://v2ex.com/signin'
home_page_url = 'https://www.v2ex.com'
mission_url = 'https://www.v2ex.com/mission/daily'
base_topic_url = 'https://www.v2ex.com/t/'


def format_time(seconds):
    local_time = time.localtime(seconds)
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time)


def clear():
    i = os.system("cls")  # windows linux->clear

# 显示用户的主题：/api/topics/show.json?username=xiqingongzi
# 回复：https://www.v2ex.com/api/replies/show.json?topic_id=362535
# 某个节点的主题：/api/topics/show.json?node_name=v2ex
# 查看具体的Node信息：/api/nodes/show.json?name=YourNodeName
# 某个用户的信息：/api/members/show.json?username=Livid
