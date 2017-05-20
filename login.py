# -*- coding:utf-8 -*-
import requests
import termcolor
import sys
import re
from conf import session, headers, login_url, home_page_url, mission_url
from bs4 import BeautifulSoup as BS


class Logging:
    flag = True

    @staticmethod
    def error(msg):
        if Logging.flag:
            print "".join([termcolor.colored("ERROR", "red"), ": ", termcolor.colored(msg, "white")])

    @staticmethod
    def warn(msg):
        if Logging.flag:
            print "".join([termcolor.colored("WARN", "yellow"), ": ", termcolor.colored(msg, "white")])

    @staticmethod
    def info(msg):
        if Logging.flag:
            print "".join([termcolor.colored("INFO", "magenta"), ": ", termcolor.colored(msg, "white")])

    @staticmethod
    def debug(msg):
        if Logging.flag:
            print "".join([termcolor.colored("DEBUG", "magenta"), ": ", termcolor.colored(msg, "white")])

    @staticmethod
    def success(msg):
        if Logging.flag:
            print "".join([termcolor.colored("SUCCESS", "green"), ": ", termcolor.colored(msg, "white")])

# Setting Logging
Logging.flag = True


class LoginPasswordError(Exception):
    def __init__(self, message):
        if type(message) != type("") or message == "":
            self.message = u"帐号密码错误"
        else:
            self.message = message
        Logging.error(self.message)


class NetworkError(Exception):
    def __init__(self, message):
        if type(message) != type("") or message == "":
            self.message = u"网络异常"
        else:
            self.message = message
        Logging.error(self.message)

username = ''   # your v2ex username
password = ''    # your v2ex password


# 获取登录参数
def get_login_data():
    content = session.get(login_url, headers=headers).content
    soup = BS(content, "html.parser")
    once_value = soup.find('input', attrs={"name": "once"}).get('value')
    psw_param = soup.find('input', attrs={"type": "password"}).get('name')
    user_param = soup.find('input', attrs={"autofocus": "autofocus"}).get('name')
    hidden_param = '/'
    data = {
        user_param: username,
        psw_param: password,
        "next": hidden_param,
        "once": once_value
    }
    return data


# 判断是否登录
def is_login():
    try:
        index = session.get(home_page_url, headers=headers).content
    except:
        print termcolor.colored("网络故障,请检查您的网络设置", "yellow")
        sys.exit()
    soup = BS(index, 'html.parser')
    login_flag = soup.find('a', href='https://workspace.v2ex.com/')
    if login_flag:
        # print termcolor.colored("已经登录过啦", "magenta")
        user = re.findall(r'<a href="/member/.*?">(.*?)</a>', index)[0]
        return True, user
    else:
        print termcolor.colored("请您登录...", "magenta")
        return False, None


def login():
    # print u'输入用户名'.decode('utf-8').encode('gbk')
    global username, password
    username = raw_input(termcolor.colored('输入用户名: ', 'cyan'))
    password = raw_input(termcolor.colored('输入密码: ', 'cyan'))
    data = get_login_data()
    resp = session.post(login_url, data=data, headers=headers)
    return resp


def mission():
    content = session.get(mission_url, headers=headers).content
    soup = BS(content, "html.parser")
    # 获取领取金币的链接
    short_url = soup.find('input', attrs={'class': 'super normal button'}).get('onclick')
    start = short_url.find("'")
    end = short_url.find("'", start+1)
    final_url = home_page_url + short_url[start+1:end]
    page = session.get(final_url, headers=headers).content
    soup = BS(page, "html.parser")
    successful = soup.find('li', attrs={'class': 'fa fa-ok-sign'})
    if successful:
        Logging.success(u'领取金币成功！')
        # print termcolor.colored('领取金币成功！', 'green')
    else:
        Logging.error(u'领取金币失败！')
        # print termcolor.colored('领取金币失败！', 'red')


if __name__ == '__main__':
    flag, username = is_login()
    if flag:
        Logging.debug(u"你已经登录过咯")
    else:
        resp = login()
        if resp.status_code == 200:
            Logging.success(u'登录成功，正在领取金币...')
            page = session.get(mission_url, headers=headers).content
            soup = BS(page, "html.parser")
            is_attain = soup.find('li', attrs={'class': 'fa fa-ok-sign'})
            if is_attain:
                Logging.success(u'今日金币已领取！')
            else:
                mission()
        else:
            Logging.error(u'登录失败！')