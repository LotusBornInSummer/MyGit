# -*- coding:utf-8 -*-

import csv
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import time
from collections import Counter
from urllib.parse import quote
import codecs
import os
import shutil
import random



def parse(tag,key,blogid):
    url = blogid[1] + "/dwr/call/plaincall/ArchiveBean.getArchivePostByTag.dwr"
    time_now = int(time.time()*1000)
    k = random.randint(100000,999999)
    k2 = random.randint(1,10)
    headers = {
        "Accept": '*/*',
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "245",
        "Content-Type": "text/plain",
        "Cookie": "_ga=GA1.2.1167147232.1422534223; usertrack=ezq0plqpHkUhneWSCsWsAg==; _ntes_nnid=02839b8d5d821ed9549b16efd119581e,1521032776189; reglogin_hasopened=1; razor_sign_js_cookie=f16592f9038d5cd8cac1828ff3ffc962; razor_1_0_1_sign_js_cookie=2c3ba79066b9eaf9817d95e53f988b09; __utmz=61349937.1535794075.467.57.utmcsr=lofter.com|utmccn=(referral)|utmcmd=referral|utmcct=/; JSESSIONID-WLF-XXD=bb2b2f599ca49acd6b9828cbd5db0cbd3c16b0543cac84ee73e783e51037668d9df447c9d2c8be6c11d5206f68187eb556c500b1bdbf9e1a78bfa64af5105c84f3d96cd01e8c65aec5bc5a380e9478b280fccb45317b5df91bcbfeb0971a870db0abd6881fe54aefd7e3555f336484d5892a09891d96690d2896c959a1651e63973ed753; __utmc=61349937; firstentry=%2FtagSearch.do%3Ftype%3D0%26recommType%3Dtotal%26X-From-ISP%3D1%26tag%3Dggad|; _gid=GA1.2.1018023908.1541577461; LOFT_SESSION_ID=RVnK4WJ6DFWs6Gaii6U5kQHqXsnB58Nu; reglogin_isLoginFlag=; PRIVILEGE_USER_IDENTIFICATION=-1; __utma=61349937.1167147232.1422534223.1541639787.1541660297.502; hb_MA-BFD7-963BF6846668_source=jofing.lofter.com; reglogin_isLoginFlag=; NTESwebSI=D3AB0BD6D60954B4C9BB7C1B668D0BBA.hzayq-lofter-web8.server.163.org-8010; __utmb=61349937.30.7.1541660726090; mp_MA-BFD7-963BF6846668_hubble=%7B%22sessionReferrer%22%3A%20%22%22%2C%22updatedTime%22%3A%201541662188623%2C%22sessionStartTime%22%3A%201541660725487%2C%22sendNumClass%22%3A%20%7B%22allNum%22%3A%205%2C%22errSendNum%22%3A%203%7D%2C%22deviceUdid%22%3A%20%22c6a5a196-0c57-48da-b37c-30f419ba902e%22%2C%22persistedTime%22%3A%201541488666301%2C%22LASTEVENT%22%3A%20%7B%22eventId%22%3A%20%22da_u_logout%22%2C%22time%22%3A%201541662188624%7D%2C%22sessionUuid%22%3A%20%22bea043d0-7b18-46b3-9eb2-354596095f97%22%7D",
        "Host": "%s.lofter.com"%blogid[1][7:].split(".")[0],
        "Origin": "http://%s.lofter.com"%blogid[1][7:].split(".")[0],
        "Referer": "http://%s.lofter.com/view"%blogid[1][7:].split(".")[0],
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

    payload ={
        "callCount":"1",
        "scriptSessionId":"${scriptSessionId}187",
        "httpSessionId":"",
        "c0-scriptName":"ArchiveBean",
        "c0-methodName":"getArchivePostByTag",
        "c0-id":"0",
        "c0-param0":"number:%d"%key,
        "c0-param1":"string:%s"%tag,
        "c0-param2":"number:%d"%(time_now),
        "c0-param3":"number:50",
        "batchId":"%d"%k
        }
    
    res = requests.post(url,data=payload,headers=headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    pattern = re.compile('s.*\.permalink="(.*?)"')
    link = re.findall(pattern,str(soup))
    print(blogid[1][7:].split(".")[0],len(link))
    #file_name = blogid[1][7:].split(".")[0]+".txt"
        #with open(file_name,"a+",encoding="utf-8") as f:
            #url_to_write = true_url+"\n"
            #f.write(url_to_write)
            #f.close()
    
    for each in link:
        archive =""
        true_url = blogid[1] + "/post/"+each
        time.sleep(2)
        res_url = requests.get(true_url,timeout=60)
        res_url.encoding = "utf-8"
        soup_url = BeautifulSoup(res_url.text,"html.parser")
        pattern_time = re.compile("\d{2}\/\d{2}\/\d{4}|\d+\.\d+\.\d{4}|\d{4}-\d+-\d+")
        time_url = re.findall(pattern_time,str(soup_url))
        print(time_url)
        if time_url != []:
            time_url_ =time_url[0]
        else:
            time_url_ = ""
        title_tag = soup_url.find_all("h2")
        if title_tag != []:
            title = title_tag[0].get_text()
            if "/" in title:
                titles = title.split('/')
                title = ""
                for each in titles:
                    title += each
                    title += "-"
            if "|" in title:
                titles = title.split('|')
                title = ""
                for each in titles:
                    title += each
                    title += "-"
        else:
            title = "随笔"
        archive = title+"\n"+"作者:"+blogid[0]+"\n发表时间:"+time_url_+"\n原帖地址:"+true_url+"\n"
        body = soup_url.find_all("p")
        if body != []:
            for each in body:
                archive += each.get_text()
                archive += "\n"
                

        filepath = r'F:/lofter/%s/%s/'%(tag,blogid[0])
        #保存路径
        
        if os.path.exists(filepath)==False:
            os.makedirs(filepath)
        filename = filepath+title+".txt"
        try:
            with open (filename,"a",encoding="utf-8") as f:
                content_write = "%s\n"
                f.write(archive)
                f.close()
        except(OSError):
            with open("error.csv","a+",encoding="utf-8") as csv_file2:
                writer2 = csv.writer(csv_file2)
                writer2.writerow([[key],true_url_,blogid[0],blogid[1]])
    with open("record.csv","a+",encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([key])
        
def read(tag,file_name):
    count_dict={}
    
    with open(file_name,"r",encoding="utf-8") as csvfile:
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            count_dict[row['data-blogid']] = [row['blogname'],row['blogid']]

    with open("dict.txt","w",encoding="utf-8") as dict_file:
        dict_file.write(str(count_dict))

    for key in count_dict:
        blogid = count_dict[key]
        parse(tag,int(key),blogid)

def reread(tag,file_name):
    count_dict={}
    
    with open(file_name,"r",encoding="utf-8") as csvfile:
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            count_dict[row['data-blogid']] = [row['blogname'],row['blogid']]

    interrupt = list(count_dict.values())[0][0]
    
    with open("record.csv","r",encoding="utf-8") as csv_file:
        dict_reader = csv.DictReader(csv_file)
        for row in dict_reader:
            del count_dict[row[interrupt]]

    with open("dict.txt","w",encoding="utf-8") as dict_file:
        dict_file.write(str(count_dict))

    del count_dict[interrupt]

    shutil.rmtree("F:/lofter/%s/%s"%(tag,interrupt))

    for key in count_dict:
        blogid = count_dict[key]
        parse(tag,int(key),blogid)



if __name__=="__main__":
    file_name = input("请输入需要读取的文件名")
    tag = input("请输入搜索的tag")
    read(tag,file_name)
    reread(tag,file_name)#如果之前报错，请使用REREAD函数

