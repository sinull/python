import urllib.request  
import urllib.parse  
import json
import json
import time
import random
import hashlib
print("按q退出")
while 1 :
    content = input("翻译:")
    if content == '':
        continue
    if  content == 'q' :  
        break
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'  
    head = {}  
    head[ 'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'  

    u = 'fanyideskweb'
    d = content
    f = str(int(time.time()*1000) + random.randint(1,10))
    c = 'rY0D^0\'nM0}g5Mm1z%1G4'
    sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()
    data = {}
    data['i'] = content
    data['client'] = 'fanyideskweb'
    data['salt'] = f
    data['sign'] = sign
    
    data = urllib.parse.urlencode(data).encode('utf-8')  
    req = urllib.request.Request(url,data,head)
    try:
        
        response = urllib.request.urlopen(req)  

        html = response.read().decode('utf-8')  
      
        target = json.loads(html)

        print("结果：%s" %(target['translateResult'][0]))

    except:
        print ('error')
