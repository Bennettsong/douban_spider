'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-03-29 21:07:05
@LastEditTime: 2020-04-23 10:53:13
'''

# 豆瓣电影的登录入口页面
DOUBAN_MOVIE_LOGIN_URL = 'https://accounts.douban.com/login'

# 搜索引擎（SEO爬虫）的请求头
USER_AGENT = [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'ia_archiver (+http://www.alexa.com/site/help/webmasters; crawler@alexa.com)'
]
UserInfo = [
    # 你的多个用户名和密码
    ('用户名1', 'password1'),
    ('用户名2', 'password2'),
    ('用户名3', 'password3')
]
# 上面用户名的个数
UserNum = 3
MAX_REQUEST_TIMES = 6

# 爬取用户信息
MAX_URL_TIMES = 20

MAX_RETRY_TIMES = 3

AGENT_SIZE = 7

# 延时设置
DELAY_MIN_SECOND = 4
DELAY_MAX_SECOND = 24

# 豆瓣电影的url前缀
URL_PREFIX = 'https://movie.douban.com/subject/'

"""
这里用到了阿布云代理动态版。使用影梭或者其他代理，甚至不用代理也可以
"""
# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
proxyUser = "HT1LX50X8R4P0I8D"
proxyPass = "1133BD889583B72A"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
