# coding=UTF-8
import urllib.request
import base64
import json

#__Account = "Bob"
#__Password = "***"
# 準備登入驗證base64字串
#base64Str = base64.b64encode(bytes('%s:%s' % (__Account, __Password), "ascii"))
# 執行Get，取得所有的issue清單
# headers = {
#    'Content-Type': 'application/json',
#    'Authorization': "Basic %s" % base64Str.decode("UTF-8")
# }
srcHeaders = {
    'Content-Type': 'application/json',
    'Authorization': "Basic %s" % base64.b64encode(bytes('%s:%s' % ("Bob", "***"), "ascii")).decode("UTF-8")
}
tagHeaders = {
    'Content-Type': 'application/json',
    'Authorization': "Basic %s" % base64.b64encode(bytes('%s:%s' % ("Bob", "***"), "ascii")).decode("UTF-8")
    # 'Authorization': "Basic %s" % base64.b64encode(bytes('%s:%s' % ("Bob", "***"), "ascii")).decode("UTF-8")
}


# 取得Gitea的Issue
def getIssues():
    # gitea api撈issues資料太多會分頁，這邊輪詢到沒有issue資料為止
    page = 1
    srcJsonData = []
    while True:
        # WebUrl = "http://192.168.1.41:3000/api/v1/repos/DSICWEBAP/DSICWEBAP/issues?state=all&page=%s&limit=999" % page
        # WebUrl = "http://192.168.1.41:3000/api/v1/repos/CloudJOP/JOP/issues?state=all&page=%s&limit=999" % page
        # WebUrl = "http://192.168.1.41:3000/api/v1/repos/CloudJOP/JOP/issues?state=all&page=%s&limit=999" % page
        WebUrl = "http://192.168.1.41:3000/api/v1/repos/CloudJOPLite/JOPLite/issues?state=all&page=%s&limit=999" % page
        req = urllib.request.Request(url=WebUrl, headers=srcHeaders, method="GET")
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read())
                # 檢查撈不到資料，就脫離迴圈
                if len(data) <= 0:
                    break
                # 把所有資料merge起來
                for item in data:
                    srcJsonData.append(item)
        except Exception as err:
            print("取得Gitea issue列表發生問題:%s" % (str(err)))
        page = page + 1
    # 排序一下，從第一筆開始處理
    sorted(srcJsonData, key=lambda item: item["number"])
    srcJsonData.reverse()
    return srcJsonData

# 取得Gitea單筆的Comments


def getComments(index):
    srcComData = []
    #WebUrl = "http://192.168.1.41:3000/api/v1/repos/DSICWEBAP/DSICWEBAP/issues/%s/comments" % index
    # WebUrl = "http://192.168.1.41:3000/api/v1/repos/CloudJOP/JOP/issues/%s/comments" % index
    WebUrl = "http://192.168.1.41:3000/api/v1/repos/CloudJOPLite/JOPLite/issues/%s/comments" % index
    req = urllib.request.Request(url=WebUrl, headers=srcHeaders, method="GET")
    try:
        with urllib.request.urlopen(req) as res:
            srcComData = json.loads(res.read())
    except Exception as err:
        print("取得Gitea issue列表發生問題:%s" % (str(err)))
    return srcComData


srcJsonData = getIssues()
# 這邊處理成create issue的格式
tarJsonData = []
for item in srcJsonData:
    # 取得指派人
    assigner = "" if item["assignee"] is None else item["assignee"]["username"]
    # 取得分派人
    assigners = []
    if item["assignees"] is not None:
        for user in item["assignees"]:
            assigners.append(user["username"])
    # 撰寫create的json
    tarJsonData.append({
        "assignee": assigner,
        "assignees": assigners,
        "body": item["body"],
        "closed": True if item["state"] == "closed" else False,
        "due_date": None,
        "labels": [],
        "milestone": None,
        "title": item["title"],
        "srcNumber": item["number"]
    })
# Post New Issue
# PostIssueUrl = "http://192.168.1.41:3000/api/v1/repos/Bob/TEST/issues"
# PostIssueUrl = "http://gitea.dsic.com.tw/api/v1/repos/DSICWEBAP-JOPV2/DSICWEBAP/issues"
# PostIssueUrl = "http://gitea.dsic.com.tw/api/v1/repos/CLOUDJOP-JOPV1/JOP/issues"
PostIssueUrl = "http://gitea.dsic.com.tw/api/v1/repos/CLOUDJOPLITE-JOPV1/JOPLite/issues"

for issue in tarJsonData:
    # 準備要post的json
    postJson = json.dumps(issue, ensure_ascii=False)
    req = urllib.request.Request(url=PostIssueUrl, data=postJson.encode("utf-8"), headers=tagHeaders, method="POST")
    try:
        with urllib.request.urlopen(req) as res:
            # 新增issue成功，擷取被配置的ID
            ID = json.loads(res.read())["number"]
            # 抓來源的commends，POST到目前新的ID
            # PostCommentUrl = "http://192.168.1.41:3000/api/v1/repos/Bob/TEST/issues/%s/comments" % ID
            # PostCommentUrl = "http://gitea.dsic.com.tw/api/v1/repos/DSICWEBAP-JOPV2/DSICWEBAP/issues/%s/comments" % ID
            # PostCommentUrl = "http://gitea.dsic.com.tw/api/v1/repos/CLOUDJOP-JOPV1/JOP/issues/%s/comments" % ID
            PostCommentUrl = "http://gitea.dsic.com.tw/api/v1/repos/CLOUDJOPLITE-JOPV1/JOPLite/issues/%s/comments" % ID
            srcComData = getComments(issue["srcNumber"])
            for com in srcComData:
                body = com["body"]
                # 上傳內容到新的issue point
                postComJson = json.dumps({"body": body}, ensure_ascii=False)
                reqCom = urllib.request.Request(url=PostCommentUrl, data=postComJson.encode("utf-8"), headers=tagHeaders, method="POST")
                try:
                    with urllib.request.urlopen(reqCom) as resCom:
                        print(resCom)
                except Exception as err:
                    print(err)
    except Exception as err:
        print(err)

print("議題導入Gitea作業完成")
input("按一下enter離開")
