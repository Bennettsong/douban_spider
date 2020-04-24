from storage.DbHelper import DbHelper
from utils.HelpTool import HelpTool
import argparse

'''
@Descripttion: 
@version: 
@Author: Bennett
@Date: 2020-04-24 08:19:03
@LastEditTime: 2020-04-24 08:40:48
'''
class storeData:
    def __init__(self):
        # 实例化爬虫类和数据库连接工具类
        self.db_helper = DbHelper()
        self.helptool = HelpTool()
    def readPersonUrl(self,path):
        data = self.db_helper.queryPersonUrl()
        # 释放资源
        self.db_helper.close_db()
        if data:
            self.helptool.storeFailData(path, data)
            print('存储成功！')
        else:
            print('存储失败')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p","--path",required=True)
    args = vars(ap.parse_args())
    store = storeData()
    print('开始存储数据')
    store.readPersonUrl(args['path'])
        