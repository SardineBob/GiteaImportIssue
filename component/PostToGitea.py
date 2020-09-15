# coding=UTF-8
import os
import json
from datetime import datetime
import urllib.request
import base64
from utilset.ConfigUtil import ConfigUtil


# 與後台平台或其他系統整合
class PostToGitea():

    __URL = None
    __Account = None
    __Password = None

    # 初始化
    def __init__(self):
        self.__URL = ConfigUtil().IssueURL
        self.__Account = ConfigUtil().Account
        self.__Password = ConfigUtil().Password

    # 發布議題到gitea
    def postGitea(self, data):
        # 抓取Post資料
        number = data["number"]
        issueTitle = data["issueTitle"]
        issueContent = data["issueContent"]
        assignUser = data["assignUser"]
        # 組出要post的json data
        postData = {
            "assignee": None,
            "assignees": assignUser.split('#'),
            "body": issueContent,
            "closed": False,
            "due_date": None,
            "labels": [0],
            "milestone": 0,
            "title": issueTitle
        }
        # 準備要post的json
        postJson = json.dumps(postData, ensure_ascii=False)
        print(postJson)
        # 準備登入驗證base64字串
        base64Str = base64.b64encode(bytes('%s:%s' % (self.__Account, self.__Password), "ascii"))
        # 執行Post
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Basic %s" % base64Str.decode("UTF-8")
        }
        req = urllib.request.Request(url=self.__URL, data=postJson.encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req) as res:
                print(res)
        except Exception as err:
            self.__outputLog("議題編號:%s；標題:%s；Post發生問題:%s" % (str(number), issueTitle, str(err)))

    # 寫入Log檔
    def __outputLog(self, result):
        logFilename = datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ".log"
        # 檢查log資料夾不存在則建立
        if os.path.exists("log") is False:
            os.mkdir("log")
        with open(os.path.join("log", logFilename), "w", encoding='UTF8') as f:
            f.write(result)
