# -*- coding: utf-8 -*-  
import urllib.request 
import json
import urllib.parse
import itchat
  
def getHtml(url):  
    page = urllib.request.urlopen(url)  
    html = page.read().decode('utf-8')
    return html  
  
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    key = '34afd60af5564e4281073b0faba070fc'  
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    
    word= msg['Text']

    wordd = urllib.parse.quote(word)
    request = api + wordd  
    response = getHtml(request)  
    dic_json = json.loads(response)  
    return (dic_json['text'])



itchat.auto_login(enableCmdQR=1)
itchat.run()
