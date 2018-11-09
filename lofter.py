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


def parse(url):
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    return soup



def get_archive(soup,file_name):    
    work = soup.find_all("h2",class_="tit")
    for each in work:
        title = each.get_text()
        address = each.find_parents("div",class_="isay")
        if address != []:
            if title:
                print("try!!")
                addr = address[0].find("a",class_="isayc").get("href")
                datatime = address[0].find("a",class_="isayc").get("data-time")
                data_time = time.localtime(int(datatime[0])/1000)
                data_blogid = each.find_parents("div",class_="m-mlist")[0].get("data-blogid")
                pattern = re.compile("热度\((\d+)\)")
                hot = int(re.findall(pattern,str(address[0]))[0])
                blogname = each.find_parents("div",class_="m-mlist")[0].get("data-blognickname")
                blogid = "http://"+str(addr.split("/")[2])
                text = '<p><a href="'+addr+'" target="_blank">'+title+'</a> '+'[热度：%d]'%hot+'by <a href="'+blogid+'" target="_blank">'+blogname+'</a> <br /></p>'

                with open(file_name, 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([title,addr,blogname,blogid,hot,data_time,data_blogid,text])
            #except(AttributeError):
                #print(title)

    
def dict_rearrange(file_name,file_stat):
    
    """
    输入：file_name文件，字典{title,addr,blogname,blogid,hot,text}
    运算：{blogname:sum(hot)}
    输出：html：{blogname：{title,addr,blogname,blogid,hot,text}} 按作者个人总热度降序
    """
    #sel_lst = []
    count_dict ={}
    counter = 0
    with open(file_name, "r", encoding='utf-8', newline='') as csvfile:
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            print(row['hot'])
            if row["blogname"] in count_dict.keys():
                count_dict[row['blogname']] += int(row['hot'])
            else:
                count_dict[row['blogname']] = int(row['hot'])
        sort_dict = sorted(count_dict.items(), key=lambda d: d[1], reverse= True)
        sort_count_dict = dict(sort_dict)

    with open(file_stat, 'a',encoding='utf-8',newline='') as f:
        writer = csv.writer(f,quotechar=' ')
        for spe_id in sort_count_dict:
            counter += 1
            with open(file_name, "r", encoding='utf-8', newline='') as csvfile:
                dict_reader = csv.DictReader(csvfile)
                writer.writerow(["<p>No."+str(counter)+"  "+spe_id+"<br/></p>"])
                for row in dict_reader:
                    if spe_id == row['blogname']:
                        writer.writerow([row['text']])





def get_pic(soup,file_name_pic):
    global pic_dic
    img = soup.find_all("div",class_="img")
    for each in img:
        addr = []
        title = []
        address = each.find_parents("div",class_="isaym")
        if address != []:
            blogid = address[0].find("a").get("href")
            blogname = address[0].find("a").get_text()
            pattern2 = re.compile("热度\((\d+)\)")
            hot = int(re.findall(pattern2,str(address[0]))[0])
            addr_tag = address[0].find_all("img")
            for content in addr_tag:
                
                try:
                    addrs = (content.get("src")).split("?")[0]
                    addr.append(addrs)
                except(AttributeError):
                   with open("error.csv", 'a', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f,quotechar=' ')
                        writer.writerow([content])
                        

            with open(file_name_pic, 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f,quotechar=' ')
                writer.writerow([title,addr,blogname,blogid,hot])


def pic_rearrange(file_name_pic,file_stat_pic):
    count_dict_pic ={}
    counter = 0
    with open(file_name, "r", encoding='utf-8', newline='') as csvfile:
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            if row["blogname"] in count_dict.keys():
                count_dict_pic[row['blogname']] += int(row['hot'])
            else:
                count_dict_pic[row['blogname']] = int(row['hot'])



#未完成
def pic_download(file_name_pic,file_stat_pic):
    count_dict_pic ={}
    counter = 0
    with open(file_name_pic, "r", encoding='utf-8', newline='') as csvfile:
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            filepath = row["blogname"]
            localpath = os.path.join(filepath,"%s"%url.split('/')[-1])
    urllib.request.urlretrieve(url,localpath)
    row["blogname"]



def archive_download(tag,soup):
    work = soup.find_all("h2",class_="tit")
    for each in work:
        title = each.get_text()
        address = each.find_parents("div",class_="isay")
        if address != []:
            if title:
                archive = address[0].find("div",class_="txt js-content ptag").get_text()
                addr = address[0].find("a",class_="isayc").get("href")
                datatime = address[0].find("a",class_="isayc").get("data-time")
                data_time = time.localtime(int(datatime[0])/1000)
                blogname = each.find_parents("div",class_="m-mlist")[0].get("data-blognickname")
                
                filepath = r"F:/0music/%s/%s"%(tag,blogname)                
                if os.path.exists(filepath) == False:
                    os.makedirs(filepath)
                filepath_ =filepath+"/%s.txt"%title
                savefile = open(filepath_, "a+", encoding='utf-8') 
                savefile.write(title+"\n作者："+blogname+"\n原帖地址："+addr+"\n发帖时间:"+data_time+"\n\n"+archive+"\n\n")            
                savefile.close()
            #except(AttributeError):
                #print(title)


def main_pic(tag,file_name_pic,file_stat_pic):
    with open(file_name_pic, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["title","addr","blogname","blogid","hot"])
    pic_dict = {}
    for i in range(0,61):
        print(i)
        time.sleep(0.5)
        url = "http://www.lofter.com/tag/%s/total?page=%d"%(quote(tag),i)
        get_pic(parse(url),file_name_pic)

        pic_rearrange(file_name_pic,file_stat_pic)

    sort_pic_dict = sorted(pic_dict.items(), key=lambda d: d[1], reverse= True)
    sort_pic_dict = dict(sort_pic_dict)

    for key,value in sort_count_dict_pic:
        with open(file_stat_pic, 'a',encoding='utf-8',newline='') as f:
            writer = csv.writer(f,quotechar=' ')
            writer.writerow([key,value])
        
    return 0



def main_archive(tag,file_name):
    with open(file_name, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["title", "addr","blogname","blogid","data-time","hot","data-blogid","text"])
        print("title", "addr","blogname","blogid","data-time","hot","data-blogid","text")
    for i in range (3,61):
        time.sleep(2)
        url = "http://www.lofter.com/tag/%s/total?page=%d"%(quote(tag),i)
        print(url)
        get_archive(parse(url),file_name)
   
  
def main_download(tag):    
    for i in range (0,61):
        time.sleep(2)
        print(i)
        url = "http://www.lofter.com/tag/%s/total?page=%d"%(quote(tag),i)
        archive_download(tag,parse(url))

        
if __name__=="__main__":        

    tag = input("请输入tag")
    count = 0
    storage =[]
    file_name = tag+"lof.csv"
    file_stat = tag+"stat.csv"
    file_name_pic = tag+"lofpic.csv"
    file_name_stat = tag + "statpic.csv"



    main_archive(tag,file_name)

