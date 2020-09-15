# coding=UTF-8
import os
import configparser
import json


# 設定檔存取元件
class ConfigUtil():

    __filePath = 'config.ini'
    IssueURL = None
    Account = None
    Password = None

    def __init__(self):
        # 判斷設定檔是否存在，不存在則給予預設參數值
        if os.path.exists(self.__filePath) is False:
            self.__saveConfig(self.__initConfig())
        # 讀取設定檔
        config = configparser.ConfigParser()
        config.read(self.__filePath, encoding="UTF-8")
        # 讀取參數設定值
        self.IssueURL = json.loads(config["SystemConfig"]["issueURL"])
        self.Account = json.loads(config["SystemConfig"]["account"])
        self.Password = json.loads(config["SystemConfig"]["password"])

    # 提供外部呼叫設定檔存檔
    def save(self):
        self.__saveConfig({
            "issueURL": self.IssueURL,
            "account": self.Account,
            "password": self.Password,
        })

    # 設定檔存檔
    def __saveConfig(self, para):
        # 讀取設定參數
        issueURL = para["issueURL"]
        account = para["account"]
        password = para["password"]
        # 產生設定檔物件
        config = configparser.ConfigParser()
        # 產生系統設定參數
        config['SystemConfig'] = {
            'issueURL': json.dumps(issueURL, ensure_ascii=False),
            'account': json.dumps(account, ensure_ascii=False),
            'password': json.dumps(password, ensure_ascii=False),
        }
        # 寫入設定檔
        with open(self.__filePath, 'w', encoding='UTF8') as configFile:
            config.write(configFile)

    # 初始化設定檔
    def __initConfig(self):
        return {
            "issueURL": "http://gitea.dsic.com.tw/api/v1/repos/LAND-JOPV2/DevelopmentFiles/issues",
            "account": "Bob",
            "password": "*****",
        }
