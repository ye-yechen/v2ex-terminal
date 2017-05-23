# -*- coding:utf-8 -*-
import requests
from topic import Topic
import json
import re
from login import login, is_login
from conf import clear, session, filter_emoji, format_time, home_page_url
import termcolor
import globlevalue

op_stop = False
offset = 0
temp = 0
limit = 5
result_topics = []


def bye():
    global op_stop
    op_stop = True
    print termcolor.colored("Bye", "cyan")
    print termcolor.colored(u"有任何建议欢迎与我联系: yczll678@163.com", "cyan")


def exit():
    global op_stop
    op_stop = True
    print termcolor.colored(u"因网络故障程序退出,请检查您的网络设置", "yellow")


def get_topics(url):
    topics = []
    response = session.get(url)
    json_data = json.loads(response.content)
    index = 0
    for data in json_data:
        topic = Topic()
        topic.id = data.get('id')
        topic.title = filter_emoji(data.get('title'))
        topic.url = data.get('url')
        topic.content = filter_emoji(data.get('content'))
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
        tag = termcolor.colored(u"节点: " + topic.node_title, 'cyan')
        info = '\n'.join([id + '\t\t' + time, title, tag]) + '\n'
        index += 1
        print info
    global result_topics
    result_topics = topics


def latest():
    latest_url = "https://www.v2ex.com/api/topics/latest.json"
    get_topics(latest_url)


def hot():
    hot_url = "https://www.v2ex.com/api/topics/hot.json"
    get_topics(hot_url)


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
           + termcolor.colored(" ( " + tagline + " )", "green")
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
    globlevalue.time = time     # 放入全局变量，这个参数在屏蔽用户时有验证


def about():
    site_info_url = "https://www.v2ex.com/api/site/info.json"
    site_stats_url = "https://www.v2ex.com/api/site/stats.json"
    resp_info = session.get(site_info_url)
    info = json.loads(resp_info.content)
    title = termcolor.colored(info.get('title'), "cyan")
    slogan = termcolor.colored(info.get('slogan'), "cyan")
    description = termcolor.colored(info.get('description'), "cyan")
    domain = termcolor.colored(info.get('domain'), "cyan")
    resp_stats = session.get(site_stats_url)
    stats = json.loads(resp_stats.content)
    topic_nums = termcolor.colored(u"共有 "+str(stats.get('topic_max'))+u" 个话题", "cyan")
    member_nums = termcolor.colored(u"共有 "+str(stats.get('member_max'))+u" 个用户", "cyan")
    tmp_star = "*****************************************************************************"
    star = termcolor.colored(tmp_star, 'green')
    show_info = "\n".join([star, title, slogan, description, domain, topic_nums, member_nums, star])
    print show_info


def get_topic_by_id(topic_id):
    url = "https://www.v2ex.com/api/topics/show.json?id="+str(topic_id)
    resp = session.get(url)
    data = json.loads(resp.content)[0]
    topic = Topic()
    topic.id = data.get('id')
    topic.title = filter_emoji(data.get('title'))
    topic.url = data.get('url')
    topic.content = filter_emoji(data.get('content'))
    topic.author = data.get('member').get('username')
    topic.node_title = data.get('node').get('title')
    topic.node_url = data.get('node').get('url')
    topic.time = format_time(data.get('created'))
    topic.replies = data.get('replies')
    return topic


def welcome():
    get_my_time()
    print termcolor.colored(u"Hello, {name}, 欢迎使用终端版 V2EX".format(name=globlevalue.username), "yellow")


def error():
    print termcolor.colored(u"输入错误, 可通过", "red") + termcolor.colored("help", "cyan") + termcolor.colored(u"查看", "red")


def help():
    info = u"\n" \
           "**********************************************************\n" \
           u"**\n" \
           u"**  latest:  最新话题\n" \
           u"**  hot:     最热话题\n" \
           u"**  #id:    指定id的话题\n" \
           u"**  me:      个人信息\n" \
           u"**  Num:     选中具体TL条目进行操作(Num 为话题的id)\n" \
           u"**  help:    帮助\n" \
           u"**  clear:   清屏\n" \
           u"**  quit:    退出系统\n" \
           u"**\n" \
           "**********************************************************\n"
    print termcolor.colored(info, "green")


main_ops = {
    "latest": latest,
    "hot": hot,
    "about": about,
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
    mode1 = re.compile(r"^\d+$")  # 匹配当前页的topic
    mode2 = re.compile(r"^#\d+$")  # 匹配任意id的topic
    welcome()
    while not op_stop:
        op = raw_input("Time Line$ ")
        if not re.match(mode1, op.strip()) and not re.match(mode2, op.strip()):
            main_ops.get(op, error)()
        elif re.match(mode1, op.strip()):
            opn = int(op)
            if opn < len(result_topics):
                topic = result_topics[opn]
                topic.operate(topic)
            else:
                print termcolor.colored(u"请输入正确的序号", "red")
        elif re.match(mode2, op.strip()):
            opn = int(op[1:])
            print opn
            topic = get_topic_by_id(opn)
            topic.operate(topic)


# if __name__ == '__main__':
#     work()
