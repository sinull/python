
#-* coding: utf-8 -*

import threading
import time
import os

def booth(tid):
  global i
  global lock
  while True:
    lock.acquire()
    if i!=0:
      i=i-1
      print u"窗口:",tid,u",剩余票数:",i
      
    else:
      print "Thread_id",tid,"No more tickets"
      os._exit(0)
    lock.release()

i = 100
lock=threading.Lock()

for k in range(5):

  new_thread = threading.Thread(target=booth,args=(k,))
  new_thread.start()
