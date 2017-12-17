# -*- coding: utf-8 -*-
#python2
import os, urllib2, requests, gzip,urllib,json,sys,re
from StringIO import StringIO
from bs4 import BeautifulSoup
from prettytable import PrettyTable

def get_html(url):
    line=raw_input("苏州公交实时查询系统\n请输入车次\n例 8，快8:".decode("utf-8").encode("gb2312"))
    if line != '' :          
        url=url+urllib.quote(line.decode('GBK').encode('utf-8'))
        req = urllib2.Request(url=url,headers={'Accept-Encoding': 'gzip, deflate',})
        res = urllib2.urlopen(req)
        html = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(html)
            f = gzip.GzipFile(fileobj=buf)
            html = f.read()
            return html
    else:
        return '123'
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
    head = u'线路,序号,始末站'.split(',')
    pt = PrettyTable()
    pt._set_field_names(head)
    pt.align = "c"
    if g !=0:
        for i in range(g):
            pt.add_row([line[i],'('+str(i)+')',station[i]])      
        print pt.get_string()
        return 'suc'
        
def refun(url):
    newurllist=[]
    pattern = re.compile('(lineID.*)&|(lineID.*)')
    for i in url:
        num = re.search(pattern,i)
        newurllist.append(num.group()[:15])
    return newurllist

def get_html2(url,urllist):
    line=raw_input('输入车次序号查看实时车辆：'.decode("utf-8").encode("gb2312")).decode(sys.stdin.encoding )
    req = urllib2.Request(url=url,headers={'Accept-Encoding': 'gzip, deflate',})
    if int(line)<len(urllist):
        req = urllib2.Request(url=url,data = urllist[int(line)],headers={'Accept-Encoding': 'gzip, deflate',})
        res = urllib2.urlopen(req)
        html = res.read()
        if res.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(html)
            f = gzip.GzipFile(fileobj=buf)
            html = f.read().decode('utf-8')
            html = html[1:]
            data = json.loads(html)
            return data['data']

def pretty_print2(line):
    head = u'站点,车牌,时间'.split(',')
    pt = PrettyTable()
    pt._set_field_names(head)
    list1 = []
    for i in line:
        if i['BusInfo']!='':
            pt.add_row([i['StationCName'],i['BusInfo'],i['InTime']])
        else :
            pt.add_row([i['StationCName'],(u'*'),(u'*')])
            list1.append(i['BusInfo'])

    pt.align = "c"
    print pt.get_string(),'\n'
  
def busstart():
    while 1:
        data = get_html('http://bus.2500.tv/line.php?line=')
        station,line,url,g = parse(data)
        newurllist = refun(url)
        while pretty_print(station,line,g) !='suc':
            print u'输入有误\n'
            break
        else:
            try:
                data2 = get_html2('http://bus.2500.tv/api_line_status.php',newurllist)
                pretty_print2(data2)
            except:
                print u'输入有误\n'

if __name__ == '__main__':
    busstart()

                
                
     
                

    
    
    
    
    
  
