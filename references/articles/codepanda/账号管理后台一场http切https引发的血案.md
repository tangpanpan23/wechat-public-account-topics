# 账号管理后台一场http切https引发的血案

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKBFOdiclTHRcFZvm4BQTXV78bibDR72YCrEiacueOvL9RDsdQf0jhWGjCg/0?wx_fmt=jpeg)

#  账号管理后台--一场http切https引发的血案

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年03月07日 12:57_ __ _ _ _ _

**前言：**

本着先把自己折腾明白，同时能够让每个人能感同身受。这里不去扯什么深度原理跟底层，也不想去官网摘抄一堆的原理图跟完全正确的废话过来。只想通过自己实实在在的经历，把每个地方遇到的坑以及遇到坑之后第一时间想法，甚至是偷懒、投机取巧、错误的想法。所有的追查之路给总结出来，警示自己也希望给后来人能够少踩坑。

大的背景：
响应集团安全号召，对目前的手头的项目http切https。
目前账号管理后台的服务架构：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKia68A72daHFqFGsu8twCumED1LWOR6Y5w4HF1se3PdDY3TfMGibwSdYg/640?wx_fmt=png)


带字幕的过程：
这个入门的后端开发的基本功，nginx服务器配置，反向代理负载均衡。
本想着根据现有的服务部署架构，只需要对客户端80端口http请求，做一次永久的重定向301到https就行。简单做一次nginx反向代理的https转发，保证客户端交互的是ssl的安全的请求。后端服务不用关心，项目代码也不用做任何调整、依旧维持原状即可。

说干就干：

*   *   *   *   *

server{        listen 80;        server_name account.zhiyinlou.com;        return 301 https://$server_name$request_uri;  }

然后，在443端口，配置对应的证书就完事。做upstream负载。

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

server {        listen       443 ssl;        server_name account.zhiyinlou.com;
ssl_certificate XX.pem;        ssl_certificate_key XX.key;
location / {             proxy_set_header   Host $host:$server_port; #设置当前的域跟端口             proxy_set_header   X-Real-IP $remote_addr;  #设置真正的客户端的ip地址             proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;  #将所有的转发层层的客户端信息header设置过去             proxy_pass http:account.zhiyinlou;        }

upstrem  account.zhiyinlou{          server 10.xx.xx.1:80;          server 10.xx.xx.2:80;          server 10.xx.xx.3:80;          server 10.xx.xx.4:80;   }

最后在真正的后端服务机上，仍然是监听80端口，处理proxy代理过来的请求，还是按照之前正常配置就行，不需要做任何修改。在nginx反向代理机配置完，reload
nginx代理机服务，输入域名account.zhiyinlou.com。然后出现标题所述的血案。

有图有真相：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKrdB5dhIKscu7YCBUswaUUkAoZUIjI02U6yy0F9Ao7qKxZNNFmu11ag/640?wx_fmt=png)

踩坑之路开始表演：

从浏览器展示问题：可以明确看到错误提示，是http请求，打到https端口。所以服务器报错。

解决问题也很简单，赶紧百度找答案：

得到两条答案 1、 建议使用https:// 2、 在后端监听的443端口 将ssl去掉
关于1的建议，我当前就是使用https请求。关于2的建议，在nginx配置做了一次尝试，没有任何效果。方向错误。

百度看来不能简单的解决我的问题，只能开始冷静下来分析请求过程。从浏览器的请求过程来分析：

http-> https -> admin(首页跳转 redirect) ->sso登录校验（报错~）

如图：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUK1hRxtgR2mI6avzS5Ls37x0iafruplL4EhicS3zjxh2DN0xMr3UFiaO1Fw/640?wx_fmt=png)

分析整个url过程：

1、输入http域名地址，在反向代理机器做一次重定向 到https 符合预期。

2、https地址，去找admin 首页地址路由，代码路由转发到了服务后端。符合预期。

3、这里存在代码逻辑验证，没有sso登录的，会redirect() 登录页面~但是这里响应的host, 通过代理设置proxy_set_header
Host $host:$server_port 带了端口443。

猜测：

nginx反向代理机，在header设置的传递参数的时候，port影响到了后端实际项目的端口号。于是将nginx中的$server_port给取消。只传host到服务端。proxy_set_header
Host $host.

验证过程：在前端失去443端口的干扰后，跳转顺利。如预期。

如图：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKpYSbaQyc968aWEAEWVlibWsbiadKBiaibGM8L0doPK8yicrBueYiatibr18xg/640?wx_fmt=png)

