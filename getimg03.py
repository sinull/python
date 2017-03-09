# encoding:utf-8
import os,urllib.request,gzip,requests
from io import StringIO
from bs4 import BeautifulSoup
import urllib.parse
head = {}  
head[ 'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

def get_html(url):
    data = {
    'Accept': 'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
    'Referer': None  
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data, head)
    res = urllib.request.urlopen(req, timeout=5)
    html = res.read().decode('utf-8')
    print ('在为你悄悄地保存一波图')
    return html

def get_imglink2(html_text): 
    bs = BeautifulSoup(html_text, 'html.parser')
    links = bs.find_all('img')
    imglist = []
    for link in links:
        imglist.append(link.get('src'))
    return imglist 
def get_img2(imgs, path): 
    dirname = './%s' % path
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for imgurl in imgs:
        filename = imgurl.split('/')[-1]
        local = os.path.join(dirname, filename)
        print (local)
        try:
            with open(local, 'wb') as jpg:
                jpg.write(requests.get('http:'+imgurl, stream=True, headers=head).content)
        except requests.RequestException:
            print ('error')
if __name__ == '__main__':
    for num in range(2000):
        html = get_html('http://jandan.net/ooxx/page-%s#comments' % str(2338 - num))
        imgs = get_imglink2(html)
        get_img2(imgs, u'图')
    print (u'图片共：', len(imgs))
    
