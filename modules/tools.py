# -*- coding:utf-8 -*-
# author:臧海彬
# function:一些工具函数

import os
import sys

# 判断name是否存在，如果存在则获取一个不存在的name名称
def getName(name):
    name = name.split(".")
    if len(name) == 1:
        firstName = name[0]
        lastName = ""
    elif len(name) > 1:
        lastName = "."+name[-1]
        firstName = ".".join(name[:-1])
    else:
        return False

    # 寻找一个不存在的文件名称
    order = ""
    while True:
        if os.path.exists(firstName+order+lastName):
            if order == "":
                order = "_1"
            else:
                order = "_" + str(int(order[1:]) + 1)
        else:
            break
    return firstName + order + lastName

# 暂停在命令行界面等待回车然后退出
def stopExit():
    input("输入回车退出...")
    sys.exit()
