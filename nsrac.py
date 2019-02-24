#python3
#author: 9bie
#blog: http://9bie.org

#coding:utf-8
import requests
import execjs
import json
import time
#python3
# from urllib.parse import quote

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
        '''
        Cookies need STOKEN and BDUSS AND BAIDUID
        :param Cookies:
        '''
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

        if Cookies:
            self.w.cookies.update(Cookies)
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
    def __errnoList(self,errno):
        errno_list = {
            0: "成功",
        -1: "由于您分享了违反相关法律法规的文件，分享功能已被禁用，之前分享出去的文件不受影响。",
        -2: "用户不存在请刷新页面后重试",
        -3: "文件不存在请刷新页面后重试",
        -4: "登录信息有误，请重新登录试试",
        -5: "登录信息有误，请重新登录试试",
        -6: "请重新登录",
        -7: "该分享已删除或已取消",
        -8: "该分享已经过期",
        -9: "访问密码错误",
        -10: "分享外链已经达到最大上限100000条，不能再次分享",
        -11: "验证cookie无效",
        -14: "对不起，短信分享每天限制20条，你今天已经分享完，请明天再来分享吧！",
        -15: "对不起，邮件分享每天限制20封，你今天已经分享完，请明天再来分享吧！",
        -16: "对不起，该文件已经限制分享！",
        -17: "文件分享超过限制",
        -19: "验证码输入错误，请重试",
        -20: "请求验证码失败，请重试",
        -21: "未绑定手机或邮箱，没有权限私密分享",
        -22: "被分享的文件无法重命名，移动等操作",
        -30: "文件已存在",
        -31: "文件保存失败",
        -32: "你的空间不足了哟，赶紧购买空间吧",
        -33: "一次支持操作999个，减点试试吧",
        -40: "热门推荐失败",
        -60: "相关推荐数据异常",
        -62: "密码输入次数达到上限",
        -64: "描述包含敏感词",
        -70: "你分享的文件中包含病毒或疑似病毒，为了你和他人的数据安全，换个文件分享吧",
        1: "服务器错误",
        2: "参数错误",
        3: "未登录或帐号无效",
        4: "存储好像出问题了，请稍候再试",
        12: "批量处理错误",
        14: "网络错误，请稍候重试",
        15: "操作失败，请稍候重试",
        16: "网络错误，请稍候重试",
        105: "创建链接失败，请重试",
        106: "文件读取失败，请页面后重试",
        108: "文件名有敏感词，优化一下吧",
        110: "您今天分享太多了，24小时后再试吧",
        111: "外链转存失败，请稍候重试",
        112: "页面已过期，请刷新后重试",
        113: "外链签名有误",
        114: "当前任务不存在，保存失败",
        115: "该文件禁止分享",
        116: "分享不存在",
        117: "分享已经过期",
        2126: "文件名中含有敏感词",
        2135: "对方拒绝接收消息",
        2102: "群组不存在",
        2103: "你已退出该群",
        9100: "你的帐号存在违规行为，已被冻结",
        9200: "你的帐号存在违规行为，已被冻结",
        9300: "你的帐号存在违规行为，该功能暂被冻结",
        9400: "你的帐号异常，需验证后才能使用该功能",
        9500: "您的帐号存在安全风险，已进入保护模式，请修改密码后使用",
        }
        if errno not in errno_list:
            return False,"未知错误"
        else:
            return True,errno_list[errno]
    def __getLogid(self):
        jsfunc = open("js.js","r")
        ctx = execjs.compile(jsfunc.read())
        jsfunc.close()
        return ctx.call('g',"baiduid")
    def __verifyIsLogin(self):
        ret = self.w.get("https://passport.baidu.com/center")
        if "修改头像".encode("utf-8") not in ret.content:
            print("登陆失败，请检查Cookies或者使用Login方法登陆。")
        else:
            self.logind=True
        # gugugu~
    def login(self,user,passwd):
        # 还未完成
        self.w.get("https://pan.baidu.com/")
        login_url = "https://passport.baidu.com/v2/api/?login"
        token_url = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"

        postData={
            "staticpage":"http://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html",
            "charset":"utf-8",
            "token":self.__getLogintoken(self.w.get(token_url).text),
            "tpl":"netdisk",
            "apiver":"v3",
            "tt":int(time.time()),
            "codestring":"",
            "safeflg":"0",
            "u":"http://pan.baidu.com",
            "isPhone":"false",
            "quick_user":"0",
            "loginmerge":"true",
            "logintype":"basicLogin",
            "username":user,
            "password":passwd,
            "verifycode":"",
            "mem_pass":"on",
            "ppui_logintime":"49586",
            "callback":"parent.bd__pcbs__hksq59"
        }
        self.w.headers.update({"referer":"https://pan.baidu.com"})
        r = self.w.post(login_url,postData)
        print(r.text)
    def __getLogintoken(self,source): return string_middle("login_token='","';",source)
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
        # data = {
        #     "fsidlist": [int(fsidlist)],
        #     "path": '/'
        # }
        result = self.w.post(self.transfer_api%(shareid,formid,bdstoken,logid),data="fsidlist=%5B"+fsidlist+"%5D&path=%2F")
        r2 = json.loads(result.text)
        if "errno" not in r2:
            print("Unknow Error.")
            print(result.text)
            return False
        else:
            ok,msg = self.__errnoList(r2["errno"])
            if ok:
                print(msg)
            else:
                print(msg)
                print(result.text)
if __name__=="__main__":
    a = BaiduPan({
        "BAIDUID":"F8FD5DB49833DA95FC8EDB8B22092848:FG=1",
        "BDUSS":"FRYTXFQaGowUjVBcmRmVWNBV1hLUVU2M09YcnVYZkw0Rkt3eXRjUW1aM35hbEJjQVFBQUFBJCQAAAAAAAAAAAEAAACAhFIh49~R7gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP~dKFz~3Shce",
        "STOKEN":"1136cd700f7005b14425121c233138466ead1163bb2c143c3a61e49214ce7e1c"
    })
    a.transfer("https://pan.baidu.com/s/1xJ-A651ih8SQFxvZJRkBMQ",code="59n8")
