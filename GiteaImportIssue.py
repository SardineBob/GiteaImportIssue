# coding=UTF-8
import tkinter as tk
from tkinter import filedialog
from utilset.ConfigUtil import ConfigUtil
from component.PostToGitea import PostToGitea

frame = tk.Tk()
frame.withdraw()
# 取得選取的CSV檔案路徑
csvPath = filedialog.askopenfilename()
# 未選取檔案，跳離程式
if csvPath == "":
    exit()
# 讀取CSV檔案
print("開始分析CSV檔")
postToGitea = PostToGitea()
with open(csvPath, "r", encoding="UTF8") as f:
    line = f.readline().replace("\n", "")
    while line:
        number, issueTitle, issueContent, assignUser = line.split(",")
        postToGitea.postGitea({
            "number": number,
            "issueTitle": issueTitle,
            "issueContent": issueContent,
            "assignUser": assignUser
        })
        line = f.readline().replace("\n", "")
print("議題導入Gitea作業完成")
input("按一下enter離開")
