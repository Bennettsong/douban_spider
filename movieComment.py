'''
@Descripttion:
@version:
@Author: Bennett
@Date: 2020-04-10 21:14:27
@LastEditTime: 2020-04-24 12:55:51
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
import sys

class Comment:
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

    def parsePage(self, mid, comment_url, result, html):
        movieComments = []
        # 提取豆瓣数据
        for item in result:
            movieComment = Entity.movieComment.copy()
            movieComment['douban_id'] = mid
            movieComment['comment_url'] = comment_url
            try:
                # 短评的唯一id
                movieComment['comment_id'] = \
                    item.xpath(
                        'div[@class="comment"]/h3/span[@class="comment-vote"]/input/@value')[0].strip()
            except Exception:
                pass
            try:
                # 多少人评论有用
                movieComment['useful_num'] = \
                    item.xpath(
                        'div[@class="comment"]/h3/span[@class="comment-vote"]/span/text()')[0].strip()
            except Exception:
                pass
            try:
                # 评分
                movieComment['star'] = \
                    item.xpath(
                        'div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/@class')[0].strip()
            except Exception:
                pass
            try:
                # 评论时间
                movieComment['time'] = item.xpath(
                    'div[@class="comment"]/h3/span[@class="comment-info"]/span[@class="comment-time "]/@title')[
                    0]
            except Exception:
                pass
            try:
                # 评论内容
                movieComment['content'] = item.xpath(
                    'div[@class="comment"]/p/span/text()')[0]
            except Exception:
                pass
            try:
                # 评论者名字（唯一）
                movieComment['people'] = item.xpath(
                    'div[@class="avatar"]/a/@title')[0]
            except Exception:
                pass
            try:
                # 评论者页面
                url = item.xpath(
                    'div[@class="avatar"]/a/@href')[0].strip()
                tmp = url.split('/')
                if tmp[-1] == '':
                    movieComment['people_id'] = tmp[-2]
                else:
                    movieComment['people_id'] = tmp[-1]
                movieComment['people_url'] = item.xpath(
                    'div[@class="avatar"]/a/@href')[0]
            except Exception:
                pass
            movieComments.append(movieComment)
        nextUrl = html.xpath('//a[@class="next"]/@href')
        return movieComments, nextUrl

    def requestComment(self, cookies, mid, pageIndex, base_url, nextUrl,retryTime):
        # headers = {'User-Agent': random.choice(constants.USER_AGENT)}
        # 获取豆瓣页面(API)数据
        sys.stdout.flush()
        if nextUrl:
            comment_url = base_url + nextUrl
        else:
            comment_url = base_url
        r = requests.get(
            comment_url,
            headers=self.headers,
            cookies=cookies
        )
        r.encoding = 'utf-8'
        if r.status_code != 200:
            self.failId.append(mid)
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            return 2
        html = etree.HTML(r.text)
        result = html.xpath('//div[@class="comment-item"]')
        # 如果获取的数据为空，延时以减轻对目标服务器的压力,并跳过。
        if not result:
            if retryTime >= constants.MAX_RETRY_TIMES:
                return 2
            retryTime += 1
            print('session失效')
            end_time1 = datetime.datetime.now()
            print('失效时间间隔:{} 秒'.format(end_time1 - self.start_time))
            cookies = self.login.getCookie()
            if not cookies:
                print('获取session失败，退出程序！')
                return 1
            return self.requestComment(cookies, mid, pageIndex, base_url, nextUrl,retryTime)
        else:
            movieComments, nextUrl = self.parsePage(mid, comment_url, result, html)
            # 豆瓣数据有效，写入数据库
            if movieComments:
                self.db_helper.insert_movieComments(movieComments)
                print('插入第{}页短评成功！'.format(pageIndex))
                pageIndex += 1
            if nextUrl:
                Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
                return self.requestComment(cookies, mid, pageIndex, base_url, nextUrl[0],1)
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
        with open(self.path, "r") as f:  # 设置文件对象
            for mid in f:
                cookies = self.login.getCookie()
                if not cookies:
                    print('获取session失败，退出程序！')
                    print(mid)
                    break
                sys.stdout.flush()
                if mid[-1] == '\n':
                    mid = mid[:-1]
                base_url = constants.URL_PREFIX + mid + "/comments"
                # 提示当前到达的id(log)
                print('当前爬取电影id {} 的影评！'.format(mid))
                flag = self.requestComment(cookies, mid, 1, base_url, None,1)
                if flag == 1:
                    print(mid)
                    break
                Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
        self.end()


# 豆瓣限制，最多能爬取25页影评，也就是500条数据
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True)
    ap.add_argument("-f", "--failPath", required=True)
    # ap.add_argument("-i", "--index", required=True)
    args = vars(ap.parse_args())
    # 初始化一些全局变量
    movie_comment = Comment(args['path'], args['failPath'])
    print("开始抓取\n")
    print('Start time:{}'.format(movie_comment.start_time))
    movie_comment.spider()
    print('Runing time:{} seconds'.format(movie_comment.end_time - movie_comment.start_time))
    print(movie_comment.login.failindex)
