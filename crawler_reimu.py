#coding:utf-8
#author:9bie
#blog:http://9bie.org
#crawler from https://blog.reimu.net
#一个很暴力很暴力的实现
# import sqlite3
# import re
# 想了想暴力就暴力到底把，什么正则表达式，什么数据库，都不用了！
import requests
def writeindb(link):
    pass
def searchindb(link):
    pass
def findcode(source):
    flag1 = source.find("提取码：")
    if flag1 == -1:
        flag1 = source.find("提取码:")
        if flag1 == -1:
            print("没有找到提取码。")
            return ""
    flag2 = source.find("<",flag1)
    flag3 = source.find("\n",flag1)
    return source[flag1+4:flag2 if flag2< flag3 else flag3]
def getbdlink(source):
    flag1 = source.find("https://pan.baidu.com")
    if flag1 == -1:
        flag1 = source.find("http://pan.baidu.com")
        if flag1 == -1:
            print("获取网盘地址失败")
            return ""
    flag2 = source.find('"',flag1)
    flag3 =  source.find(" ",flag1)

    flag4 = source.find("<",flag1)
    if flag2>flag3:
        flag5=flag3
    else:
        flag5=flag2
    return source[flag1:flag4 if flag4<flag5 else flag5]

if __name__ == '__main__':
    a = requests.get("https://blog.reimu.net/archives/32892")
    print(getbdlink(a.text))
    print(findcode(a.text))
