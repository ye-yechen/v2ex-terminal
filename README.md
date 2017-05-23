# 终端版 V2EX

`python|terminal|crawler`

> python-terminal 采用 python2.7 编写，通过在命令行中输入命令执行 python 程序完成 v2ex 的常用功能：`登录、获取最新话题、获取最热话题、查看某个话题、查看话题的作者、话题答案分页显示、收藏话题、关注用户、屏蔽用户` 以及其他常用功能。利用了官方提供的 API，以及少量的爬虫。在命令行上， V2EX 的logo 是显示的字符，参考了网上的教程，将图片的灰度映射到字符上。

## 安装
**准备：安装好 python 2.7 环境**

- **克隆本项目**

```
 git clone https://github.com/creatorYC/v2ex-terminal.git
 cd v2ex-terminal
```

- **项目依赖**

```
 1. BeautifulSoup
 2. requests
 3. termcolor
 4. PIL
```

- **安装依赖**

```
pip install -r requirements.txt
```

- **开启终端版 V2EX**

>在 v2ex-terminal 文件下执行 `python v2ex.py`
初次使用时需要登录，之后保存到 cookies 就不需要每次都登录了。

- **体验命令行的快乐**

**在每个操作目录下都可以使用 `help` 命令查看此操作目录下可用的命令**

- **操作截图**

![登录](https://github.com/creatorYC/v2ex-terminal/blob/master/images/start.PNG)

![根操作目录](https://github.com/creatorYC/v2ex-terminal/blob/master/images/TL.PNG)

![选中话题index](https://github.com/creatorYC/v2ex-terminal/blob/master/images/TL-idx.PNG)

![话题](https://github.com/creatorYC/v2ex-terminal/blob/master/images/topic.PNG)

![答案](https://github.com/creatorYC/v2ex-terminal/blob/master/images/answer.PNG)

![作者](https://github.com/creatorYC/v2ex-terminal/blob/master/images/author.PNG)

---------------
### - contact me
- email: <yechoor@gmail.com>



