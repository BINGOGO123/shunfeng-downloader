## 程序功能
从顺丰快递官网批量下载指定手机号邮寄快递的[运单号、邮寄物、取件时间]三项信息并存于excel表中
每次运行都会取最新的订单号进行存储

## 程序文件说明
* main.py
  > 主函数
* spider/downloader.py
  > 爬虫函数，负责下载信息
* modules/Db.py
  > 数据库替代函数，此程序没有使用已有的数据库管理工具，而是通过简单的文件存储来实现
* modules/tools.py
  > 一些工具函数
* config/logger.py
  > 公用日志
* config/config
  > 常量和参数指定

## 生成文件说明
* result
  > 所有生成的excel文件都放在result目录下
  > 文件命名方式：手机号_日期_数字.xls
* logs
  > 日志目录
  > 文件命名方式：main.日期.log
* cache
  > 下载的验证码图片目录，主要用于之后自动识别验证码的测试
  > 文件命名方式：手机号_日志_数字.png
* db_file
  > 简易存储系统路径
  > 手机号_finished 存储已经下载过的运单号
  > 手机号_error 存储本次运行时尚未取得邮寄时间的正常快递（不是取消和待寄出状态），下次运行时会再次下载，并在成功运行完成之后删除。也可手动往其中添加运单号，空格作为分隔符即可。

## 运行方法
* python3.6 newMain.py
  > config/config.py中的debug控制是否为debug模式，如果debug为True则使用指定headers，否则根据手机号登录获取

## 备注
* 目前还没有实现自动识别验证码，所以还是手动输入验证码的方式