'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-04-22 08:51:26
@LastEditTime: 2020-04-24 15:27:21
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


class personInfo:
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

    def parsePage(self, personUrl, html, name):
        personalInfo = Entity.personalInfo.copy()
        tmp = personUrl.split('/')
        if tmp[-1] == '':
            personalInfo['pid'] = tmp[-2]
        else:
            personalInfo['pid'] = tmp[-1]
        personalInfo['name'] = name[0].strip()
        personalInfo['personUrl'] = personUrl
        try:
            personalInfo['register_time'] = html.xpath('//*[@id="profile"]/div/div[2]/div[1]/div/div/text()')[
                1].strip()[:-2]
        except Exception:
            pass
        try:
            personalInfo['location'] = html.xpath(
                '//*[@id="profile"]/div/div[2]/div[1]/div/a/text()')[0].strip()
        except Exception:
            pass
        try:
            personalInfo['introduction'] = ''.join(
                html.xpath('//*[@id="intro_display"]/text()'))
        except Exception:
            pass
        try:
            temp = html.xpath(
                '//*[@id="friend"]/h2/span/a/text()')[0].strip()
            personalInfo['follow_num'] = re.search('(\d+)', temp).group()
        except Exception:
            pass
        try:
            personalInfo['follow_url'] = html.xpath(
                '//*[@id="friend"]/h2/span/a/@href')[0]
        except Exception:
            pass
        try:
            temps = html.xpath('//*[@id="movie"]/h2/span/a')
            #['https://movie.douban.com/people/153843683/do', 'https://movie.douban.com/people/153843683/wish', 'https://movie.douban.com/people/153843683/collect']
            for temp in temps:
                result = temp.xpath('@href')[0]
                num = temp.xpath('text()')[0]
                num1 = re.search('(\d+)', num).group()
                tmp = result.split('/')
                url = ''
                if tmp[-1] == '':
                    url = tmp[-2]
                else:
                    url = tmp[-1]
                if url == 'do':
                    personalInfo['do'] = result
                    personalInfo['do_num'] = num1
                elif url == 'wish':
                    personalInfo['wish'] = result
                    personalInfo['wish_num'] = num1
                elif url == 'collect':
                    personalInfo['collect'] = result
                    personalInfo['collect_num'] = num1
        except Exception:
            pass
        return personalInfo

    def requestInfo(self, cookies, personUrl, peopleIndex, retryTime):
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
                '----------爬取第{}个用户,链接为{},爬取失败----------'.format(str(peopleIndex), personUrl))
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            return 2
        # 提示当前到达的id(log)
        print('正在爬取第{}个用户,链接为{}的个人信息'.format(str(peopleIndex), personUrl))
        html = etree.HTML(r.text)
        name = html.xpath(
            '//*[@id="profile"]/div/div[2]/div[1]/div/div/text()[1]')
        if not name:
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
            return self.requestInfo(cookies, personUrl, peopleIndex, retryTime)
        else:
            personalInfo = self.parsePage(personUrl, html, name)
            # 豆瓣数据有效，写入数据库
            if personalInfo:
                self.db_helper.insert_personalInfo(personalInfo)
                print('插入链接为{}用户信息成功！'.format(personUrl))
            return 0

    def end(self):
        # 存储爬取失败的电影id
        self.helptool.storeFailData(self.failPath, self.failId)
        # 释放资源
        self.db_helper.close_db()
        self.end_time = datetime.datetime.now()
        self.login.closeChrome()
    # 每次爬取一个电影的影评用一个新的用户

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
                flag = self.requestInfo(cookies, personUrl, peopleIndex, 1)
                if flag == 1:
                    print(personUrl)
                    break
                peopleIndex += 1
                times += 1
                Utils.delay(constants.DELAY_MIN_SECOND,
                            constants.DELAY_MAX_SECOND)
        self.end()


# 豆瓣限制，最多能爬取25页影评，也就是500条数据
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True)
    ap.add_argument("-f", "--failPath", required=True)
    args = vars(ap.parse_args())
    # 初始化一些全局变量
    infos = personInfo(args['path'], args['failPath'])
    # path = 'data/personUrl.txt'
    # failPath = 'data/fail.txt'
    # infos = personInfo(path, failPath)
    print("开始抓取\n")
    print('Start time:{}'.format(infos.start_time))
    infos.spider()
    print('Runing time:{} seconds'.format(infos.end_time - infos.start_time))
    print(infos.login.failindex)
