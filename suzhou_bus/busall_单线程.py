# -*- coding: utf-8 -*-
import os, urllib2, requests, gzip,urllib,json,sys,re
from StringIO import StringIO
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import time,datetime

def get_html(url):
    req = urllib2.Request(url=url,headers={'Accept-Encoding': 'gzip, deflate',})
    res = urllib2.urlopen(req)
    html = res.read()
    if res.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(html)
        f = gzip.GzipFile(fileobj=buf)
        html = f.read()
        return html
    
def parse (html):
    bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    links = bs.find_all('dd')
    stationlist=[]
    linelist = []
    urllist = []
    for a in links:
        for b in a.find_all('a'):
            urllist.append(b.get('href'))
            stationlist.append(b.find_all('p')[1].text)
            linelist.append(b.find_all('p')[0].text)
    g= len(linelist)
    for c in range (g):
        stationlist[c] = stationlist[c][38:]
    return stationlist,linelist,urllist,g

def pretty_print(station,line,g):
    head = '线路,站点,序号'.split(',')
    pt = PrettyTable()
    pt._set_field_names(head)
    if g !=0:
        for i in range(g):
            pt.add_row([line[i],station[i],i])      
        print pt
    else:
        print u'输入有误，或无此车次'
        
def refun(url):
    newurllist=[]
    pattern = re.compile('(lineID.*)&|(lineID.*)')
    for i in url:
        num = re.search(pattern,i)
        newurllist.append(num.group()[:15])
    return newurllist

def get_html2(url,urllist):
    req = urllib2.Request(url=url,headers={'Accept-Encoding': 'gzip, deflate',})
    for i in urllist: 
        req = urllib2.Request(url=url,data = i,headers={'Accept-Encoding': 'gzip, deflate',})
        res = urllib2.urlopen(req)
        html = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(html)
            f = gzip.GzipFile(fileobj=buf)
            html = f.read().decode('utf-8')
            html = html[1:]
            data = json.loads(html)
            for i in data['data']:
                if i['BusInfo']!='':
                    yield i['BusInfo']
                    
def spider():
    data = get_html('http://bus.2500.tv/line.php?line=%BF%EC')
    station,line,url,g = parse(data)
    #pretty_print(station,line,g)
    dict1 = set()
    newurllist = refun(url)
    data2 = get_html2('http://bus.2500.tv/api_line_status.php',newurllist)
    num = 0
    for i in data2:
        num = num+1
        print num
    return str(num)
    

if __name__ == '__main__':
    
    while 1:
        num = spider()
        print u'完成一轮'
        txt = file('data3.txt','a')
        txt.write("\""+str(time.time())+"\""+":"+"\""+num+"\""+',')
        txt.close()
        
                  



            
        

    
    
    
    
    
  
