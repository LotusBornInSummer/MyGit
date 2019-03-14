import tkinter
from tkinter import messagebox
import csv
import re
import os
from bs4 import BeautifulSoup
import requests
import time
import random
import platform

class DownloadArchiveInTag(object):
    def __init__(self):
        
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        self.root.update()
        # 给主窗口设置标题内容
        self.root.title("download_archives_in_tag")
        #窗口大小是否可变
        self.root.geometry("500x450")
        self.root.resizable(width=True, height=True)
        #外部输入tag名，时间截点，热度筛选，屏蔽tag
        tag_name_input = tkinter.StringVar()
        tag_name_input.set("hp")
        self.tag_input = tkinter.Entry(self.root,textvariable=tag_name_input,width=30)
            
        time_input = tkinter.StringVar()
        time_input.set("2011-12-01")
        self.time_input = tkinter.Entry(self.root,textvariable=time_input,width=30)

        hot_filter_input = tkinter.StringVar()        
        hot_filter_input.set("300")
        self.hot_filter_input = tkinter.Entry(self.root,textvariable=hot_filter_input,width=30)

        tag_filter_input=tkinter.StringVar()
        self.tag_filter_input = tkinter.Entry(self.root,textvariable=tag_filter_input,width=30,state="disabled")
        
        self.down_check = tkinter.IntVar()
        self.down_check.set(0)
        self.download_check = tkinter.Checkbutton(self.root,text = "下载文章",variable=self.down_check, onvalue="1",offvalue="0")
        
        self.shield_check = tkinter.IntVar()
        self.shield_check.set(0)
        self.tag_filter_check = tkinter.Checkbutton(self.root,text = "屏蔽tag（多个tag请用逗号分隔）",variable=self.shield_check, onvalue="1",offvalue="0",command=self.check_shielding_input)
        # 创建一个回显列表
        self.display_slider=tkinter.Scrollbar(self.root)
        self.display_info = tkinter.Text(self.root,width=40,height=20,yscrollcommand=self.display_slider.set)
        self.display_slider.config(command=self.display_info.yview)
        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command = self.download, text = "开始")
        
    #控件布局    
    def gui_arrang(self):
        tkinter.Label(self.root,text="请输入tag").grid(row=0,column=0,stick="w")
        tkinter.Label(self.root,text="搜索截止日期").grid(row=1,column=0,stick="w")
        tkinter.Label(self.root,text="筛选热度").grid(row=2,column=0,stick="w")
        self.tag_filter_check.grid(row=3,column=0,stick="w")
        self.tag_input.grid(row=0,column=1,stick="w")
        self.time_input.grid(row=1,column=1,stick="w")
        self.hot_filter_input.grid(row=2,column=1,stick="w")
        self.tag_filter_input.grid(row=3,column=1,stick="w")
        self.download_check.grid(row=4,column=1,stick="w")
        self.display_info.grid(row =5,column=0,columnspan=2)
        #self.display_slider["command"] = self.display_info.yview
        self.display_slider.grid(row = 5,column =2,sticky="N"+"S")#.(side="right",fill="y")
        self.result_button.grid(row=6,column=1)

     #控件的禁用启用
    def check_shielding_input(self):
        if self.shield_check.get()==1:
            self.tag_filter_input.config(state="normal")
        else:
            self.tag_filter_input.config(state="disabled")
    
    #下载文章
    def download_archive(self,paths,title,author,url,archive):
        filename = "%s/%s_%s.txt"%(paths,author,title)
        archive = BeautifulSoup(archive,"html.parser").get_text()
        try:
            with open (filename,"w",encoding="utf-8",errors="ignore") as f:
                f.write("原文地址：%s\n"%url)
                f.write(archive)
                f.close()
        except(OSError):
            with open("fail_to_download.csv","a+",encoding="utf-8") as csv_file2:
                writer2 = csv.writer(csv_file2)
                writer2.writerow([title,author])
        except(UnicodeEncodeError):
            with open("fail_to_download.csv","a+",encoding="utf-8") as csv_file2:
                writer2 = csv.writer(csv_file2)
                writer2.writerow([title,author])

    #下载外链
    def download_links(self,paths,title,author,archive):
        archive_links = BeautifulSoup(archive,"html.parser").find_all("a")
        serial = 0
        for each_link in archive_links:
            if (".jpg"or".jpeg"or ".png") in each_link["href"]:
                serial += 1
                path = "%s/%s_%s%d.jpg"%(paths,author,title,serial)              
                self.download_image(path,each_link["href"])
    
    #图链
    def download_image(self,path,imgurl):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
        for i in range(1,3):
            try:
                image_request = requests.get(imgurl, headers = headers, timeout = 20)
                if image_request.status_code == 200:
                    open(path, 'wb').write(image_request.content)
                    #image = Image.open(path)
                    #text = pytesseract.image_to_string(image,lang="chi_sim")
                    #open(path_txt, 'w+').write(text)
                    break
            except requests.exceptions.ConnectionError as e:
                pass
            finally:
                pass

     #三个常用外链库，都没写
    def download_ao3(self):
        #感觉，这个可能要区分一下是不是proceed页面
        pass

    def download_shimo(self):
        pass

    def download_weibo(self):
        pass
            
    #写入文件
    def manage_title(self,title):
        if "/" in title:
            title = title.replace('/','-')
        if "|" in title:
            title = title.replace('|','-')
        if "\\" in title:
            title = title.replace('\\','-')
        return title

    def create_query_data(self,tag_lofter,i,timestamp_now):
        data = {'callCount':'1',
                'scriptSessionId':'${scriptSessionId}187',
                'httpSessionId':'',
                'c0-scriptName':'TagBean',
                'c0-methodName':'search',
                'c0-id':'0',
                'c0-param0':'string:%s'%tag_lofter,
                'c0-param1':'number:0',
                'c0-param2':'string:',
                'c0-param3':'string:new',
                'c0-param4':'boolean:false',
                'c0-param5':'number:0',
                'c0-param6':'number:20',
                'c0-param7':'number:%d' %(20*i),
                'c0-param8':'number:%d'%timestamp_now,
                'batchId':'123456'}
        return data

            
    def download(self):
        self.result_button.config(text="运行中")
        pattern_date= re.compile("20\d{2}-[0-1]\d-\d{2}")
        result = re.match(pattern_date,self.time_input.get())
        if result == None:
            self.tkinter.Message
            self.display_info.insert("end","请以年年年年-月月-日日的格式输入，LOFTER是2011年8月创建的，想要搜索全部请输入2011-08-01")
            self.result_button.config(text="开始")
            return 0
        
        tag_lofter = self.tag_input.get()
        paths = {
        'Windows': 'D:/lofter/' + tag_lofter,
        'Linux': '/mnt/d/lofter/' + tag_lofter
        }.get(platform.system())
        if not os.path.isdir(paths):
            os.makedirs(paths)
        tag_filter = self.tag_filter_input.get()
        tag_filter_list = tag_filter.split(",")
        res_tag_num = requests.get("http://www.lofter.com/tag/%s?tab=archive"%tag_lofter)
        tag_num_pattern=re.compile('''<span class="joincount">(\d*)参与</span>''')
        tag_num = re.findall(tag_num_pattern,res_tag_num.text)
        if tag_num == [] or tag_num ==['1']:
            self.display_info.insert("end","tag下无信息")
            self.result_button.config(text="开始")
            return 0
        else:
            self.display_info.insert("end","tag下共%s条"%tag_num[0])
            tag_page = round(int(tag_num[0])/20)

        hot_filter = int(self.hot_filter_input.get())
        time_stamp = time.mktime(time.strptime('%s 00:00:00'%self.time_input.get(), '%Y-%m-%d %H:%M:%S'))
        url_res = "http://www.lofter.com/dwr/call/plaincall/TagBean.search.dwr"
        headers = {
                "Accept": '*/*',
                "Accept-Encoding": "gzip",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Content-Length": "245",
                "Content-Type": "text/plain",
                "Host": "www.lofter.com",
                "Origin": "http://www.lofter.com",
                "Referer": "http://www.lofter.com/tag/ggad?tab=archive",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                }
        time_stamp_now =round(time.time()*1000)
        data = self.create_query_data(tag_lofter,0,time_stamp_now)
        for i in range(0,tag_page):
            if (i%3 == 1):
                self.display_info.update()
            if i :
                time_pattern = re.compile('s\d*?\.publishTime=(\d*);' )
                timestamp = re.findall(time_pattern,res.text)                
                if (int(timestamp[-1])<1000*time_stamp):
                    #hot_filter = 200
                    self.result_button.config(text="开始")
                    return 0
                data["c0-param7"]='number:%d'%(20*i)
                data["c0-param8"]='number:%s'%timestamp[-1]
            time3 = time.time()
            res = requests.post(url_res,data=data,headers=headers)
            time4 = time.time()
            res.encoding = "unicode_escape"
            title_pattern = re.compile('''s(\d*).title=\"(.*?)\";''')
            title = re.findall(title_pattern,res.text)
            for each in title:
                judge = 0
                if self.shield_check.get()==1:
                    tag_pattern = re.compile('''s%s.tag=\"(.*?)\"'''%each[0])
                    tags = re.findall(tag_pattern,res.text)
                    if tags != []:
                        tags = tags[0].lower()
                    for xxx in tag_filter_list:
                        if xxx == "":
                            pass
                        else:
                            xxx = xxx.lower()
                            if xxx in tags:
                                judge = 1
                                break
                if judge == 0:
                    if each[1] != "" and each[1] != "title":
                        if "," in each[1]:
                            title = str(each[1]).split(",")[0]
                        else:
                            title = each[1]
                        title = self.manage_title(title)
                        hot_pattern = re.compile('''s%s.hot=(\d*);'''%each[0])
                        hot = re.findall(hot_pattern,res.text)
                        if hot != []:
                            if int(hot[0])>hot_filter:
                                url_pattern = re.compile('''s%s.blogPageUrl=\"(.*?)\";'''%each[0])
                                blogid_pattern = re.compile('''s%s.blogId=(\d*?);'''%each[0])
                                url = re.findall(url_pattern,res.text)
                                blogurl = url[0].split("post")[0]
                                blogid = re.findall(blogid_pattern,res.text)
                                blognickname_pattern = re.compile('''s\d*.blogId=%s;.*?blogNickName=\"(.*?)\";'''%blogid[0])
                                blognickname = re.findall(blognickname_pattern,res.text)                                
                                self.display_info.insert('end',"%s [热度：%s]\n%s\n"%(title,hot[0],url[0]))             
                                
                                if self.down_check.get() ==1:                                        
                                    archive_pattern = re.compile('''s%s\.content=\"(.*?)\";'''%each[0],re.S)
                                    archive = re.findall(archive_pattern,res.text)
                                    self.download_links(paths,title,blognickname[0],archive[0])
                                    self.download_archive(paths,title,blognickname[0],url[0],archive[0])
        self.result_button.config(text="开始")
        return 0


def main():
    # 初始化对象
    FL = DownloadArchiveInTag()
    # 进行布局
    FL.gui_arrang()
    # 主程序执行
    tkinter.mainloop()
    pass


if __name__ == "__main__":
    main()
