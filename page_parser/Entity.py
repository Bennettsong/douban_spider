'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-04-22 08:42:47
@LastEditTime: 2020-04-24 10:37:18
'''
#!/usr/bin/env python3
# coding=utf-8
# author=XingLong Pan
# date=2016-12-05

# 你可以理解为scrapy框架中的item
movie = {
    # 电影id
    'douban_id': '',
    # 电影名字
    'title': '',
    # 导演
    'directors': '',
    # 编剧
    'scriptwriters': '',
    # 演员
    'actors': '',
    #
    'types': '',
    'release_region': '',
    'release_date': '',
    'alias': '',
    'languages': '',
    'duration': '',
    'score': 0.0,
    'description': '',
    'tags': '',
    'recommendMovie': '',
    'vote_num': '',
    'rating_per_stars5': '',
    'rating_per_stars4': '',
    'rating_per_stars3': '',
    'rating_per_stars2': '',
    'rating_per_stars1': '',
    'comment_num': ''

}

movieComment = {
    "douban_id": '',
    "comment_url": '',
    "star": '',
    "content": '',
    "comment_id": '',
    "people_id": '',
    "people": '',
    "useful_num": '',
    "time": '',
    "people_url": '',
}

personalInfo = {
    "pid": '',
    "name": '',
    "location": '',
    "introduction": '',
    "follow_num": '',  # 关注人的数量，但其中包含了一些已经注销了账号的，注销账号的不爬取
    "personUrl": '',
    "register_time": '',
    "follow_url": '',
    "do":'',
    "wish":'',
    "collect":'',
    "do_num":'',
    "wish_num":'',
    "collect_num":''
}

followPersonUrl = {
    "originalId": '',  # 源豆瓣人的名字
    "followId": '',  # 关注人的id（唯一）
    "followUrl": ''  # 关注人主页的url
}

wishMovie = {
    "douban_id": '',  # 源豆瓣人的名字
    "people_id": '',  # 关注人的id（唯一）
    "time": ''  # 关注人主页的url
}

