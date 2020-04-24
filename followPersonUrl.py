'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-04-22 20:28:31
@LastEditTime: 2020-04-24 16:16:21
'''
from utils.HelpTool import HelpTool
from storage.DbHelper import DbHelper
from utils.GetCookies import GetCookies
import datetime
import argparse
import constants
from utils.Utils import Utils
import requests
from lxml import etree
from page_parser import Entity
import re
import sys


class FollowPersonUrl:
    def __init__(self, path, failPath):
        self.path = path
        self.failPath = failPath
        self.failId = []
        self.helptool = HelpTool()
        # 实例化爬虫类和数据库连接工具类
        self.db_helper = DbHelper()
        self.login = GetCookies()
        # self.login = Login()
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'}

    def parsePage(self, result, personUrl):
        followPersonUrls = []
        for item in result:
            try:
                followPersonUrl = Entity.followPersonUrl.copy()
                followName = item.xpath('dd/a/text()')[0].strip()
                if followName == "[已注销]" or followName == "已注销":
                    continue
                tmp = personUrl.split('/')
                if tmp[-1] == '':
                    followPersonUrl['originalId'] = tmp[-3]
                else:
                    followPersonUrl['originalId'] = tmp[-2]
                url = item.xpath('dd/a/@href')[0].strip()
                followPersonUrl['followUrl'] = url
                tmp = url.split('/')
                if tmp[-1] == '':
                    followPersonUrl['followId'] = tmp[-2]
                else:
                    followPersonUrl['followId'] = tmp[-1]
                followPersonUrls.append(followPersonUrl)
            except Exception:
                pass
        return followPersonUrls

    def request_personfollowurl(self, cookies, personUrl, peopleIndex, retryTime):
        sys.stdout.flush()
        r = requests.get(
            personUrl,
            headers=self.headers,
            cookies=cookies
        )
        r.encoding = 'utf-8'
        if r.status_code != 200:
            self.failId.append(personUrl)
            print(
                '----------爬取第{}个用户,链接为{}的关注人链接,爬取失败----------'.format(str(peopleIndex), personUrl))
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            return 2
        # 提示当前到达的id(log)
        print('正在爬取第{}个用户,链接为{}的关注人链接信息'.format(str(peopleIndex), personUrl))
        html = etree.HTML(r.text)
        result = html.xpath('//dl[@class="obu"]')
        if not result:
            if retryTime >= constants.MAX_RETRY_TIMES:
                return 2
            retryTime += 1
            print('cookies失效')
            end_time1 = datetime.datetime.now()
            print('失效时间间隔:{} 秒'.format(end_time1 - self.start_time))
            cookies = self.login.getCookie()
            if not cookies:
                print('获取cookie失败，退出程序！')
                return 1
            return self.request_personfollowurl(cookies, personUrl, peopleIndex, retryTime)
        else:
            followPersonUrls = self.parsePage(result, personUrl)
            # 豆瓣数据有效，写入数据库
            if followPersonUrls:
                self.db_helper.insert_followPersonUrl(followPersonUrls)
                print('插入链接为{}用户关注人链接成功！'.format(personUrl))
            return 0

    def end(self):
        # 存储爬取失败的电影id
        self.helptool.storeFailData(self.failPath, self.failId)
        # 释放资源
        self.db_helper.close_db()
        self.end_time = datetime.datetime.now()
        self.login.closeChrome()

    def spider(self):
        peopleIndex = 1
        times = 0
        cookies = self.login.getCookie()
        with open(self.path, "r") as f:  # 设置文件对象
            for personUrl in f:
                if personUrl[-1] == '\n':
                    personUrl = personUrl[:-1]
                if times >= constants.MAX_URL_TIMES:
                    times = 0
                    cookies = self.login.getCookie()
                if not cookies:
                    print('获取cookie失败，退出程序！')
                    print(personUrl)
                    break
                sys.stdout.flush()
                flag = self.request_personfollowurl(
                    cookies, personUrl, peopleIndex, 1)
                if flag == 1:
                    print(personUrl)
                    break
                peopleIndex += 1
                times += 1
                Utils.delay(constants.DELAY_MIN_SECOND,
                            constants.DELAY_MAX_SECOND)
        self.end()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True)
    ap.add_argument("-f", "--failPath", required=True)
    args = vars(ap.parse_args())
    followUrl = FollowPersonUrl(args['path'], args['failPath'])
    # path = 'data/followPersonUrl.txt'
    # failPath = 'data/fail.txt'
    # followUrl = FollowPersonUrl(path, failPath)
    print("开始抓取\n")
    print('Start time:{}'.format(followUrl.start_time))
    followUrl.spider()
    print('Runing time:{} seconds'.format(
        followUrl.end_time - followUrl.start_time))
    print(followUrl.login.failindex)
