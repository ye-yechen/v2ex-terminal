# -*- coding:utf-8 -*-
import requests
import time
import cookielib
import os
import platform
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS


headers = {
        "Host": "www.v2ex.com",
        "Referer": "https://www.v2ex.com/signin",
        "Origin": "https://www.v2ex.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \ '
                      '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
session = requests.session()
session.cookies = cookielib.LWPCookieJar('cookies')
login_url = 'https://v2ex.com/signin'
home_page_url = 'https://www.v2ex.com'
mission_url = 'https://www.v2ex.com/mission/daily'
base_topic_url = 'https://www.v2ex.com/t/'
topic_urls = []


def search(key):    # 搜索
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome()
    driver.get(home_page_url)
    try:
        wait = WebDriverWait(driver, 10)
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        search_input.clear()
        search_input.send_keys(key)
        search_input.send_keys(Keys.ENTER)  # 回车键
        driver.switch_to.window(driver.window_handles[1])   # 切换到跳转后的页面
        # print driver.current_url
        for _ in range(5):
            total_result = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#resultStats"))
            )
            if total_result.text:
                get_search_results(driver.page_source)
                next_page = driver.find_element_by_id("pnnext")
                next_page.click()
        return topic_urls
    except TimeoutException:
        print "TimeoutException..."
        search(key)     # 超时重新请求
    finally:
        driver.quit()


def get_search_results(page_source):   # 解析搜索结果
    soup = BS(page_source, 'html.parser')
    links = soup.find_all('cite')   # 获取包含话题链接的<cite>标签
    global topic_urls
    [topic_urls.append(link.string) for link in links if link.string.startswith('https')]


# 将时间秒数格式化
def format_time(seconds):
    local_time = time.localtime(seconds)
    return time.strftime("%Y-%m-%d %H:%M:%S", local_time)


# 调用系统的清屏命令
def clear():
    if platform.system() == "Windows":
        i = os.system("cls")
    else:
        i = os.system("clear")


# 过滤表情
def filter_emoji(input_str, replace_str=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(replace_str, input_str)

# 显示用户的主题：/api/topics/show.json?username=xiqingongzi
# 回复：https://www.v2ex.com/api/replies/show.json?topic_id=362535
# 某个节点的主题：/api/topics/show.json?node_name=v2ex
# 查看具体的Node信息：/api/nodes/show.json?name=YourNodeName
# 某个用户的信息：/api/members/show.json?username=Livid
