# go项目踩坑小霸王捉bug记

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPb2qlH4RFo4lwgdZwXucgbDdvaicM7jCZxv9HUiatuXkLAVkaP1TILgLIA/0?wx_fmt=jpeg)

#  go项目踩坑-小霸王捉bug记

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2022年03月16日 15:42_ __ _ _ _ _

**_ 现象：  _ **

将go项目build成可执行程序，直接执行该程序。所有请求访问都work，但是只要是通过supervisor
起来的该程序，就一直报错。成了一个黑盒。通过curl直接测试，都发现进去就直接是服务无响应。

手动执行的go可执行程序，然后再curl的结果：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPbDryG39guVehGqzibQADCNq8rfSSWTjCFvHK0sZgFDz3ibkPzlyjjLDug/640?wx_fmt=png)

通过supervisor执行的go可执行程序，curl的结果：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPbzSAXsz1ibMwX8WR5e8IticgRsqawg2RTniafUyic328QE3GQ5WlDyMIgZQ/640?wx_fmt=png)

开始猜测：

第一，直觉表示惊奇跟不可置信。supervisor只是一个守护程序而已。一直怀疑是可执行go程序本身的bug，然后重新强制编译，结果没用。

第二，supervisor应该是存在缓存导致。然后重新restart 包括stop 再start， reload conf还是依旧没用。

第三，可能supervisor起来的程序跟手动执行的程序，端口或者用户不同。通过lsof 对比两者起来的程序的端口占用以及用户都是root。几乎没有差异。

在此陷入僵局，时间也在这种不可思议中过去了两天~然后还是毫无头绪。

到此陷入死局，毫无头绪。于是开始写其他的需求，顺便修复其他的bug~

开始重新梳理思路，很明显可执行程序肯定是没有问题的。问题应该出在了代码本身。其他路由通过curl进来，可以正常响应，而这里是一个系统执行命令。通过路由，调用了系统命令
exec.Command。问题应该是出在这个系统调用上面。但是通过日志啥都看不到。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPbQYmYnUGD6QaT51JA1d2Gf5mBQmWOAvpxBNiaoGiawrSpLfY4ZFdu6ohw/640?wx_fmt=png)

必须要把错误日志给抓出来，要不然靠猜一切还是白搭。  于是从系统命令开始入手，如何将其中具体错误信息给get到。查阅资料，把原来的执行的调用方式
CombinedOutput()
改成，data.Run()，分别将Stdout、Stderr标准输出跟标准错误，给捕捉到，再抛出来。然后改代码，这里于是得到了三天以来，第一次具体的错误信息。看到具体的错误，问题就解决一大半了。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPbgTk77hs0xNWcmga3QorWlayOcToFDfP9SnoOgmNWNP51ic0YDlJ4DlQ/640?wx_fmt=png)

这里就能看到明显的错误提示，这里是告知缺少环境变量GOPATH，然后知道明显的错误，就可以按图索骥。配置对应的环境变量到supervisor的conf里面。
environment=GOPATH="/root/go",GOCACHE="/root/.cache/go-build"

直接在当前echo $GOPATH 居然为空~ 但是go env 查看当前的go 环境变量，却可以看到GOPATH的配置以及GOCACHE的配置。然后把go
env里面的配置到supervisor的conf中。重启supervisor 搞定。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPbuDPGY09Q3Eg7aas53n3tMUED4y7Ise0aKLVw01WoRiajocEEULa2FiaA/640?wx_fmt=png)

对go语言还不是太熟。不太理解go代码的依赖。然后对于这种go的包外系统调用，输出没有很好的了解跟选择。还是因为缺乏了解，所以选择上有些盲目，对于错误输出缺少明显的提示，于是陷入猜测的泥潭中。回到go语言的设计原则第一课，就是所有的错误都必须可控，不能有未知异常错误。这里就明显的忽略了这个。在没有明确的错误情况下，所有的猜测行为都是抓瞎。

下面聊聊，这几天的奇遇。周六在家出去买菜做饭，还一切好好的。然后周日再去买菜的时候，突然发现我的健康宝弹窗了~
也算是见识到了疫情之下，健康宝弹窗是个什么样子了。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPbobB3V9aOBBQ0Ntm3Herg0Y3TCM5YYticzxLxDWV9FicCJKpkrd2Ytcpw/640?wx_fmt=jpeg)

然后我懵逼了，简直是不知所措啊。不过正好，可以光明正大的响应国家居家办公的政策了。直接在家炒菜，吃饭，睡觉，写bug~也挺好~

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPbUSmVcgDxpeyznuYuetk7jfXPHicetgGX82sdOlfGib9FxwwCLibjFHjLA/640?wx_fmt=jpeg)

去社区找居委会，居委会大姐。上来就审问：近期出京去过哪里？去过哪个疫情风险地区？
本人一脸无辜的表示：我近期没有出过北京啊。大姐一脸嫌弃的说：你再好好想想，到底去过哪？要不然咋给你弹窗。2月份出过北京没？我再次懵逼的表示：在北京过年，过完年就上班。哪都没去。大姐还不死心的追问：你上次出京是啥时候？好好想想。在大姐的死亡追问之下，我作恍然大悟的表情：哦~~~~~~，我想起来了。对对对，想起来上一次出北京的时间了。大姐喜上眉梢，赶紧打断问道：快说，啥时候？去哪了？我回答：去年国庆，去天津玩了三天。然后只见大姐一脸的失落：这怎么可能？然后同屋其他居委会大姐都表示，这应该是误判。但是没办法，只能先去做核酸。

然后喜滋滋的居家办公了两天，拿着核酸阴性证明。终于恢复了我的健康宝绿码。不过在全球都躺平的防疫政策下，中国迟早也会要躺平的。炒个蛋炒饭，来庆祝一下离我远去的健康宝弹窗~

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXBX8ibUUoFFQZgllhSTdGBPbbaaFKBV8RvdOg5yLM4c3e8ZnstgnWat6wIPsdjIpdZEM53o3Ut0XQw/640?wx_fmt=jpeg)

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