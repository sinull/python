# encoding:utf-8
import os, urllib2, requests, gzip
from StringIO import StringIO
from bs4 import BeautifulSoup
req_header = {
    'User-Agent': 'Mozilla/4.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) '
                  'Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
    'Referer': None  
}
def get_html(url):
    req = urllib2.Request(url=url, headers=req_header)
    res = urllib2.urlopen(req, timeout=5)
    html = res.read()
    print 'Content-Encoding :', res.info().get('Content-Encoding')
    if res.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(html)
        f = gzip.GzipFile(fileobj=buf)
        html = f.read()
    return html   
def get_imglink2(html_text): 
    bs = BeautifulSoup(html_text, 'html.parser', from_encoding='utf-8')
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
        print local
        try:
            with open(local, 'wb') as jpg:
                jpg.write(requests.get('http:'+imgurl, stream=True, headers=req_header).content)
        except requests.RequestException,e:
            print e
if __name__ == '__main__':
    for num in range(2000):
        html = get_html('http://jandan.net/ooxx/page-%s#comments' % str(2338 - num))
        imgs = get_imglink2(html)
        get_img2(imgs, u'图')
    print u'图片共：', len(imgs)
    
