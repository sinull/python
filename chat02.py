# -*- coding: utf-8 -*-  
import urllib2
import json

import itchat
  
def getHtml(url):  
    page = urllib2.urlopen(url)  
    html = page.read().decode('utf-8')
    return html  
  
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    key = '34afd60af5564e4281073b0faba070fc'  
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    
    word= msg['Text'].encode('utf-8')

    
    request = api + word 
    response = getHtml(request)  
    dic_json = json.loads(response)  
    return (dic_json['text'])



itchat.auto_login(enableCmdQR=1)
itchat.run()
