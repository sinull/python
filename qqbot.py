#encoding:utf-8
from qqbot import QQBot
import urllib2
import json

myqqbot = QQBot()
def getHtml(url):  
    page = urllib2.urlopen(url)  
    html = page.read().decode('utf-8')
    return html

@myqqbot.On('qqmessage')
def handler(bot, message):
    
        
    key = '34afd60af5564e4281073b0faba070fc'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    word= message.content
    print message.contact.ctype
        
    request = api + word

    response = getHtml(request)  
    dic_json = json.loads(response)
    b = dic_json['text']
    c = b.encode('utf-8')

    if message.contact.ctype=='buddy':
        bot.SendTo(message.contact,c)
    

myqqbot.LoginAndRun()
