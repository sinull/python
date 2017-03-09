# encoding:utf-8
import os, urllib, re, urllib2, requests, gzip , time
from StringIO import StringIO
from bs4 import BeautifulSoup
req_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Host': 'www.mmonly.cc',
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
        imglist.append(link.get('original'))
    return imglist
def get_img2(imgs,path):
    dirname = './%s' %path
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for imgurl in imgs:
        if imgurl == None:
            pass
        else:
            name = imgurl.split('/')[-1]
            timename = str(time.time())
            filename = timename+name
            print filename
            print imgurl
            local = os.path.join(dirname, filename)
            try:
                with open(local,'wb') as png:
                    png.write(requests.get(imgurl).content)
            except requests.RequestException,e:
                print e
if __name__ == '__main__':
    print('www.mmonly.cc')
    site = input(u'输入网址，并格式化页码：')
    name = raw_input(u'输入文件名:')
    for num in range(1,100):
        html = get_html(site %str(num))
        imgs = get_imglink2(html)
        get_img2(imgs,name)
        print u'图片共：', len(imgs)
