from django.conf import settings
import hashlib

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8')) #利用配置文件中的SECRET_KEY作为加密函数的盐
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()