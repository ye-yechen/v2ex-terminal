# -*- coding:utf-8 -*-
import termcolor
from conf import session, headers, clear
import re

offset = 0
tmp = 0
limit = 5
current_answer_list = []


class Answer:

    def __init__(self):
        pass

    def error(self):
        print termcolor.colored(u"输入错误, 可通过", "red") + termcolor.colored("help", "cyan") + termcolor.colored(u"查看","red")

    def ignore(self, answer):
        pass

    def thanks(self, answer):
        pass

    def help(self):
        info = "\n" \
               "*************************************************************************\n" \
               "**\n" \
               "**  Num:        查看答案(Num 为当前页的id)\n" \
               "**  next:       下一页\n" \
               "**  pre:        上一页\n" \
               "**  hide:       隐藏答案\n" \
               "**  thx:        感谢答案作者\n" \
               "**  pwd:        查看当前条目内容\n" \
               "**  clear:      清屏\n" \
               "**  break:      返回上级操作目录\n" \
               "**\n" \
               "************************************************************************\n"
        print termcolor.colored(info, "green")

    def show_answers(self, answer_list):
        global offset, limit, current_answer_list
        current_answer_list = answer_list[offset:offset+limit]
        offset = offset + limit
        index = 0
        if len(answer_list) > 0:
            for answer in answer_list:
                id = termcolor.colored(str(index), 'red')
                time = termcolor.colored(answer.time, 'white')
                content = termcolor.colored(answer.content, 'blue') + \
                        termcolor.colored("(" + answer.author + ")", 'green')
                info = '\n'.join([id + '\t\t' + time, content]) + '\n'
                index += 1
                print info
        else:
            print termcolor.colored("还没有回答", 'red')

    def operate(self, answer_list):
        self.show_answers(answer_list)
        mode = re.compile(r"^\d+$")
        while True:
            op = raw_input("Answer List$ ")
            if re.match(mode, op.strip()):
                pass
            else:
                if op == "":
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

