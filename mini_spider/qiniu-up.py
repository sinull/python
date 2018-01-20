#coding:utf-8

from qiniu import Auth,put_file,etag, urlsafe_base64_encode
import qiniu.config
import os

###需要填写你的 Access Key 和 Secret Key
access_key = 'tvcLj9EtEAROjnoeZQAu_dSz6cVJp11d8uZV9uAr'
secret_key = '2Niq_KZ8BKe4FxlltmljplHbOwvZHlLEZO6IBaAC'
#####构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'image'

def upload_qiniu(name):
    #上传到七牛后保存的文件名
    key = name
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    #要上传文件的本地路径
    localfile = name
    ret, info = put_file(token, key, localfile)
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

def list():
    dirs = os.path.dirname(os.path.realpath(__file__))     
    return (os.listdir(dirs))
        
    
if __name__=='__main__':
    a = list()
    for i in a:
        
        upload_qiniu(i)
        
