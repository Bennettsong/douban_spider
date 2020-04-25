from selenium import webdriver
import time
import requests
from lxml import etree
from utils.Utils import Utils
import constants
from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class GetCookies:
    def __init__(self):
        self.chrome_options = Options()
        # 设置chrome浏览器无界面模式
        self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        # self.driver = webdriver.Chrome()
        self.logined_url = 'https://www.douban.com/people/104118815/'
        self.headers = {
            # 'User-Agent': random.choice(constants.USER_AGENT),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Host': 'www.douban.com'
        }
        self.index = 0
        self.failindex = []
        self.userNum = constants.UserNum
        # 标识是否第一次访问，如果不是，则需要退出登录
        self.flag = 0

    def restart(self):
        print('----------重启webDriver!----------')
        self.driver.quit()
        time.sleep(random.randrange(3,6))
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
        self.flag = 0

    def login(self, name, password):
        maxTryTimes = 6
        times = 0
        while True:
            try:
                if self.flag:
                    wait1 = WebDriverWait(self.driver,10)
                    inputs = wait1.until(EC.presence_of_element_located((By.CLASS_NAME,'nav-user-account')))
                    self.driver.find_element_by_class_name(
                        'nav-user-account').click()
                    self.driver.find_element_by_xpath(
                        '//*[@id="db-global-nav"]/div/div[1]/ul/li[2]/div/table/tbody/tr[5]/td/a').click()
                    
                else:
                    self.driver.get('https://www.douban.com/')
                    self.flag = 1
                times = 0
                time.sleep(random.randrange(3,6))
                break
            except Exception:
                print('---------Time Out,Retrying!----------')
                self.restart()
                times += 1
                if times >= maxTryTimes:
                    return None
        while True:
            try:
                wait = WebDriverWait(self.driver,10)
                inputs = wait.until(EC.presence_of_element_located((By.TAG_NAME,'iframe')))
                iframe = self.driver.find_element_by_tag_name("iframe")
                self.driver.switch_to_frame(iframe)
                self.driver.find_element_by_class_name('account-tab-account').click()
                self.driver.find_element_by_id('username').send_keys(name)
                self.driver.find_element_by_id('password').send_keys(password)
                self.driver.find_element_by_class_name('btn-account').click()
                break
            except Exception:
                print('----------无法定位到用户名输入框---------')
                times += 1
                if times >= maxTryTimes:
                    return None
                time.sleep(random.randrange(3,6))
                # return self.login(name, password)
        time.sleep(random.randrange(5,8))
        try:
            cookies_list = self.driver.get_cookies()
            cookies = {i["name"]: i["value"] for i in cookies_list}
        except Exception:
            print('-----------登录成功，但是获取Cookie失败----------')
            return None
        flag = self.detection(cookies)
        if flag == 0:
            print('获取session成功')
            return cookies
        else:
            print('获取session失败')
            return None

    # 检测session是否失效，返回0没失效，1失效
    def detection(self, cookies):
        r = requests.get(self.logined_url,
                         headers=self.headers, cookies=cookies)
        Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            html = etree.HTML(r.text)
            name = html.xpath(
                '//*[@id="profile"]/div/div[2]/div[1]/div/div/text()[1]')
            if not name:
                return 1
            else:
                print(name)
                return 0
        else:
            return 1

    def getCookie(self):
        cookies = self.login(
            name=constants.UserInfo[self.index][0], password=constants.UserInfo[self.index][1])
        if not cookies:
            self.failindex.append(self.index)
            while True:
                self.index = (self.index + 1) % self.userNum
                if self.index not in self.failindex:
                    break
                if len(self.failindex) == self.userNum:
                    return None
            return self.getCookie()

        else:
            self.index = (self.index + 1) % self.userNum
            return cookies

    def closeChrome(self):
        # 关闭chreomedriver进程
        self.driver.quit()
