'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-04-22 20:28:31
@LastEditTime: 2020-04-24 12:53:54
'''
import datetime
from utils.HelpTool import HelpTool
from storage.DbHelper import DbHelper
import constants
from lxml import etree
from utils.Utils import Utils
from page_parser import Entity
import argparse
# from utils.login import Login
from utils.GetCookies import GetCookies
import requests
import re
import sys


class CollectMovie:
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

    def parsePage(self, pid, collect_url, result, html):
        ids = 1
        collectComments = []
        star = 'allstar{}0 rating'
        for item in result:
            movieComment = Entity.movieComment.copy()
            movieComment['people_id'] = pid
            movieComment['comment_url'] = collect_url
            movieComment['comment_id'] = str(
                datetime.datetime.now().timestamp()).replace('.', '')+str(ids)
            ids += 1
            tmp = item.xpath(
                'div[@class="info"]/ul/li[@class="title"]/a/@href')
            if not tmp:
                continue
            else:
                tmp1 = tmp[0].strip().split('/')
                if tmp1[-1] == '':
                    douban_id = tmp1[-2]
                else:
                    douban_id = tmp1[-1]
                movieComment['douban_id'] = douban_id
            try:
                tmp = item.xpath(
                    'div[@class="info"]/ul/li[3]/span[1]/@class')[0].strip()
                tmp1 = re.search('(\d+)', tmp).group()
                movieComment['star'] = star.format(tmp1)
            except Exception:
                pass
            try:
                movieComment['time'] = item.xpath(
                    'div[@class="info"]/ul/li[3]/span[@class="date"]/text()')[0].strip()
            except Exception:
                pass
            try:
                movieComment['content'] = item.xpath(
                    'div[@class="info"]/ul/li[4]/span[@class="comment"]/text()')[0].strip()
            except Exception:
                pass
            try:
                tmp = item.xpath(
                    'div[@class="info"]/ul/li[4]/span[@class="p1"]/text()')[0].strip()
                movieComment['useful_num'] = re.search('(\d+)', tmp).group()
            except Exception:
                pass
            collectComments.append(movieComment)
        nextUrl = html.xpath(
            '//div[@class="paginator"]/span[@class="next"]/a[1]/@href')
        return collectComments, nextUrl

    def requestCollect(self, cookies, pid, pageIndex, base_url, nextUrl, retryTime):
        sys.stdout.flush()
        if nextUrl:
            collect_url = base_url + nextUrl
        else:
            collect_url = base_url
        r = requests.get(
            collect_url,
            headers=self.headers,
            cookies=cookies
        )
        r.encoding = 'utf-8'
        if r.status_code != 200:
            self.failId.append(pid)
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            return 2
        html = etree.HTML(r.text)
        result = html.xpath('//div[@class="item"]')
        if not result:
            if retryTime >= constants.MAX_RETRY_TIMES:
                return 2
            retryTime += 1
            print('cookie失效')
            end_time1 = datetime.datetime.now()
            print('失效时间间隔:{} 秒'.format(end_time1 - self.start_time))
            cookies = self.login.getCookie()
            if not cookies:
                print('获取session失败，退出程序！')
                return 1
            return self.requestCollect(cookies, pid, pageIndex, base_url, nextUrl, retryTime)
        else:
            collectComments, nextUrl = self.parsePage(
                pid, collect_url, result, html)
            # 豆瓣数据有效，写入数据库
            if collectComments:
                self.db_helper.insert_movieComments(collectComments)
                print('插入第{}页短评成功！'.format(pageIndex))
                pageIndex += 1
            if nextUrl:
                base_url = 'https://movie.douban.com'
                Utils.delay(constants.DELAY_MIN_SECOND,
                            constants.DELAY_MAX_SECOND)
                return self.requestCollect(cookies, pid, pageIndex,
                                    base_url, nextUrl[0], 1)
            return 0

    def end(self):
        # 存储爬取失败的电影id
        self.helptool.storeFailData(self.failPath, self.failId)
        # 释放资源
        self.db_helper.close_db()
        self.end_time = datetime.datetime.now()
        self.login.closeChrome()

    def spider(self):
        times = 0
        cookies = self.login.getCookie()
        with open(self.path, "r") as f:  # 设置文件对象
            for collectUrl in f:
                pid = ''
                if times >= constants.MAX_URL_TIMES:
                    times = 0
                    cookies = self.login.getCookie()
                if not cookies:
                    print('获取session失败，退出程序！')
                    print(collectUrl)
                    break
                tmp = collectUrl.split('/')
                if tmp[-1] == '':
                    pid = tmp[-3]
                else:
                    pid = tmp[-2]
                # 提示当前到达的id(log)
                print('当前爬取用户id {} 看过的电影！'.format(pid))
                sys.stdout.flush()
                flag = self.requestCollect(
                    cookies, pid, 1, collectUrl.strip(), None, 1)
                if flag == 1:
                    print(pid)
                    break
                times += 1
                Utils.delay(constants.DELAY_MIN_SECOND,
                            constants.DELAY_MAX_SECOND)
        self.end()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True)
    ap.add_argument("-f", "--failPath", required=True)
    args = vars(ap.parse_args())
    # 初始化一些全局变量
    collect_movie = CollectMovie(args['path'], args['failPath'])
    # path = 'data/collectUrl.txt'
    # failPath = 'data/fail.txt'
    # collect_movie = CollectMovie(path, failPath)
    print("开始抓取\n")
    print('Start time:{}'.format(collect_movie.start_time))
    collect_movie.spider()
    print('Runing time:{} seconds'.format(
        collect_movie.end_time - collect_movie.start_time))
    print(collect_movie.login.failindex)
