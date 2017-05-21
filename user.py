# -*- coding:utf-8 -*-
import termcolor
from conf import clear, home_page_url, headers, session
import globlevalue
import json

try:
    session.cookies.load(ignore_discard=True)
except:
    pass


class User:

    def __init__(self):
        pass

    def error(self):
        print termcolor.colored(u"输入错误, 可通过", "red") + termcolor.colored("help", "cyan") + termcolor.colored(u"查看","red")

    def help(self):
        info = "\n" \
               "*************************************************************************\n" \
               "**\n" \
               "**  focus:      关注用户\n" \
               "**  block:      屏蔽用户\n" \
               "**  topics:     查看用户的主题\n" \
               "**  clear:      清屏\n" \
               "**  back:      返回上级操作目录\n" \
               "**\n" \
               "************************************************************************\n"
        print termcolor.colored(info, "green")

    def show_author_info(self, author):
        tmp_star = "*****************************************************************************"
        star = termcolor.colored(tmp_star, 'green')
        info = termcolor.colored(author.name, "red") \
               +termcolor.colored(" ("+author.tagline+" )", "green")
        website = termcolor.colored("website: "+author.website, "blue")
        github = termcolor.colored("github: "+author.github, "blue")
        twitter = termcolor.colored("twitter: "+author.twitter, "blue")
        location = termcolor.colored("location: "+author.location, "blue")
        bio = termcolor.colored("bio: "+author.bio, "blue")
        line = termcolor.colored(u"V2EX 第 {id} 号会员,加入于 {time} .".format(id=author.id, time=author.time), "blue")
        print "\n".join([star, info, website, github, twitter, location, bio, line, star]) + "\n"

    def focus(self, author):
        focus_url = home_page_url+"/follow/" + str(author.id) + "?once="+str(globlevalue.once)
        response = session.get(focus_url, headers=headers)
        if response.status_code == 200:
            print termcolor.colored("已关注 {name}.".format(name=author.name), "green")
        else:
            print termcolor.colored("关注失败.", "red")

    def block(self, author):
        # 这个 t 参数是当前登录用户注册的时间浮点数
        block_url = home_page_url+"/block/" + str(author.id) + "?t="+str(globlevalue.time)
        response = session.get(block_url, headers=headers)
        if response.status_code == 200:
            print termcolor.colored("已屏蔽 {name}.".format(name=author.name), "green")
        else:
            print termcolor.colored("屏蔽失败.", "red")

    # def topics(self, author):
    #     url = home_page_url+"/api/topics/show.json?username="+author.name
    #     response = session.get(url)
    #     data = json.loads(response.content)

    def operate(self, author):
        self.show_author_info(author)
        while True:
            op = raw_input("Author$ ")
            if op == "focus":
                self.focus(author)
            elif op == "block":
                self.block(author)
            elif op == "topics":
                pass
            elif op == "help":
                self.help()
            elif op == "back":
                break
            elif op == "clear":
                clear()
            else:
                self.error()
