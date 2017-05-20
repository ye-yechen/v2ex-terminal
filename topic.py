# -*- coding:utf-8 -*-
from conf import session, headers
import termcolor
from conf import clear
import re
from bs4 import BeautifulSoup as BS


class Topic:

    def __init__(self):
        pass

    def topic_detail(self, topic):
        id = termcolor.colored(topic.id, 'red')
        time = termcolor.colored(topic.time, 'white')
        title = termcolor.colored(topic.title, 'blue') + \
                termcolor.colored("(" + topic.author + ")", 'green')
        content = termcolor.colored(topic.content, 'magenta')
        tag = termcolor.colored(u"节点: " + topic.node_title, 'cyan')
        info = '\n'.join([id + '\t\t' + time, title, content, tag]) + '\n'
        print info

    def error(self):
        print termcolor.colored(u"输入错误, 可通过", "red") + termcolor.colored("help", "cyan") + termcolor.colored(u"查看","red")

    def help(self):
        info = "\n" \
               "*************************************************************************\n" \
               "**\n" \
               "**  answer:     查看回答(仅当TL条目与回答相关时)\n" \
               "**  author:     查看回答的作者(仅当TL条目与回答相关时)\n" \
               "**  pwd:        查看当前TL条目内容\n" \
               "**  clear:      清屏\n" \
               "**  break:      返回上级操作目录\n" \
               "**  quit:       退出系统\n" \
               "**\n" \
               "************************************************************************\n"
        print termcolor.colored(info, "green")

    def operate(self, topic):
        self.topic_detail(topic)

        while True:
            op = raw_input("Topic$ ")
            if op == "answer":
                pass
            elif op == "author":
                pass
            elif op == "help":
                self.help()
            elif op == "break":
                break
            elif op == "clear":
                clear()
            elif op == "quit":
                return True
            else:
                self.error()



