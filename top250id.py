'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-04-13 17:16:26
@LastEditTime: 2020-04-24 09:23:57
'''
import datetime
from utils.HelpTool import HelpTool
import requests
import constants
import random
from lxml import etree
from utils.Utils import Utils


def run():
    helptool = HelpTool()
    cookieList = helptool.getCookie()
    base_url = 'https://movie.douban.com/top250'
    headers = {'User-Agent': random.choice(constants.USER_AGENT)}
    doubanIds = []
    savePath = 'data/top250id.txt'
    # 指明当前用第几个cookie
    index = 0
    # 获取豆瓣TOP250id数据
    r = requests.get(
        base_url,
        headers=headers,
        cookies=cookieList[index]
    )
    r.encoding = 'utf-8'
    while True:
        html = etree.HTML(r.text)
        result = html.xpath('//div[@class="item"]')
        # 如果获取的数据为空，延时以减轻对目标服务器的压力,并跳过。
        if not result:
            continue
        for item in result:
            doubanid = item.xpath('div/div[@class="hd"]/a/@href')
            if doubanid:
                tmp = doubanid[0].strip().split('/')
                if tmp[-1] == '':
                    value = tmp[-2]
                else:
                    value = tmp[-1]
                doubanIds.append(value)
                print('----------电影id ' + value + ':爬取成功' + '----------')
        nextUrl = html.xpath('//span[@class="next"]/a/@href')
        if not nextUrl:
            break
        url = base_url+nextUrl[0]
        index += 1
        if index >= constants.UserNum:
            index = 0
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
        r = requests.get(
            url,
            headers=headers,
            cookies=cookieList[index]
        )
        r.encoding = 'utf-8'
    if doubanIds:
        helptool.storeFailData(savePath, doubanIds)


if __name__ == '__main__':
    print("开始抓取\n")
    start_time = datetime.datetime.now()
    print('Start time:{}'.format(start_time))
    run()
    end_time = datetime.datetime.now()
    print('Runing time:{} seconds'.format(end_time - start_time))
