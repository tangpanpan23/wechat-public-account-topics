# PHP的小细节字符变量

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXBic3POoOnCEAyjRdLtQQtFWqDXBibgTOF118piag35TavyWSLrZvkmuRNtzJJ6HGUicTedtQCiaP63ciaw/0?wx_fmt=jpeg)

#  PHP的小细节-字符变量

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年09月08日 11:04_ __ _ _ _ _

任何语言提速的关键，其本质逻辑都是在内存的存取的效率，CPU的调度的利用率上面。而PHP这种语言层面的单进程，其实从语言本身去控制对CPU的调度就没有太多的功效，倒是也有这样一个分支朝着这个方向优化，例如swoole协程，就是考虑从CPU的调度利用率上面做功夫。但是就语言本身迭代的历史主进程，还是从内存的读取效率为大方向。

所以PHP语言本身的迭代，从PHP5到PHP7这个大版本的跳跃，最大的优化点也是在于变量结构体的改变，从而整体提升了PHP7的运行的效率。单纯变量的结构体相比较，整体的PHP7做了精简，而且合理利用了计算机读取的不管是32位，还是64位计算机分配内存对齐的原理。控制变量结构体在32位的倍数之类，能够最大程度减少多余内存的分配读取。减少在变量不仅仅是本身内存的开销，还有申请内存过程中的产生的开销。这个应该PHP7相较于PHP5性能提升的关键因素。

一个细节小问题，单引号跟双引号的区别。正常来说都是字符串的话，没有区别。尤其是PHP这种弱变量语言来说。作为PHPer最常见的，双引号会解析里面的变量，而单引号不会解析都直接当成普通字符串。所以这里在定义字符串string变量的时候，尽量采用单引号，避免无意义的转换开销。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBic3POoOnCEAyjRdLtQQtFWbnw2VtCKo2OAyLp5BNaVn1IO6vxLT2hAXhdVIl98Gicr0onvV5Rz0vw/640?wx_fmt=png)

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBic3POoOnCEAyjRdLtQQtFWvfejduiaWHOVUcicKOefPzRp0QfyiaHh1dCS6qypvyEdLd1OgfeCQ3law/640?wx_fmt=png)

这里可以明显看到，双引号对里面的字符串，做了一次转义。所以双引号处理字符串的时候，当需要echo
或者print输出的时候，会自动调用string的转换函数来处理双引号之间的内容。里面的\0
直接被处理成字符串‘0’，而单引号之间的内容，直接整体当成字符串处理，不会转义的情况。

另外一个小细节点，在字符串变量是COW 写时复制的原则，而整体变量是直接copy一份值存入。这里存在一个常见的
误解偏见，字符串变量比同样的整体变量更节省空间，因为cow的原则存在。这是错误的观点。

因为PHP7新的变量zval结构体，里面的zval.value按照不同的类型给重新做了分类。如果是string类型的变量，这里是zavl.value
*str 是一个指针，指向zend_string的结构体，用zend_sting结构体来存储变量内容。而如果是整型变量的话，zval.value lval
直接储存整型值，不需要额外的结构体来存储内容。结果如下：

*   *   *

$a = '123456';
$b = $a;

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBic3POoOnCEAyjRdLtQQtFWXIZRQz95bGBV8wdvZfKgpazEk1G9WhXLgWzkwcb5nFlfAWickhkiakfw/640?wx_fmt=png)

*   *   *

$c = 2;
$d = $c;

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBic3POoOnCEAyjRdLtQQtFWE05ojibQtr5uicfCiciacNUrIwCP41ZXiaOpbVwZ1ibDNao1khmJwO5Aw4EQ/640?wx_fmt=png)

所以还是整型变量更节省空间。所以在程序代码里面，如果不需要字符串的数字，尽量可以申明成int类型来使用。

另外opcache开启对PHP的影响，就是字面量，以及常量字符是否常驻内存，这里的常驻的内存是PHP的CG全量字符表，会把PHP的代码经过词法，语法解析后，变成AST的抽象可执行opcode中间码，会把字面量，字符常量标记成inner_string内部字符常量类型，从而进行保存。而且这种也只有php-
fpm模式下存在，如果是cli模式的话，还是会把PHP的生命周期的全流程重复执行。php_mould_start php_request_start,
php_request_finsh, php_mould_end。 PHP-
fpm模式下，只是请求生命周期内，会进行销毁对应的变量。而PHP初始化阶段的内部保留字符串，常量，等不会销毁依旧保持在内存的CG里面，从而可以加速PHP执行的速度，不用每次都做重复的解析。

ps:

另外最近get到了一个新的skill，netstat命令参数的详解。之前都是netstat
查看本机的网络连接。但是不清楚后面携带参数到底干啥的。赶紧把几个常用参数解释给get到技能包里面。

netstat –all(a) –numeric(n) –tcp(t) –udp(u) –timers(o) –listening(l)
所以在查看本地网络连接的时候，一般都是tcp协议，netstat -ant 如果查看监听listen状态 可以再加上l参数~
貌似就这几个参数就足够来对付常用的问题排查了。

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