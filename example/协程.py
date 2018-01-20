import time
 
def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('Consume running %s...' % n)
        time.sleep(1) #遇到阻塞到produce执行
        r = '200 OK'
 
def produce(c):
    c.next() #启动迭代器
    n = 0
    while n < 5:
        n = n + 1
        print('[Produce] running %s...' % n)
        r = c.send(n) #到consumer中执行
        print('[Consumer] return: %s' % r)
    c.close()
 
if __name__=='__main__':
    c = consumer() #迭代器
    produce(c)
