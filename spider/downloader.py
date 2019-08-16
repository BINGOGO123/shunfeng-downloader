# -*- coding:utf-8 -*-
# author:臧海彬
# function:负责从顺丰快递下载指定参数信息并入库和生成文件

from config.logger import logger
import requests
import time
import json
import sys
from modules.Db import Db
from config.config import repeatMax
from config.config import cacheName
from config.config import debug
from config.config import debugHeaders
import datetime
from modules.tools import getName
import os
from modules.tools import stopExit
from PIL import Image

class Downloader:
    # 指定downloader类常量
    __headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    }
    __home = "https://www.sf-express.com/cn/sc/index.html"
    __login = "https://www.sf-express.com/sf-service-core-web/service/user/sms/login?rememberMe=true&lang=sc&region=cn&translate="
    def __code(self):
        return "https://www.sf-express.com/sf-service-owf-web/service/captcha/sms?force=true&time={}".format(int(time.time()*1000))
    def __ensureCode(self,answer):
        return "https://www.sf-express.com/sf-service-owf-web/service/sms/user/{}/notification?app=sms&answer={}&area=&lang=sc&region=cn&translate=".format(self.phone,answer)
    
    # 进行顺丰快递手机号的登录过程和其他的初始化内容
    def __init__(self,phone):
        logger.info("初始化Downloader对象，phone = {}".format(phone))
        self.finishedDb = Db(phone+"_finished")
        self.errorDb = Db(phone+"_error")
        self.s = requests.session()
        self.phone = phone
        self.s.headers.update(self.__headers)
        self.isLogin = False
        self.login()
        logger.info("初始化Downloader对象结束")
    
    # 进行顺丰快递的登录
    def login(self):
        if debug:
            logger.info("Downloader登录[debug模式使用指定headers]")
            self.s.headers.update(debugHeaders)
            self.isLogin = True
            logger.info("Downloader登录完成[debug模式使用指定headers]")
            return
        logger.info("Downloader登录")
        # 首先需要验证码认证
        while True:
            logger.info("获取验证码")
            # 获取验证码
            try:
                r = self.s.get(self.__code())
                r.raise_for_status()
            except:
                logger.exception("获取验证码出现错误")
                return
            # 保存验证码
            if not os.path.exists(cacheName):
                logger.info("{} 目录不存在，创建之".format(cacheName))
                os.mkdir(cacheName)
            verificationCodeName = getName(cacheName + "/" + self.phone + "." + str(datetime.date.today()) + ".png")
            f = open(verificationCodeName,"wb")
            f.write(r.content)
            f.close()
            logger.info("验证码保存在 {} 中".format(verificationCodeName))
            im = Image.open(verificationCodeName)
            im.show()

            # 目前是人工识别验证码
            answer = input("请输入验证码[{}]:".format(verificationCodeName))
            logger.info("输入的验证码：{}".format(answer))

            logger.info("开始向服务器发送验证码：{}".format(answer))
            try:
                r = self.s.post(self.__ensureCode(answer))
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                logger.warning("输入验证码 {} 错误，重新获取验证码".format(answer))
                continue
            except:
                logger.exception("向服务器发送验证码出现错误")
                return
            if json.loads(r.content.decode("utf8"))["code"] == 0:
                logger.info("验证码认证成功")
                break
            else:
                logger.error("验证码认证失败：{}".format(r.content.decode("utf8")))
                return
        
        code = input("请输入您手机收到的验证码：")
        logger.info("输入的验证码为：{}".format(code))
        self.s.headers.update({
            "SMS-Verification-App": "user",
            "SMS-Verification-Code": code,
            "SMS-Verification-Mobile": self.phone,
            "SMS-Verification-Mobile-Area":"" 
        })
        try:
            r = self.s.post("https://www.sf-express.com/sf-service-core-web/service/user/sms/login?rememberMe=true&lang=sc&region=cn&translate=")
            r.raise_for_status()
        except:
            logger.exception("输入验证码登录出现错误：{}".format(r.content.decode("utf8")))
            return
        if json.loads(r.content.decode("utf8"))["code"] == 111:
            logger.warning("验证码错误，重新登录")
            self.login()
            return
        elif json.loads(r.content.decode("utf8"))["code"] != 0:
            logger.error("登录失败：{}".format(r.content.decode("utf8")))
            return

        # 表示登录成功
        self.isLogin = True
        logger.info("登录成功")

        # 打印一下cookies
        for i in self.s.cookies:
            logger.debug("{} {} {}".format(i.domain,i.name,i.value))

    def download(self):
        # 批量下载所有运单号
        pageNo = 1
        stopNo = 1
        count = 0
        codeList = []
        logger.info("开始获取运单号")
        # 表示是否跳出循环
        out = False
        # 当前运单号重复次数
        repeatCount = 0
        while True:
            # 如果大于运单号最大页数则退出
            if pageNo > stopNo:
                break
            url = "https://www.sf-express.com/sf-service-core-web/service/waybills/list/send?lang=sc&region=cn&translate=&pageNo={}&pageRows=10".format(pageNo)
            response = self.s.get(url)
            result = json.loads(response.text)
            if result["code"] == 500:
                logger.error("无法查询到运单号信息 {}".format(result))
                stopExit()
            elif result["code"] != 0:
                if debug:
                    logger.error("登录已经过期[debug模式],退出 {}".format(result))
                    stopExit()
                logger.error("登录已经过期，需要重新登录 {}".format(result))
                self.isLogin = False
                self.login()
                # 登录失败直接退出
                if not self.isLogin:
                    logger.error("登录失败，退出")
                    stopExit()
                # 登录成功再次下载该页信息
                continue
            stopNo = int(result["result"]["totalPage"])
            for item in result["result"]["content"]:
                # 运单已经取消
                if item["waybillno"] == None or item["waybillno"] == "":
                    logger.info("{} 运单取消".format(count))
                    count+=1
                    continue
                if not self.finishedDb.addItem(str(item["waybillno"])):
                    repeatCount += 1
                    logger.info("{} 已经下载过的订单信息:{} repeatCount = {}".format(count,str(item["waybillno"]),repeatCount))
                    if repeatCount == repeatMax:
                        logger.info("{} {} 达到最大重复次数 {} 不再继续获取订单号".format(count,str(item["waybillno"]),repeatMax))
                        count += 1
                        out = True
                        break
                else:
                    logger.info("{} {}".format(count,item["waybillno"]))
                    repeatCount = 0
                    codeList.append(item["waybillno"])
                count+=1
            if out:
                break
            pageNo += 1
        logger.info("运单号获取完毕，已处理[{}]个运单号，共计得到[{}]个有效运单号".format(count,len(codeList)))

        logger.info("此次运行强制下载的{}个运单号信息：{}".format(len(self.errorDb.itemList),self.errorDb.itemList))
        codeList += self.errorDb.itemList
        self.errorDb.clear()

        logger.info("开始下载每个运单号的详细信息")
        # 用来放置每个订单号下载的三项信息
        itemResult = []
        # 根据每个运单号下载相应信息
        for i in range(len(codeList)):
            code = codeList[i]
            # 出现了空的运单号，如果出现这个问题那么很奇怪，因为前面应该已经不会将空运单号加入进来
            if code == None or code == "":
                itemResult.append(["奇怪的空运单号","",""])
                logger.warning("{} 当前获取运单号为空！".format(i))
                continue
            logger.info("{} 当前处理运单号:{}".format(i,code))
            # 存入表格的信息
            final = [code]
            # 托寄物信息的获取
            url = "https://www.sf-express.com/sf-service-owf-web/service/memberBills/{}/getBillEleStub?lang=sc&region=cn&translate=&securityExpress=false".format(code)
            response = self.s.get(url)
            result = json.loads(response.text)
            if result["code"] != 0:
                final.append("")
            else:
                try:
                    final.append(result["result"]["innerWaybillConsigns"])
                except:
                    logger.exception("获取托寄物信息时出现错误:{}".format(result))
                    final.append("")
            logger.info("托寄物:"+final[1])
            # 托寄时间的获取
            url = "https://www.sf-express.com/sf-service-core-web/service/bills/{}/route?lang=sc&region=cn&translate=".format(code)
            response = self.s.get(url)
            result = json.loads(response.text)
            if result["code"] != 0:
                final.append("")
            else:
                try:
                    final.append(result["result"]["routes"][0]["scanDateTime"])
                except:
                    logger.exception("获取托寄时间信息出现错误:{}".format(result))
                    final.append("")
            logger.info("托寄时间:" + final[2])
            itemResult.append(final)
        logger.info("每个运单号的信息下载完成")
        return itemResult
    
    # 保存数据库到硬盘
    def saveDb(self):
        self.finishedDb.save()
        self.errorDb.save()