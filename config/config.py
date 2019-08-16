# -*- coding:utf-8 -*-
# author:臧海彬
# function:参数指定

# 要登录的账号
phone = "18717707251"
# phone = "18724730978"

# 存储的excel文件的文件夹名称
dirName = "result"

# 存储的excel文件的标题
title=["运单号","托寄物","邮寄时间"]

# 存储缓存文件的目录
cacheName = "cache"

# 设置最大连续重复次数，当运单号连续重复次数到达最大时将不再继续获取运单号
repeatMax = 10

# 如果debug为True则开启debug模式
debug = False
# 该模式下使用指定headers
debugHeaders = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "G_ESG_OWF_NGINX_CNSZ17=ESG_OWF_CNSZ17_NGINX_WEB_226_134; G_ESG_OWF_NGINX_CNSZ17=ESG_OWF_CNSZ17_NGINX_WEB_226_134; cookie-agree=true; ESG_OWF_NGINX_CNSZ17=ESG_OWF_CNSZ17_NGINX_WEB_226_131; route=efb92da3dac37f08b3c224a8321c437d; loginUser=18217293220; Hm_lvt_32464c62d48217432782c817b1ae58ce=1565681951,1565929486,1565966090,1565966195; Hm_lpvt_32464c62d48217432782c817b1ae58ce=1565966195; remember-me=NDBkMTdiYTI4NWU2NDY3YmIxNmVhZDMxMmZmNGU3M2Q6YzE4YzAyMjdmZjQ2NDdmMmFmYTQyOWEwZGI2NTAxNTA=; SESSION=7a7f0c381c4249c8ba3f20c8329b52d8",
    "Host": "www.sf-express.com",
    "Referer": "https://www.sf-express.com/cn/sc/dynamic_function/waybill/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}