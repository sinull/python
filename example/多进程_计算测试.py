from multiprocessing import Pool,Manager, Value
import time

def num(x):
    a = 0
    for i in range(10000000):
        a+=1
    x.value += a
    
def multi():
    manager = Manager()
    x = manager.Value('i', 0) 
    pool=Pool(processes=8)
    for i in range(10):
        pool.apply_async(num,(x,))
    pool.close()
    pool.join()
    return x.value             

if __name__ == "__main__":
    a = time.time()
    b = multi()
    print b ,time.time()-a
