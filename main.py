#python3
#author: 9bie
#blog: http://9bie.org

#coding:utf-8
import requests
import execjs
import json
import time
#python3
from urllib.parse import quote

#python2
#import urllib
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
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "Accept-Language":"zh-HK,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6,zh-TW;q=0.5,en-US;q=0.4,en;q=0.3",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.w.headers.update(self.headers)
        self.w.cookies.update(Cookies)
        if Cookies:
            self.__verifyIsLogin()


        self.share_verify_api="https://pan.baidu.com/share/verify?surl=%s" \
                              "&t=%s" \
                              "&channel=chunlei" \
                              "&web=1" \
                              "&app_id=250528" \
                              "&bdstoken=%s" \
                              "&logid=%s" \
                              "&clienttype=0"
        self.transfer_api = "https://pan.baidu.com/share/transfer?shareid=%s" \
                            "&from=%s" \
                            "&channel=chunlei" \
                            "&ondup=newcopy"\
                            "&async=1"\
                            "&web=1" \
                            "&app_id=250528" \
                            "&bdstoken=%s" \
                            "&logid=%s" \
                            "&clienttype=0"
        self.report_user_api="https://pan.baidu.com/api/report/user?channel=chunlei&web=1&app_id=250528&bdstoken=%s" \
                             "&logid=%s" \
                             "&clienttype=0"
        self.memship_api="https://pan.baidu.com/rest/2.0/membership/user?method=query" \
                         "&reminder=1" \
                         "&channel=chunlei" \
                         "&web=1" \
                         "&app_id=250528" \
                         "&bdstoken=%s" \
                         "&logid=%s&clienttype=0"
        temp = "http://yun.baidu.com/share/transfer?shareid=%s&from=%s&bdstoken=%s&channel=chunlei&clienttype=0&web=1&app_id=250528"
    def __getLogid(self):
        jsfunc = open("js.js","r")
        ctx = execjs.compile(jsfunc.read())
        jsfunc.close()
        return ctx.call('g',"baiduid")
    def __verifyIsLogin(self):
        ret = self.w.get("https://passport.baidu.com/center")
        open("temp.html", "wb").write(ret.content)
        self.logind=True
        # gugugu~
    def login(self,user,passwd):
        pass
    def __getShareuk(self,source):return string_middle('"uk":',',',source)
    def __getFsidlist(self,source):return string_middle('"fs_id":',',',source)
    def __getBdstoken(self,source):return string_middle('bdstoken":"','"',source)
    def __getShareid(self,source):return string_middle('"shareid":',',',source)

    def transfer(self,bdlink,code=None,path="/"):
        if not self.logind:
            print("Please login.")
            return False
        obj = self.w.get(bdlink)
        logid =self.__getLogid()
        bdstoken = self.__getBdstoken(source=obj.text)
        if obj.status_code == 302 and not code or "请输入提取码".encode("utf-8") in obj.content and not code:
            print("Need Code.")
            return False
        elif "请输入提取码".encode("utf-8") in obj.content and code:
            if not bdstoken:
                print("Get bdstoken Failed.")
                return False
            surl = bdlink[bdlink.find("s/1")+3:]
            data = {
                "pwd" : code,
                "vcode" :"",
                "vcode_str":""
            }
            self.w.headers.update({"referer":obj.url})
            result = self.w.post(self.share_verify_api%(surl,(int(round(time.time() * 1000))),bdstoken,logid),data=data,
                                 )
            r2 = json.loads(result.text)
            if "randsk" not in r2:
                print("Get Randsk Faild.")
                print(result.text)
                return False
            self.w.cookies.update({"BDCLND":r2["randsk"]})

            # Verify Sussfully
        obj = self.w.get(bdlink)

        fsidlist=self.__getFsidlist(obj.text)
        shareid=self.__getShareid(obj.text)
        formid=self.__getShareuk(obj.text)
        self.w.get(self.memship_api%(bdstoken,logid))


        self.w.headers.update({"origin": "https://pan.baidu.com"})
        self.w.headers.update({"referer":bdlink})

        self.w.post(self.report_user_api%(bdstoken,logid),data={
            "timestamp":int(time.time()),
            "action":"share_transfer"
        })
        data = {
            "fsidlist": [int(fsidlist)],
            "path": '/'
        }
        print(data)
        result = self.w.post(self.transfer_api%(shareid,formid,bdstoken,logid),data="fsidlist=%5B"+fsidlist+"%5D&path=%2F")
        r2 = json.loads(result.text)
        if "errno" not in r2:
            print("Unknow Error.")
            print(result.text)
            return False
        else:
            if r2["errno"] == "0":
                print("Transfer Successfully")
                return True
            else:
                print("Transfer Faild.")
                print(result.text)
                return False
if __name__=="__main__":
    a = BaiduPan({
        "BAIDUID":":FG=1",
        "STOKEN":"",
        "BDUSS":"~~dKFz~3Shce",

    })
    a.transfer("https://pan.baidu.com/s/1vs78d9IvYDSs3WB3ixgCjA",code="uwoo")