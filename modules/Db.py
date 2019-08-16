# -*- coding:utf-8 -*-
# author:臧海彬
# function:简易文件存储系统代替数据库

import os
from config.logger import logger

class Db:
    __dirName = "db_file"
    def __init__(self,fileName,encoding="utf8"):
        logger.info("初始化数据库类，文件名：{}，编码：{}".format(fileName,encoding))
        if not os.path.exists(Db.__dirName):
            logger.info("{} 不存在，新建".format(Db.__dirName))
            os.mkdir(Db.__dirName)
        self.fileName = Db.__dirName + "/" + fileName
        self.encoding = encoding
        if not os.path.exists(self.fileName):
            logger.info("文件不存在，新建")
            f = open(self.fileName,"w",encoding=self.encoding)
            f.close()
            self.itemList = []
        else:
            logger.info("文件已经存在")
            f = open(self.fileName,"r",encoding=self.encoding)
            block=10000
            result = ""
            while True:
                line = f.read(block)
                if line == "":
                    break
                result+=line
            f.close()
            result = result.strip()
            if result != "":
                self.itemList = result.split(" ")
            else:
                self.itemList = []
        logger.info("数据库初始化完成")
    
    # 删除元素
    def removeItem(self,item):
        try:
            self.itemList.remove(item)
            logger.info("[成功] 删除 {} 中的 {}".format(self.fileName,item))
            return True
        except ValueError:
            logger.info("[失败] 删除 {} 中的 {}".format(self.fileName,item))
            return False
    
    # 添加元素
    def addItem(self,item):
        try:
            self.itemList.index(item)
            logger.info("[失败] 添加 {} 中的 {}".format(self.fileName,item))
            return False
        except ValueError:
            # 插入到最后面
            self.itemList.append(item)
            # self.itemList.insert(0,item)
            logger.info("[成功] 添加 {} 中的 {}".format(self.fileName,item))
            return True
    
    # 保存到硬盘
    def save(self):
        f = open(self.fileName,"w",encoding = self.encoding)
        for item in self.itemList:
            f.write(item+" ")
        f.close()
        logger.info("{} {} 将内容存到硬盘中".format(self.fileName,self.encoding))

    # 清空
    def clear(self):
        self.itemList.clear()
        return True
    
