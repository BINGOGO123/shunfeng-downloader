# -*- coding:utf-8 -*-
# author:臧海彬
# function:主函数

import bs4
from bs4 import BeautifulSoup
import requests
import xlwt
import sys
import os
import logging
import datetime
from config.logger import logger
from config.config import phone
from config.config import dirName
from config.config import title
from config.config import debug
from spider.downloader import Downloader
from modules.tools import getName
from modules.tools import stopExit

# 是否是debug模式
if debug:
    phone = "debug"
# 获取结果文件的名称
def getResultName():
    if len(sys.argv) > 1:
        resultName = sys.argv[1]
    else:
        resultName = phone + "_" + str(datetime.date.today()) + "_订单号信息"
        
    if not os.path.exists(dirName):
        os.mkdir(dirName)
    return getName(dirName + "/" + resultName+".xls")
    
# 初始化日志对象
def initialLogger():
    logger.setLevel(logging.DEBUG)
    # 如果不存在logs文件夹则创建
    if not os.path.exists("logs"):
        os.mkdir("logs")
    handler1 = logging.FileHandler(filename="logs/main."+str(datetime.date.today()) +".log",mode="a",encoding="utf8")
    handler2 = logging.StreamHandler()
    handler1.setLevel(logging.DEBUG)
    handler2.setLevel(logging.INFO)
    formatter1 = logging.Formatter(fmt="%(asctime)s [%(levelname)s] [%(lineno)d] >> %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
    formatter2 = logging.Formatter(fmt = "[%(levelname)s] >> %(message)s")
    handler1.setFormatter(formatter1)
    handler2.setFormatter(formatter2)
    logger.addHandler(handler1)
    logger.addHandler(handler2)

# 将信息保存到resultName中
def save(result,resultName,sheetName):
    r = xlwt.Workbook(encoding="utf8")
    # 创建表格以及题头信息
    sheet = r.add_sheet(sheetName)
    for row in range(len(result)):
        for column in range(len(result[row])):
            sheet.write(row,column,result[row][column]) 
    r.save(resultName)
    
if __name__ == "__main__":
    logger.info("顺丰快递订单下载启动")
    # 更改路径
    os.chdir(sys.path[0])
    # 初始化日志对象
    initialLogger()
    downloader = Downloader(phone)
    if not downloader.isLogin:
        logger.info("登录失败，退出")
        stopExit()
    # 获取下载内容
    result = downloader.download()
    # 保存文件到resultName中
    resultName = getResultName()
    result = [title] + result
    save(result,resultName,"Sheet1")
    # 保存已经下载的订单号到硬盘
    downloader.saveDb()
    logger.info("下载信息保存在 [{}] 中".format(resultName))
    logger.info("顺丰快递订单下载完毕")
    input("输入回车关闭...")
    