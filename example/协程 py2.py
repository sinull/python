#coding:utf-8
#python27 使用gevent实现协程

import gevent
from gevent import monkey;monkey.patch_all()
import urllib2
def get_body(i):
	print ("start",i)
	urllib2.urlopen("http://cn.bing.com")
	print ("end",i)
tasks=[gevent.spawn(get_body,i) for i in range(3)]
gevent.joinall(tasks)


#python27 使用多线程
import threading
import urllib2
def get_body(i):
	print "start",i
	urllib2.urlopen("http://cn.bing.com")
	print "end",i
for i in range(3):
	t=threading.Thread(target=get_body,args=(i,))
	t.start()
