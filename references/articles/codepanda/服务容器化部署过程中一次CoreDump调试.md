# 服务容器化部署过程中一次CoreDump调试

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXDrbLhyq5KeDpzWs3hWH7ibFm8ibjWTo1Uk7ggtCJafic2sogsqTS1oxW98icnqFC4yP695ygZA1icrjMA/0?wx_fmt=jpeg)

#  服务容器化部署过程中一次CoreDump调试

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年03月31日 14:44_ __ _ _ _ _

最近都在集体服务部署容器化，在实体机上采取容器化部署项目。在此记录一下无意中发现的core dump的程序调试过程。

迁移服务部署，一件很简单的事。部署代码，发布。在前置机对url请求进行容器网关的转发，在容器配置nginx解析。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXDrbLhyq5KeDpzWs3hWH7ibFYdu1O7ic4NXVR6cKLMHb2rJqaegTYYF636lmaLic08zMHmlgDTK8Mwmg/640?wx_fmt=png)

前置机，是做的主从互活的配置。所以这里为了不影响线上正常的服务，这里都在前置机的备机上进行转发配置。所以需要在本地绑定一下hosts进行校验。

想着一次过，简单完事。结果一坑到底。发现一直500错误。服务根本打不进来。然后发现根本没有业务日志进来。紧接着去nginx的访问日志，都是500的日志。

懵逼中，想着执行一下php -v 看一下版本是否影响。结果直接core
dump中断。看来问题就在这里，程序中断了。问题是产生了一堆的core文件，而core文件，都是可elk可执行文件。无法通过cat
或者vim这种编辑器，直接以文本打开的形式查看。

赶紧百度一下core dump的定义，以及core文件的分析定位。简单来说，core
dump是当运行的程序，发生了非预期的中断退出，Linux系统对当前的堆栈区的一个快照现场保存。可以供coder进行错误调试定位。然后再百度一下，通过GDB可对执行文件进行分析。然，容器并没有GDB环境~安装，通过apt-
update, 再apt-install GDB,一路Yes Yes就完事。

好，GDB安装完毕。至此杀猪环境准备完成，准备杀猪。再次执行php -m，
依旧看到错误，同时在当前目录生成了core文件。然后赶紧按图索骥，照猫画虎。用GDB来杀猪core文件，如下：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXDrbLhyq5KeDpzWs3hWH7ibFQ0zVRvaOMZ81YCnpLr9RGfAFy3ibp4JMZc86vEBanOeGsA1TZYAOJnA/640?wx_fmt=png)

可以明确看到，php程序在加载phalcon的拓展的时候，异常中断退出。

所以暂且问题可以定位于此，当前php版本应该跟phalcon应该是不兼容。横向对比线上实体服务器上的php版本跟phalcon的版本如下：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXDrbLhyq5KeDpzWs3hWH7ibF2f7cnlnPV8eQmn66VIrOVa9q9a8Hiavao23eWtibcqkvH8fJU1QIoZKg/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXDrbLhyq5KeDpzWs3hWH7ibFyHicg9LtTlqotibAtBr5Zn8WUnjwZjicUKf51fC1OO7sg3xkhm29Yb0QA/640?wx_fmt=png)

先移除容器的里面phalcon的拓展，不对其进行加载。php启动正常。查看容器的php版本如下：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXDrbLhyq5KeDpzWs3hWH7ibF435xSCoEqSpaqCLqzHzUjFMZ2UdRbsGIv178GZMniceZVsajFUTwxaw/640?wx_fmt=png)

最后根据运维的解释：容器那台机器，并不是php版本跟phalcon不兼容，是因为那台机器比较老，cpu指令集不兼容优化下的phaclon版本。不明觉厉~同时在容器换了一台物理机，搭载php跟phalcon，都运行正常。如下：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXDrbLhyq5KeDpzWs3hWH7ibF5udxQpP4Miba3EndVRO2EuJOicO20cwwib4iapw8RVymwDu9PFoFk2qLbw/640?wx_fmt=png)

参考资料：

*

https://blog.csdn.net/ydyang1126/article/details/51769010

[ 为啥这个视频播放量突然增高了？
](http://mp.weixin.qq.com/s?__biz=MzA5NTc2NzcxOA==&mid=2448038564&idx=1&sn=d0209b78d83e439b725edae70db8cca0&chksm=84a4e76db3d36e7be27187e8f9d9fc25b7a15a3e04ac9817b1dcb89215c328e372f2664c11b4&scene=21#wechat_redirect)

在没有任何推广之下，居然超过了所有关注我的人数。真的是奇怪，费解。

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