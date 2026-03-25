# PHP程序猿技术流水账

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXAss1yMbhTGSqJSqw31rAzjiaxC3IIOhDEMKqw9ibElAsPAmLdnlL1FfmBpzXprK30JeyNWBCt8DCQg/0?wx_fmt=jpeg)

#  PHP程序猿技术流水账

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年04月13日 09:42_ __ _ _ _ _

#  前言

PHP程序猿的技术流水账，工作多年，历经各种大小项目。很少回过头去总结回顾，在项目中提升了什么？得到了什么？技术深度几何？突发奇想，想对自己脑海里闪现过的技术细节做一个流水账。想到哪里，就随手赶紧写下来
。

##  PHP语言本身：

细节技术点，
第一，PHP是一种动态脚本执行语言。所以PHP需要解释器，需要将PHP代码通过词法分析器，解析成中间opcode码的过程。在这里可以opcode
cache缓存，从而PHP的运行速度。
第二，PHP的是单进程，一般通过php-
fpm进行管理，通过master进程来调度worker进程处理请求。在常见问题之中，瞬时高并发流量进来，web响应缓慢会导致的php超时，在web访问日志看到的500的或者504的http错误码。可以通过适当调整加大php-
fpm的进程数，解决php超时问题。

PHP变量的一个技术点：
传值跟传地址的区别。一般情况，变量都是采取=传值，相当于变量内容，都是开辟不同的空间进行储存。=变量赋值，针对普通的字符、数组类型是传值，但是针对object对象是引用。在新版本的PHP中，采取的COW，Copy
On
Write写时复制技术）。在变量没有改变的前提下，不会开辟新的堆栈地址存储变量内容，只有发生变量内容发生改变的时候，才会开辟新的内存堆栈地址存储对应的内容。
所以在实际项目中，如果超级大的数组变量情况下，针对超大数组变量(百兆),并且不需要对变量做修改的情况，或者修改的条件都是可以业务上统一的情况下，这里最好采用传引用&，这样可以大大的节约内存使用。
简单code验证一下:

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

<?phpecho "脚本初始化内存大小字节:".memory_get_usage().'</br>';$a = array();for($i=1; $i<10000000; $i++){    $a[$i] = rand(1,1000).'tanktestds';}echo "初始化千万数组变量消耗内存:".memory_get_usage().'</br>';//普通传值$b = $a;echo '普通传值 a赋值给b消耗内存'.memory_get_usage().'</br>';//对其中一个变量进行改变$a[100000] = 'panpan';echo '对其中a变量进行改变消耗内存变化:'.memory_get_usage().'</br>';//对另外一个变量进行改变$b[1000098] ='dada';echo '对其中b变量进行改变内存变化:'.memory_get_usage().'</br>';
$c = array();for($i=1; $i<10000000; $i++){    $c[$i] = rand(1,1000).'tanktestds';}echo "初始化千万数组变量消耗内存:".memory_get_usage().'</br>';$d = &$c;echo '引用传值 c赋值给d消耗内存'.memory_get_usage().'</br>';//对其中一个变量进行改变$c[100000] = 'panpan';echo '对其中a变量进行改变消耗内存变化:'.memory_get_usage().'</br>';//对另外一个变量进行改变$d[1000098] ='dada';echo '对其中b变量进行改变内存变化:'.memory_get_usage().'</br>';die('finish');

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXA0OQsRcbRET75VgaPaOGQ6O8HyibmoBW64fQklJiaD1PSsnLVptgIcq1mlWBSWsuicoljTDQ6JnOqLw/640?wx_fmt=png)

可以清楚看到，不论是传值or传引用，在变量进行赋值的时候，不论是= or &=
内存不会发生变化。当其中一个变量改变的时候，确实看到内存翻倍的变化。证明了COW。当前php7.3的版本。而采用传引用的时候，都是平稳的，不会发生内存的明显的波动。

##  PHP语言跟web服务的衔接

一般服务部署，都是前置反向代理机，通过负载均衡到后端真实的web服务上。这里涉及获取真实的客户端IP的问题。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXCBSQRiakozn7UiczRxUpAzUKia68A72daHFqFGsu8twCumED1LWOR6Y5w4HF1se3PdDY3TfMGibwSdYg/640?wx_fmt=png)

$_SERVER预定义的超全局数组变量，可以获取到请求header头信息，请求path路径，以及当前执行脚本的位置等信息~所以header头信息，在通过nginx负载机的时候，需要代理机set
header头，将用户真实的信息带过来。否则后端服务器，拿到的都是从负载机过来的IP。

所以需要在前置机proxy_set_header添加客户端真实的IP地址，透传到后端真实的服务器，以便于$_SERVER超全局预定义的数组变量，可以获取到真实的客户端的HTTP_X_REAL_IP。

##  HTTP的响应码

正常http常用的状态，2XX是正常的请求。3XX都是重定向错误码。4XX都是资源类型错误码。5XX一般是服务器自身的错误。
尤其是301跟302状态码，都是跳转跟重定向。
主要区别在于：
301的状态码是永久重定向，在于老域名废弃，或者http切换https的场景下使用。这里尤其是针对搜索引擎跟前端缓存服务。前端会缓存301的新url服务的信息，同时搜索引擎会收录新的url站点的信息。
而302状态码，临时跳转。主要是场景在于登录后成功跳转，或者购物车支付订单的首页跳转等业务场景。一般是不进行前端缓存（除非指定~），同时搜索引擎依旧只会收录老的域名地址地址。

##  整站加速CDN：


Content Delivery
Network，内容分发网络。顾名思义，CDN这是一个网络。而CDN的加速的本质，就是在DNS服务、ISP服务商，在真实的服务器中间提供一层负载均衡的cache内容。通常会通过当前的IP地址，地域、或者当前的网络服务商，选择最近的ISP服务商服务上的cache，快速返回给用户。避免了真实服务器的带宽的拥挤跟网络消耗，可以起到削峰操作，最主要还是提速。
所以这里CDN的技术细节点，
第一网络负载均衡，通过在DNS选择对应的合适的ISP服务商提供服务。
第二，内容缓存技术 。需要在各个服务节点，提供cache服务。避免频繁的请求后端真实的资源。

##  安全编码XXS跟CSRF

XSS（Cross-Site Script）跨站脚本，CSRF（Cross-site Request
Foregey）跨站请求伪造。通过理解缩写的意思，顾名思义就能准确get到背后的面临的问题。

跨站脚本攻击，发生场景在浏览器，根本原因在于浏览器无法识别是否是恶意脚本代码，从而导致通过一些手段在当前页面构造一些恶意脚本，会让浏览器执行一些恶意的代码逻辑，从而发生一些非预期的操作。

本质利用在浏览器，构造非法的可执行代码，通过一些恶意非法逻辑代码，获取到一些用户敏感信息或者制造一些不可控的恶意操作。

eg:

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXA0OQsRcbRET75VgaPaOGQ6VDNE2lVibWcqVwFpbNrN3SW0NvLrNDkOOWM0zwczvtEzAdhibEro7R5g/640?wx_fmt=png)

CSRF跨站请求伪造，其根本原因是诱骗用户，通过点击恶意构造的链接，以冒充当前用户的身份，在用户不知情况下，在第三方站点进行操作动作。

其本质利用服务端，没有对当前请求做强安全性的校验导致。

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