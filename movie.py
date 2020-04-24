'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-04-24 15:36:44
@LastEditTime: 2020-04-24 16:18:55
'''
from utils.HelpTool import HelpTool
from storage.DbHelper import DbHelper
from utils.GetCookies import GetCookies
import datetime
import argparse
import constants
from utils.Utils import Utils
import requests
from page_parser import Entity
from page_parser.MovieParser import MovieParser
import sys
class Movie:
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
        # 实例化爬虫类和数据库连接工具类
        self.movie_parser = MovieParser()
    def request_movie(self, cookies, mid, movieIndex, retryTime):
        sys.stdout.flush()
        r = requests.get(
            constants.URL_PREFIX + mid,
            headers=self.headers,
            cookies=cookies
        )
        r.encoding = 'utf-8'
        if r.status_code != 200:
            self.failId.append(mid)
            print(
                '----------爬取第{}部电影信息,id为{},爬取失败----------'.format(str(movieIndex), mid))
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            return 2
        print('正在爬取第{}部电影信息,id为{}'.format(str(movieIndex), mid))
        movie = self.movie_parser.extract_movie_info(r)
        if not movie:
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
            return self.request_movie(cookies, mid, movieIndex, retryTime)
        else:
            # 豆瓣数据有效，写入数据库
            movie['douban_id'] = mid
            self.db_helper.insert_movie(movie)
            print('----------电影id ' + mid + ':爬取成功' + '----------')
            return 0
    def end(self):
        # 存储爬取失败的电影id
        self.helptool.storeFailData(self.failPath, self.failId)
        # 释放资源
        self.db_helper.close_db()
        self.end_time = datetime.datetime.now()
        self.login.closeChrome()
    def spider(self):
        movieIndex = 1
        times = 0
        cookies = self.login.getCookie()
        with open(self.path, "r") as f:  # 设置文件对象
            for mid in f:
                if mid[-1] == '\n':
                    mid = mid[:-1]
                if times >= constants.MAX_URL_TIMES:
                    times = 0
                    cookies = self.login.getCookie()
                if not cookies:
                    print('获取cookie失败，退出程序！')
                    print(mid)
                    break
                sys.stdout.flush()
                flag = self.request_movie(cookies, mid, movieIndex, 1)
                if flag == 1:
                    print(mid)
                    break
                movieIndex += 1
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
    movieInfo = Movie(args['path'], args['failPath'])
    # path = 'data/personUrl.txt'
    # failPath = 'data/fail.txt'
    # infos = personInfo(path, failPath)
    print("开始抓取\n")
    print('Start time:{}'.format(movieInfo.start_time))
    movieInfo.spider()
    print('Runing time:{} seconds'.format(movieInfo.end_time - movieInfo.start_time))
    print(movieInfo.login.failindex)
    