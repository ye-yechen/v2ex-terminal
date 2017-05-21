# -*- coding:utf-8 -*-
import requests
from topic import Topic
import json
import os
import re
from login import login, is_login
from conf import clear, session, headers, format_time, home_page_url
import termcolor
import globlevalue

op_stop = False
offset = 0
temp = 0
limit = 5
latest_topics = []


def help():
    info = "\n" \
           "**********************************************************\n" \
           "**\n" \
           "**  latest:  最新话题\n" \
           "**  me:      个人信息\n" \
           "**  Num:     选中具体TL条目进行操作(Num 为话题的id)\n" \
           "**  help:    帮助\n" \
           "**  clear:   清屏\n" \
           "**  quit:    退出系统\n" \
           "**\n" \
           "**********************************************************\n"
    print termcolor.colored(info, "green")


def bye():
    global op_stop
    op_stop = True
    print termcolor.colored("Bye", "cyan")
    print termcolor.colored("有任何建议欢迎与我联系: yczll678@163.com", "cyan")


def exit():
    global op_stop
    op_stop = True
    print termcolor.colored("因网络故障程序退出,请检查您的网络设置", "yellow")


def latest():
    topics = []
    hot_url = "https://www.v2ex.com/api/topics/latest.json"
    response = session.get(hot_url)
    json_data = json.loads(response.content)
    index = 0
    for data in json_data:
        topic = Topic()
        topic.id = data.get('id')
        topic.title = data.get('title')
        topic.url = data.get('url')
        topic.content = data.get('content')
        topic.author = data.get('member').get('username')
        topic.node_title = data.get('node').get('title')
        topic.node_url = data.get('node').get('url')
        topic.time = format_time(data.get('created'))
        topic.replies = data.get('replies')
        topics.append(topic)
        id = termcolor.colored(str(index), 'red')
        time = termcolor.colored(topic.time, 'white')
        title = termcolor.colored(topic.title, 'blue') + \
                termcolor.colored("(" + topic.author + ")", 'green')
        tag = termcolor.colored(u"节点: "+topic.node_title, 'cyan')
        info = '\n'.join([id+'\t\t'+time, title, tag]) + '\n'
        index += 1
        print info

    global latest_topics
    latest_topics = topics


def me():
    url = home_page_url + "/api/members/show.json?username=" + globlevalue.username
    response = session.get(url)
    data = json.loads(response.content)
    id = data.get('id')
    name = data.get('username')
    website = data.get('website')
    twitter = data.get('twitter')
    github = data.get('github')
    location = data.get('location')
    tagline = data.get('tagline')
    bio = data.get('bio')
    time = format_time(data.get('created'))

    tmp_star = "*****************************************************************************"
    star = termcolor.colored(tmp_star, 'green')
    info = termcolor.colored(name, "red") \
           + termcolor.colored(" (" + tagline + " )", "green")
    website = termcolor.colored("website: " + website, "blue")
    github = termcolor.colored("github: " + github, "blue")
    twitter = termcolor.colored("twitter: " + twitter, "blue")
    location = termcolor.colored("location: " + location, "blue")
    bio = termcolor.colored("bio: " + bio, "blue")
    line = termcolor.colored(u"V2EX 第 {id} 号会员,加入于 {time} .".format(id=id, time=time), "blue")
    print "\n".join([star, info, website, github, twitter, location, bio, line, star]) + "\n"


# 获取当前登录用户的注册时间秒数
def get_my_time():
    url = home_page_url + "/api/members/show.json?username=" + globlevalue.username
    response = session.get(url)
    data = json.loads(response.content)
    time = data.get('created')
    globlevalue.time = time


def welcome():
    clear()
    get_my_time()
    print termcolor.colored(u"Hello {name}, 欢迎使用终端版V2EX".format(name=globlevalue.username), "yellow")


def error():
    print termcolor.colored(u"输入错误, 可通过", "red") + termcolor.colored("help", "cyan") + termcolor.colored(u"查看", "red")


main_ops = {
    "latest": latest,
    "me": me,
    "clear": clear,
    "quit": bye,
    "exit": bye,
    "help": help
}


def work():
    global offset
    global temp
    global op_stop
    op_stop = False
    mode = re.compile(r"^\d+$")
    welcome()
    while not op_stop:
        op = raw_input("Time Line$ ")
        if not re.match(mode, op.strip()):
            main_ops.get(op, error)()
        else:
            opn = int(op)
            if opn < len(latest_topics):
                topic = latest_topics[opn]
                topic.operate(topic)
            else:
                print termcolor.colored("请输入正确的序号", "red")


# if __name__ == '__main__':
#     work()
