import requests
import constants
# import random
from utils.Utils import Utils
from lxml import etree


class Login(object):
    def __init__(self):
        self.login_url = 'https://accounts.douban.com/passport/login'
        self.post_url = 'https://accounts.douban.com/j/mobile/login/basic'
        self.logined_url = 'https://www.douban.com/people/104118815/'
        # self.session = requests.Session()
        self.headers1 = {
            # 'User-Agent': random.choice(constants.USER_AGENT),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Host': 'accounts.douban.com'
        }
        self.headers2 = {
            # 'User-Agent': random.choice(constants.USER_AGENT),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Referer': 'https://accounts.douban.com/passport/login',
            'Host': 'accounts.douban.com'
        }
        self.headers3 = {
            # 'User-Agent': random.choice(constants.USER_AGENT),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Host': 'www.douban.com'
        }
        self.index = 0
        self.failindex = []
        self.userNum = constants.UserNum

    def login(self, name, password):
        session = requests.Session()
        session.get(self.login_url, headers=self.headers1)
        post_data = {
            'name': name,
            'password': password,
            'remember': 'false'
        }
        response = session.post(self.post_url, data=post_data, headers=self.headers2)
        if response.status_code == 200:
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
            flag = self.detection(session)
            if flag == 0:
                print('获取session成功')
                return session
            else:
                print('获取session失败')
                return None
        else:
            print('获取session失败')
            return None

    # 检测session是否失效，返回0没失效，1失效
    def detection(self, session):
        r = session.get(self.logined_url, headers=self.headers3)
        Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            html = etree.HTML(r.text)
            name = html.xpath('//*[@id="profile"]/div/div[2]/div[1]/div/div/text()[1]')
            if not name:
                return 1
            else:
                return 0
        else:
            return 1

    def getSession(self):
        s = self.login(name=constants.UserInfo[self.index][0], password=constants.UserInfo[self.index][1])
        if not s:
            self.failindex.append(self.index)
            while True:
                self.index = (self.index + 1) % self.userNum
                if self.index not in self.failindex:
                    break
                if len(self.failindex) == self.userNum:
                    return None
            return self.getSession()

        else:
            self.index = (self.index + 1) % self.userNum
            return s
