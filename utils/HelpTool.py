import constants
from utils.Utils import Utils
import requests

'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-04-14 11:11:26
@LastEditTime: 2020-04-24 16:46:00
'''


class HelpTool:
    def getCookie(self, name, password):
        s = requests.Session()
        cookie = None
        login_url = 'https://accounts.douban.com/j/mobile/login/basic'
        # 请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
            'Referer': 'https://accounts.douban.com/passport/login'
        }
        data = {
            'name': name,
            'password': password,
            'remember': 'false'
        }
        try:
            r = s.post(login_url, headers=headers, data=data)
            r.raise_for_status()
            cookie = requests.utils.dict_from_cookiejar(s.cookies)
        except:
            print('cookie获取失败')
        return cookie

    def getCookies1(self):
        index = 1
        cookieNum = 0
        cookieList = []
        for i in range(constants.UserNum):
            cookie = self.getCookie(
                constants.UserInfo[i][0],
                constants.UserInfo[i][1]
            )
            if 'dbcl2' in cookie.keys():
                print('获取第{}个cookie信息成功！'.format(index))
                cookieList.append(cookie)
                cookieNum += 1
            else:
                print('获取第{}个cookie信息失败！'.format(index))
            index += 1
            Utils.delay(constants.DELAY_MIN_SECOND, constants.DELAY_MAX_SECOND)
        return cookieList, cookieNum

    def getCookies(self):
        cookieNum = 1
        cookies = {
            'Cookie': '''_vwo_uuid_v2=DE925DEA282940A3862F45B76D16F6515|c7b25564ecc5f3a76fe0b215a7049dcd; douban-fav-remind=1; __gads=ID=5a7186a96a399d3b:T=1562035381:S=ALNI_MYVQZhDZuk4k65Gc6m43xHzlIHfiQ; trc_cookie_storage=taboola%2520global%253Auser-id%3Df89a91a1-0e2a-49da-ab4a-541fec676940-tuct30e3605; bid=GsH8Y166Fc0; ll="108258"; push_doumail_num=0; douban-profile-remind=1; ct=y; gr_user_id=3c3d78fa-91ff-4d8e-93d7-84ea0293d55d; push_noty_num=0; __utmc=30149280; __utma=30149280.701767670.1586593238.1587091479.1587093712.21; __utmz=30149280.1587093712.21.9.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; ap_v=0,6.0; dbcl2="161570896:xQFdJRMTjro"; ck=AQSi; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1587097839%2C%22https%3A%2F%2Fmovie.douban.com%2Fmine%22%5D; _pk_ses.100001.8cb4=*; __utmt=1; __utmv=30149280.16157; _pk_id.100001.8cb4=5365909cde383ce1.1547220225.49.1587097851.1587094281.; __utmb=30149280.10.10.1587093712'''}
        cookie1 = {
            'Cookie': '''_vwo_uuid_v2=DE925DEA282940A3862F45B76D16F6515|c7b25564ecc5f3a76fe0b215a7049dcd; douban-fav-remind=1; trc_cookie_storage=taboola%2520global%253Auser-id%3Df89a91a1-0e2a-49da-ab4a-541fec676940-tuct30e3605; __gads=ID=5a7186a96a399d3b:T=1562035381:S=ALNI_MYVQZhDZuk4k65Gc6m43xHzlIHfiQ; bid=GsH8Y166Fc0; ll="108258"; push_doumail_num=0; douban-profile-remind=1; ct=y; gr_user_id=3c3d78fa-91ff-4d8e-93d7-84ea0293d55d; push_noty_num=0; __utmc=30149280; __utmv=30149280.21507; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1587091477%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%22%5D; __utma=30149280.701767670.1586593238.1587086437.1587091479.20; __utmz=30149280.1587091479.20.8.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utma=223695111.1550008018.1547219243.1587088110.1587091479.59; __utmz=223695111.1587091479.59.44.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; _pk_id.100001.4cf6=9de2fde76a32ede0.1547219249.56.1587091789.1587089177.; dbcl2="160262599:I2sOvT86AU4"'''}
        cookie2 = {
            'Cookie': '''_vwo_uuid_v2=DE925DEA282940A3862F45B76D16F6515|c7b25564ecc5f3a76fe0b215a7049dcd; douban-fav-remind=1; __gads=ID=5a7186a96a399d3b:T=1562035381:S=ALNI_MYVQZhDZuk4k65Gc6m43xHzlIHfiQ; trc_cookie_storage=taboola%2520global%253Auser-id%3Df89a91a1-0e2a-49da-ab4a-541fec676940-tuct30e3605; bid=GsH8Y166Fc0; ll="108258"; push_doumail_num=0; douban-profile-remind=1; ct=y; gr_user_id=3c3d78fa-91ff-4d8e-93d7-84ea0293d55d; push_noty_num=0; __utmz=30149280.1587040594.18.7.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1587086437%2C%22https%3A%2F%2Fwww.baidu.com%2Fs%3Fie%3DUTF-8%26wd%3D%25E8%25B1%2586%25E7%2593%25A3%22%5D; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.701767670.1586593238.1587040594.1587086437.19; __utmc=30149280; dbcl2="198641190:O0bqoSGFSac"; ck=wsP3; __utmt=1; __utmv=30149280.19864; _pk_id.100001.8cb4=5365909cde383ce1.1547220225.47.1587087413.1587028838.; __utmb=30149280.12.10.1587086437'''}
        # cookieList = [cookie1,cookie2]
        cookieList = [cookies]
        return cookieList, cookieNum

    def storeFailData(self, path, data):
        if data:
            with open(path, 'w') as f:
                for tmp in data:
                    f.write(tmp)
                    f.write('\n')
                # f.writelines(data)
