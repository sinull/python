##import threading
##import time
## 
##counter = 0
##mutex = threading.Lock()
## 
##class MyThread(threading.Thread):
##    def __init__(self):
##        threading.Thread.__init__(self)
## 
##    def run(self):
##        a = 0
##        global counter, mutex
##        if mutex.acquire():
##        for i in range(10000000):
##            a+=1
##        counter += a
##            mutex.release()
## 
##if __name__ == "__main__":
##    a = time.time()
##    for i in range(10):
##        my_thread = MyThread()
##        my_thread.start()
##    my_thread.join()
##    print time.time()-a,counter
import threading
import time
import threadpool 
 
counter = 0
mutex = threading.Lock()
 
def run(self):
    a = 0
    global counter, mutex
    if mutex.acquire():   
        for i in range(10000000):
            a+=1
        counter += a
        mutex.release()   
 
if __name__ == "__main__":
    a = time.time()
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(run, range(10))
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print time.time()-a,counter
