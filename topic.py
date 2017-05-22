# -*- coding:utf-8 -*-
from conf import session, headers, base_topic_url
import termcolor
from conf import clear, format_time, home_page_url
import json
from bs4 import BeautifulSoup as BS
from answer import Answer
from user import User
import globlevalue

try:
    session.cookies.load(ignore_discard=True)
except:
    pass

once = ""


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
        return answer_list, topic.replies

    def collect(self, topic):
        topic_url = base_topic_url + str(topic.id)
        resp = session.get(topic_url, headers=headers)
        soup = BS(resp.content, 'html.parser')
        div = soup.find('div', class_="topic_buttons")
        # 获取 “收藏” 的url
        collect_url_a = div.contents[1]
        tmp_url = collect_url_a['href']
        collect_url = home_page_url + tmp_url
        # # 获取 once 值
        # global once
        # once = soup.find('input', attrs={"name": "once"}).get("value")
        # # once 加入全局变量
        # globlevalue.once = once
        resp = session.get(collect_url, headers=headers)
        if resp.status_code == 200:
            print termcolor.colored(u"收藏话题成功.", "green")
        else:
            print termcolor.colored(u"收藏话题失败.", "red")

    def author_info(self, topic):
        author_url = home_page_url+"/api/members/show.json?username="+topic.author
        response = session.get(author_url)
        data = json.loads(response.content)
        user = User()
        user.id = data.get('id')
        user.name = data.get('username')
        user.website = data.get('website')
        user.twitter = data.get('twitter')
        user.github = data.get('github')
        user.location = data.get('location')
        user.tagline = data.get('tagline')
        user.bio = data.get('bio')
        user.time = format_time(data.get('created'))
        return user

    def ignore(self, topic):
        # ignore_url = home_page_url + "/ignore/topic/"+str(topic.id)+"/?once="+once
        pass

    def thanks(self, topic):
        pass

    def help(self):
        info = "\n" \
               "*************************************************************************\n" \
               "**\n" \
               u"**  answer:     查看回答\n" \
               u"**  author:     查看话题的作者\n" \
               u"**  collect:    收藏话题\n" \
               u"**  ignore:     忽略话题\n" \
               u"**  thx:        感谢话题作者\n" \
               u"**  clear:      清屏\n" \
               u"**  back:       返回上级操作目录\n" \
               "**\n" \
               "************************************************************************\n"
        print termcolor.colored(info, "green")

    def operate(self, topic):
        self.topic_detail(topic)

        while True:
            op = raw_input("Topic$ ")
            if op == "answer":
                answer = Answer()
                answer_list, replies = self.answer(topic)
                answer.operate(answer_list, replies)
            elif op == "author":
                user = self.author_info(topic)
                user.operate(user)
            elif op == "thx":
                print termcolor.colored(u"暂不支持!", "red")
            elif op == "ignore":
                print termcolor.colored(u"暂不支持!", "red")
            elif op == "collect":
                self.collect(topic)
            elif op == "help":
                self.help()
            elif op == "back":
                break
            elif op == "clear":
                clear()
            else:
                self.error()



