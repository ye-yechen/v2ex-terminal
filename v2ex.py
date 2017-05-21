# -*- coding:utf-8 -*-
from login import login, is_login, Logging, mission
from conf import session, mission_url, headers, format_time, base_topic_url
from bs4 import BeautifulSoup as BS
import os
from operate import work
import globlevalue
from PIL import Image
import termcolor

try:
    session.cookies.load(ignore_discard=True)
except:
    pass

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def get_once():
    topic_url = base_topic_url + str(362683)
    resp = session.get(topic_url, headers=headers)
    soup = BS(resp.content, 'html.parser')
    once = soup.find('input', attrs={"name": "once"}).get("value")
    # once 加入全局变量
    globlevalue.once = once


# 将256灰度映射到70个字符上
def getchar(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126*r + 0.7152*g + 0.0722*b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray/unit)]


def get_logo():
    img = Image.open('v2ex.png')
    w, h = img.size
    img.resize((w, h), Image.NEAREST)
    txt = ""
    for i in range(h):
        for j in range(w):
            txt += getchar(*img.getpixel((j, i)))
        txt += '\n'
    return txt


def main():
    txt = get_logo()
    print termcolor.colored(txt, "cyan")
    if not os.path.exists("cookies"):
        flag, username = is_login()
        # 用户名放入全局变量
        globlevalue.username = username
        if flag:
            Logging.debug(u"你已经登录过咯")
        else:
            resp = login()
            if resp.status_code == 200:
                Logging.success(u'登录成功，正在领取金币...')
                session.cookies.save()
                get_once()
                page = session.get(mission_url, headers=headers).content
                soup = BS(page, "html.parser")
                is_attain = soup.find('li', attrs={'class': 'fa fa-ok-sign'})
                if is_attain:
                    Logging.success(u'今日金币已领取！')
                    work()
                else:
                    mission()
                    work()
            else:
                Logging.error(u'登录失败！')
    else:
        get_once()
        flag, username = is_login()
        # 用户名放入全局变量
        globlevalue.username = username
        page = session.get(mission_url, headers=headers).content
        soup = BS(page, "html.parser")
        is_attain = soup.find('li', attrs={'class': 'fa fa-ok-sign'})
        if is_attain:
            Logging.success(u'今日金币已领取！')
        else:
            mission()
        work()


if __name__ == '__main__':
    main()
