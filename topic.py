# -*- coding:utf-8 -*-
from conf import session, headers, base_topic_url
import termcolor
from conf import clear, format_time
from selenium import webdriver
import json
from bs4 import BeautifulSoup as BS
from answer import Answer


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

    def answer(self, topic):
        answer_list = []
        url = "https://www.v2ex.com/api/replies/show.json?topic_id="+str(topic.id)
        response = session.get(url)
        json_data = json.loads(response.content)
        for data in json_data:
            answer = Answer()
            answer.id = data.get('id')
            answer.thanks = data.get('thanks')
            answer.content = data.get('content')
            answer.author = data.get('member').get('username')
            answer.time = format_time(data.get('created'))
            answer_list.append(answer)
        return answer_list

    def collect(self, topic):
        url = base_topic_url + str(topic.id)
        driver = webdriver.PhantomJS("D:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        driver.get(url)
        resp = driver.page_source
        print resp
        soup = BS(resp, 'html.parser')
        div = soup.find('div', class_="topic_buttons")
        print div
        result = div.contents[1]
        print result

    def ignore(self, topic):
        pass

    def thanks(self, topic):
        pass

    def help(self):
        info = "\n" \
               "*************************************************************************\n" \
               "**\n" \
               "**  answer:     查看回答\n" \
               "**  author:     查看话题的作者\n" \
               "**  collect:    收藏话题\n" \
               "**  ignore:     忽略话题\n" \
               "**  thx:        感谢话题作者\n" \
               "**  pwd:        查看当前条目内容\n" \
               "**  clear:      清屏\n" \
               "**  break:      返回上级操作目录\n" \
               "**\n" \
               "************************************************************************\n"
        print termcolor.colored(info, "green")

    def operate(self, topic):
        self.topic_detail(topic)

        while True:
            op = raw_input("Topic$ ")
            if op == "answer":
                answer = Answer()
                answer_list = self.answer(topic)
                answer.operate(answer_list)
            elif op == "author":
                pass
            elif op == "collect":
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



