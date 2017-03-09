# encoding:utf-8
from bs4 import BeautifulSoup
import re
import urllib.parse , os
import urllib.request


while 1:
    word = input("(q退出)输入关键字：")
    if word == '':
        continue
    if word == 'q':
        break
    
    url = "http://baike.baidu.com/search/word?word="
    word = urllib.parse.quote(word)
    request = url + word
    res = urllib.request.urlopen(request)    
    html =res.read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')     
    node = soup.find('div', class_="lemma-summary")
    if node == None:
        print("没有该词条")
        pass
    else:
        data = node.get_text(strip=True)
        print(data)

    
    


