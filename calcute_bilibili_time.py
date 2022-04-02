# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 15:40:25 2022
@author: libin
"""
import requests
from bs4 import BeautifulSoup
import json
import re

def logHtmltextToFile(htmlText, filePath):
    try:
        with open(filePath, 'w', encoding = 'utf-8') as f:
            f.write(htmlText)
        f.close()
    except:
        print("保存html文本到文件出错\n")
        
#startChapter---number
#endChapter---number
#return interval seconds
def getIntervalTime(startChapter,endChapter,bv):
    url = "https://www.bilibili.com/video/"+bv+"?p="+str(startChapter)
    kv = {"User-Agent":"chrome/10"}
    res = None;
    #异常处理
    try:
        res = requests.get(url,headers = kv)
        res.raise_for_status()
    except:
        print("网页请求出错\n")
    htmlText = res.text
    soup = BeautifulSoup(htmlText,"html.parser")
    logHtmltextToFile(soup.prettify(), "htmlText.txt")
    tempElements = soup.find_all('script')
    scriptElement = None
    for tempElement in tempElements:
        try:
            if(tempElement.string.startswith('window.__INITIAL_STATE__')):
                scriptElement = tempElement
        except:
            continue
    jsonText = re.search('"videoData".*"upData"', scriptElement.string).group(0).rstrip(',"upData"').lstrip('"videoData":')
    data = json.loads(jsonText) 
    intervalTime = 0
    for i in range(startChapter,endChapter):
        intervalTime = intervalTime + data['pages'][i-1]['duration']
    return intervalTime


def main():
    #bv---string
    print("友情提示:使用本程序请关闭科学上网\n")
    bv=input("输入位于链接中的bv号:")
    startChapter = int(input("输入起始章节数字:\n"))
    endChapter = int(input("输入结束章节数字:\n"))
    seconds = getIntervalTime(startChapter,endChapter,bv)
    print("---------------视频统计信息---------------")
    print("序号"+str(startChapter)+"到"+str(endChapter))
    print("总时长:"+str(seconds)+"秒")
    print("约"+str(seconds/60)+"分")
    print("约"+str(seconds/3600)+"时")
    print("约"+str(seconds/(24*60*60))+"天")
    input("按任意键继续...")
main()