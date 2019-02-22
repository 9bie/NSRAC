#coding:utf-8
import requests
import execjs
import json
import time
def string_middle(start_str, end, html):
    try:
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return html[start:end].strip()
    except:
        return None
class BaiduPan(object):
    def __init__(self,Cookies=None):
        self.logind=False
        self.w = requests.session()
        self.headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-HK,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6,zh-TW;q=0.5,en-US;q=0.4,en;q=0.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        }
        self.Cookies = Cookies
        if Cookies:
            self.__verifyIsLogin()


        self.share_verify_api="https://pan.baidu.com/share/verify?surl=%s&t=%s&channel=chunlei&web=1&app_id=250528&bdstoken=%s&logid=%s=&clienttype=0"
    def __getLogid(self):
        jsfunc='''var i = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/~£¡@#£¤%¡­¡­&", a = String.fromCharCode,o = function (e){if (e.length < 2) {var r = e.charCodeAt(0);return 128 > r ? e : 2048 > r ? a(192 | r >>> 6) + a(128 | 63 & r) : a(224 | r >>> 12 & 15) + a(128 | r >>> 6 & 63) + a(128 | 63 & r)}var r = 65536 + 1024 * (e.charCodeAt(0) - 55296) + (e.charCodeAt(1) - 56320);return a(240 | r >>> 18 & 7) + a(128 | r >>> 12 & 63)+ a(128 | r >>> 6 & 63) + a(128 | 63 & r)},u = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g, c = function (e){return (e +""+Math.random()).replace(u, o)}, l = function (e) {var r = [0, 2, 1][e.length % 3],t = e.charCodeAt(0) << 16 | (e.length > 1 ? e.charCodeAt(1) : 0) << 8 | (e.length > 2 ? e.charCodeAt(2) : 0),n = [i.charAt(t >>> 18), i.charAt(t >>> 12 & 63), r >= 2 ? "=" : i.charAt(t >>> 6 & 63), r >= 1 ? "=" : i.charAt(63 & t)];return n.join("")}, p = function (e) {return e.replace(/[\s\S]{1,3}/g, l)}, d = function () {return p(c((new Date).getTime()))}, g = function (e, r) {return r ? d(String(e)).replace(/[+\/]/g, function (e) {return "+" == e ? "-" : "_"}).replace(/=/g, "") : d(String(e))};'''
        ctx = execjs.compile(jsfunc)
        return ctx.call('g',"baiduid")
    def __verifyIsLogin(self):
        self.logind=True
        # gugugu~
    def login(self,user,passwd):
        pass
    def __getBdstoken(self,source):
        # source = self.w.get(link,headers=self.headers,cookies=self.Cookies).text
        return string_middle('bdstoken":"','"',source)
    def transfer(self,bdlink,code=None):
        obj = self.w.get(bdlink,headers=self.headers,cookies=self.Cookies)
        bdstoken = self.__getBdstoken(source=obj.text)
        if obj.status_code == 302 and not code:
            print("Need Code.")
            return False
        else:
            if not bdstoken:
                print("Get bdstoken Failed.")
                return False
            surl = bdlink[bdlink.find("s/1")+3:]
            result = self.w.get(self.share_verify_api%(surl,int(time.time()),bdstoken,self.__getLogid()))
            r2 = json.loads(result)
            if "randsk" not in r2:
                print("Get Randsk Faild.")
                return False
            self.Cookies["SCRC"] = r2["randsk"]
            # Verify Sussfully