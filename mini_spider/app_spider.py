#encoding:utf-8
import requests,json,pprint,os
import time
from multiprocessing import Lock, Pool
def pre():
    b= requests.get('http://service.picasso.adesk.com/v1/wallpaper/category?adult=false&first=1').content
    a = json.loads(b)['res']['category']
    name = []
    idid = []
    for i in a :
        name.append(i['name'])
        idid.append(i['id'])
    return name,idid
def firstpage(idid,name):
    c=0
    data = []
    for i in idid:
        url = 'http://service.picasso.adesk.com/v1/wallpaper/category/'+i+'/wallpaper?limit=30&adult=false&first=1&order=new'
        html = json.loads(requests.get(url).content)
        dis =html['res']['wallpaper']
        data.append(dis)    
    for i in data:
        b= name[c]
        c = c+1
        for j in i:
            if not os.path.exists(os.path.join('data',b)):
                try:
                    os.makedirs(os.path.join('data',b))
                except Exception as e:
                    print e
            else:
                path = os.path.join('data',b)
                files = os.path.join(path,str(j['id'])+'.jpg')
                data= requests.get(j['wp']).content
                f = open(files,'ab')
                f.write(data)
                f.close
def start(name,idid):
    c = 0
    for i in idid:
        page = 30
        url = 'http://service.picasso.adesk.com/v1/wallpaper/category/'+i+'/wallpaper?limit=30&skip='+str(page)+'&adult=false&first=0&order=new'
        b= name[c]
        c = c+1
        for aa in xrange(166):
            aa+=1
            print aa
            url = 'http://service.picasso.adesk.com/v1/wallpaper/category/'+i+'/wallpaper?limit=30&skip='+str(page)+'&adult=false&first=0&order=new'
            html = json.loads(requests.get(url).content)
            dis =html['res']['wallpaper']
            page+=30
            for j in dis:
                yield j['wp'],j['id'],b
def downpic(url,idid,b): 
    if not os.path.exists(os.path.join('data',b)):
        try:
            os.makedirs(os.path.join('data',b))
        except Exception as e:
            pass
    else:
        path = os.path.join('data',b)
        files = os.path.join(path,idid+'.jpg')
        data= requests.get(url).content
        f = open(files,'ab')
        f.write(data)
        f.close

if __name__=='__main__':
    name,idid = pre()
    firstpage(idid,name)
    urls = start(name,idid)
    pool=Pool(processes=8)
    for i,j,k in urls:
        pool.apply_async(downpic,(i,j,k, ))
    pool.close()
    pool.join()
    
        
        


    
    
