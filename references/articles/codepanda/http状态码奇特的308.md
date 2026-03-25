# http状态码奇特的308

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXCUFjvfyaUwluGYLOoKQ2iaRiadDH5icLmWN9gZna9HLGccCGTrKGaEOBS2oUhBchDhTZFPfrFYhIcZw/0?wx_fmt=jpeg)

#  http状态码-奇特的308

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年06月15日 10:21_ __ _ _ _ _

开篇

最近在做站点升级，http统一切https的时候，在前置机配置redirect的80的http
到443的https的时候，沿用原来的状态码301，发现了一个奇特的现象，参数全部都丢失，然后去后端机器上，跟进access日志，发现post请求都变成了get请求，所以导致post的入参都丢失。然后跟进了一下，发现了一个http
status code码的有趣问题。301跟302是最多被提及跟面试会问的，但是很少有人关注307跟308的状态码。

概览

http status code：

301 永久调整 302 临时跳转

308 永久跳转 307 临时跳转

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCUFjvfyaUwluGYLOoKQ2iaRFaiaQ0iaibPNejuPryeLtHNbw5micqNwFoOVibgIfDsBjyS1q7SaRWmUZjA/640?wx_fmt=png)

这其实是两组http status code，301配套的302状态码，主要是区分永久跟临时跳转。

301应该是用于原域名彻底不再维护的情况下，302应该是用于原目标站点处于维护升级的场景下。

与之对应的是另外一组308跟307的相互配套的状态码。308跟301状态码，几乎一模一样，唯一的区别就是，在301状态码在nginx前置代理机的代理跳转的时候，会把POST请求，转成GET请求。

解决http升级https

所以这里再做网站http的升级https的时候，需要注意redirect重定向的的http status
code的选择。最好是选择307跟308这一组的状态码。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCUFjvfyaUwluGYLOoKQ2iaRJp5rg1sABiboupQNZ6ZnyQaSMcSHFiag71pb9SU91icBHia4I2YRQsTFQQ/640?wx_fmt=png)

番外

从RFC的文档解释来看，貌似是308是后定义的，而且应该是属于当时错漏。所以308对应的永久性的跳转。英文不太好，凑合着自我理解。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCUFjvfyaUwluGYLOoKQ2iaRjQDibwmcMFcwTxCNxOWh6Rgh3q9rlwLz7VOMptILzfuQShxUTlDXjQA/640?wx_fmt=png)

感兴趣的，英语优秀的可以自我去探究。

参考资料：

https://datatracker.ietf.org/doc/html/rfc7538#page-2

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXCUFjvfyaUwluGYLOoKQ2iaRPdqnXKgTUnDKW6gaNSiaklcyTQInEA6Im3MIL7WCHDmOubPI4wia3Ybw/640?wx_fmt=jpeg)

关注该公众号

使用小程序

****

****

****

×  分析

__

![作者头像](http://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBgiark9DSndLEbkHAncxsR0lzDOfllKSZtbGTHWiaBibsQl2ia0dhK0JRFibXneWtbqk14THQSTUILsnA/0?wx_fmt=png)

可打开此内容，
使用完整服务

：  ，  ，  ，  ，  ，  ，  ，  ，  ，  ，  ，  ，  。  视频  小程序  赞  ，轻点两下取消赞  在看  ，轻点两下取消在看
分享  留言  收藏  听过