随即出现新问题，1、在前端使用asset生成加载地址时候报错~而且依旧看到是http协议，前端样式无法加载。2、同时在redirect时候，依旧是http经过做了一次代理的https的重定向。所以还是存在问题。

如图：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKyTeXUO1Q0afctG5k5NUbDdFEN8DQMJ2TiafrMdiaD9d4X3do4h71J3vg/640?wx_fmt=png)

根据新问题做第三次分析，猜测后端的scheme存在问题导致。

所以尝试在nginx反向代理机上，加上scheme的配置。proxy_set_header X-Forwarded-Proto
$scheme;同样还是无效。

最后开始分析猜测，是不是因为真正的提供后端服务依旧是80端口导致？

项目本身获取到的scheme仍然是当前项目的80端口的非安全模式？

开始追laravel框架生成url源码的地方，生成的url以及重定向redirect权重顺序据第一设置了安全地址，其次是scheme，最后是根据当前host来。默认是http！

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKEW6CC4bWH6hMVgDrFqvUU5npmlYicYo357a7fYib8gVYlIgFnTLL0zzA/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUK4MALibDiblqI3zwW3odNWmCXAmQOQEs21YnR7eKISNwnL6XeYNCtnyYQ/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKRkibYj6ic9m6FFicHSvfKCic7B3CzblxfTHDXYoPEdjz69LrhUf9F6DRyg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKf44wlYcYDUSBSLdgxU417efVoLFMvib1jjJv7ibgdUokNfwGOlZHUjOQ/640?wx_fmt=png)

于是在项目代码里面尝试获取当前的scheme、port、host、  secure字段值来佐证猜想如图：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKKicTP2obdSQ9TYjiaCnu0Hwe5THj6Ek76Qh0MLIBXhA8wCbtUicicKFSjg/640?wx_fmt=png)

可以看到源码里面，生成url的规则顺序，如果是完整的地址，直接返回完整url路径地址。否则先判断是否开启了secure模式，会强制转成https，（redirect、asset都有对应的参数可显示控制~）、最后按照scheme来获取。而从获取的结果来看，scheme、secure不会跟着当前浏览器的https而影响。而server_port确实从proxy_set_header带过来了。但是设置scheme从proxy_set_header转化失效。

解决办法：

在项目本身中，做调整。在容器初始化的时候，根据当前的配置的是否是https地址来判断，是否强制都走https。同时解决单纯生成http连接都需要经过nginx转发做跳转。同时兼容http环境。依赖env配置确定当前的首页的地址是http跟https来确定是否开启整站的https。

如图：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKnysrMYQGuAVUMwEjA56icQCAEyKGR8vlDbibW1Ls1O0Fdb2t6cLgyjrg/640?wx_fmt=png)

预发环境验证结果：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKhiaDjDUMrPa4NCyI02A7ZiaG1ubJ59jLr8H5qDTJ6riaxQTN8OXj5L5pA/640?wx_fmt=png)

结论：

反向代理机设置的头信息，其中scheme信息，如果后端实际的提供服务的端口不是443端口的话，是带不过去的。laravel项目依旧是以实际提供服务的服务器的信息为准获取到的scheme模式。但是server_port可以带过去。结合实际情况，需要对项目代码做一下调整。

参考资料：

http https的差别：

https://www.runoob.com/w3cnote/http-vs-https.html

nginx_proxy_header的配置：

http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_purge

laravel重定向redirect跟asset的源码分析:

https://learnku.com/articles/5590/laravel-http-the-use-and-source-analysis-of-
redirection

laravel解决https强制：

https://learnku.com/articles/4764/force-laravel-to-use-https

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