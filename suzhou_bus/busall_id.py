# -*- coding: utf-8 -*-
import os, urllib2, requests, gzip,urllib,json,sys,re
from StringIO import StringIO
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import time,datetime,csv

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
    urllist = []
    for a in links:
        for b in a.find_all('a'):
            urllist.append(b.get('href'))
    return urllist
        
def refun(url):
    newurllist=[]
    pattern = re.compile('(lineID.*)&|(lineID.*)')
    for i in url:
        num = re.search(pattern,i)
        newurllist.append(num.group()[:15])
    return newurllist
                    
def spider():
    data = get_html('http://bus.2500.tv/line.php?line=%BF%EC')
    url = parse(data)
    newurllist = refun(url)
    urls = []
    for i in newurllist:
        urls.append((i,))
    txt = file('id.csv','wb')
    write = csv.writer(txt)
    write.writerows(urls)
    txt.close()
         

if __name__ == '__main__':
    spider()

    
                  



            
        

    
    
    
    
    
  
