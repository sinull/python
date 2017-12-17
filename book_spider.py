#encoding: utf-8
#python2 

import urllib2 ,os ,requests,gzip ,re,urllib
from StringIO import StringIO
from bs4 import BeautifulSoup
import string ,time

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
    }

def gethtml(url):
    try:
        
        req = urllib2.Request(url= url,headers = head)
        res = urllib2.urlopen(req,timeout = 15)
        html = res.read()
        if res.info().get('Content-Encoding')== 'gzip':
            buf = StringIO(html)
            f = gzip.GzipFile(fileobj=buf)
            html = f.read()
        return html
    except:
        print 'error'


def paser(html):
    try:
        pattern = re.compile('<a.*?href=(.*)title=".*?">Txt')
        thing = re.findall(pattern,html)
    
        
        bb= thing[0]
        cc=  bb[1:-2]
        bb = urllib.quote(cc, safe=string.printable)
        return bb
    except:
        print 'error'
    
    
def get_img2(imgs): 
    dirname = './book'
    
    if not os.path.exists(dirname):
    
        os.makedirs(dirname)
    filename = urllib.unquote(imgs).decode('utf8').split('/')[-1] 
    local = os.path.join(dirname, filename)
    print local
    try:
        with open(local, 'wb') as jpg:
            jpg.write(requests.get(imgs, stream=True, headers=head).content)
    except requests.RequestException,e:
        print e

if __name__=='__main__':
    for i in range(36807):
        html = gethtml('https://www.qisuu.com/%s.html' %str(36807-i))
        url = paser(html)
        try:
            
            get_img2(url)
        except:
            print 'error'
  
        
        
        
        
        
    
