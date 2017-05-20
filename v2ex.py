# -*- coding:utf-8 -*-
from login import login, is_login, Logging, mission
from conf import session, mission_url, headers
from bs4 import BeautifulSoup as BS
import os
import cookielib
from operate import work

session.cookies = cookielib.LWPCookieJar('cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    pass


def main():
    if not os.path.exists("cookies"):
        flag, username = is_login()
        if flag:
            Logging.debug(u"你已经登录过咯")
        else:
            resp = login()
            if resp.status_code == 200:
                Logging.success(u'登录成功，正在领取金币...')
                session.cookies.save()
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
        work()


if __name__ == '__main__':
    main()