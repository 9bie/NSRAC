# NSRAC 百度网盘自动转存
## 如何使用

执行`pip install -r requirements.txt` 安装所需依赖。

之后
```python
import nsrac
baidu = nsrac.BaiduPan(Cookies={
    #如果你有cookies的话，请在这里添加BDUSS,STOKEN和BAIDUID，否则请留空
})
#如果Cookies留空，请使用如下调用(还未实现)
#baidu.login(user,passwd)

baidu.transfer("https://pan.baidu.com/s/xxxxx",code="")
```

## 注意
务必保证js.js和nsrac在同一个目录下

## python2?

理论上支持，没试过