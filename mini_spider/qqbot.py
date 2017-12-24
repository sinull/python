#encoding:utf-8

#python2.7

import urllib2
import json


def getHtml(url):  
    page = urllib2.urlopen(url)  
    html = page.read().decode('utf-8')
    return html

def onQQMessage(bot, contact, member, content):
    
    key = '34afd60af5564e4281073b0faba070fc'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='  
    request = api + content
    response = getHtml(request)  
    dic_json = json.loads(response)
    b = dic_json['text']
    c = b.encode('utf-8')
    bot.SendTo(contact,c)
    


