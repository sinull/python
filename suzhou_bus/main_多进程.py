# -*- coding: utf-8 -*-
#python2.7
import os, urllib2,gzip,json,sys
from StringIO import StringIO
import time
from multiprocessing import Pool,Manager, Value
import csv
def req(i,x):
    url ='http://bus.2500.tv/api_line_status.php'
    req = urllib2.Request(url=url,data = i,headers={'Accept-Encoding': 'gzip, deflate',})
    res = urllib2.urlopen(req)
    html = res.read()
    if res.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(html)
        f = gzip.GzipFile(fileobj=buf)
        html = f.read().decode('utf-8')
        html = html[1:]
        data = json.loads(html)
        num=0
        for i in data['data']:
            if i['BusInfo']!='':
                num+=1      
        x.value += num            
def multi(urllist):
    manager = Manager()
    x = manager.Value('i', 0) 
    pool=Pool(processes=50)
    for i in urllist:
        pool.apply_async(req,(i[0],x,))
    pool.close()
    pool.join()
    return x.value

if __name__ == '__main__':
    while 1:
        with open("id.csv","rb") as f:
            f_csv = csv.reader(f)
            num = multi(f_csv)
            f.close()
            print u'完成一轮'
            print time.ctime()
            txt = file('data1.txt','a')
            txt.write("\""+str(time.time())+"\""+":"+"\""+str(num)+"\""+',')
            txt.close()
    








    
