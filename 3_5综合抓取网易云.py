import json

import requests
from lxml import etree
from Crypto.Cipher import AES
from base64 import b64encode
url="https://music.163.com/weapi/comment/resource/comments/get?csrf_token="

#请求方式是post

dat={
"csrf_token": "",
"cursor": "-1",
"offset": "0",
"orderType": "1",
"pageNo": "1",
"pageSize": "20",
"rid": "R_SO_4_1325905146",
"threadId": "R_SO_4_1325905146"
}

#处理加密过程windows.asrsea
'''
 function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {   d:数据   e:010001  f:很长 g:较长
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
'''
f='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g='0CoJUm6Qyw8W8jud'
e='010001'
i="ASduLDdUhy0jdvaV"
encSecKey="623b2c811c97afda853600feff682a80699ff16d7476521fb75d8910a470c86b9c7c47cd36961984cc49bd76004845552f61ac8ffcf09746ccfcc9c287163cfc382a098b51b96e44a84401e8a0f1aec9debb150ff5a731b15b7f5e59ceca644bf57de5005021785a6dfdca68a4c6f1536959da6c179d00cf8ee17e2cdeeba54b"
def get_encSecKey():
    return "6479a44d496f69af024fe34ec6400d3dd4dce1038c706456c45a4e206900d5411cbe52dc0a06240370d4400eaf7b9c3a48bf5c530020d597e9db137ba02dd55dbc75534647a24d6a4224d19ae33f487141311f0bf1a0aa014ec9cbdae355aa4ed0a966c05f69fd1a5ebec6dd6efe034d23ab5e27813b8a7ca37fd42b2bfde3b6"


def get_params(data):
    first=enc_params(data,g)
    second=enc_params(first,i)
    return second

def to_16(data):
    pad=16-len(data)%16
    data+=chr(pad)*pad
    return data

def enc_params(data,key):
    iv="0102030405060708"
    data=to_16(data)
    aes=AES.new(key=key.encode('utf-8'),IV=iv.encode('utf-8'),mode=AES.MODE_CBC)
    bs=aes.encrypt(data.encode("utf-8"))
    return str(b64encode(bs),"utf-8")

resp=requests.post(url,data={
    "params":get_params(json.dumps(dat)),
    "encSecKey":get_encSecKey()
})

print(resp.text)


resp.close()