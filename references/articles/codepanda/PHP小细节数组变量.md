# PHP小细节数组变量

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXD0bk6icLp2fG2cSZSZ3iaFdV8pMia79jv4libHXru3UL9rbBwkjEP2a3NAOosX5PN61VApn9NTlW4Ibw/0?wx_fmt=jpeg)

#  PHP小细节-数组变量

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年09月13日 11:28_ __ _ _ _ _

PHP首先是一种脚本语言，而且是弱语言，天然决定了代码的易上手，易开发。很开放的一种语言，但是由此容易注定PHPer的代码随意性，从而忽略不同代码写法小细节带来的系统影响。

废话少说，从一段简单的代码入手，同样实现一个数组变量，来承载100W个元素int整形的数字。

code demo1：

*   *   *   *   *   *   *   *   *

$start_1 = memory_get_usage();$a1 = [];for ($i=0; $i<10000000; $i++){    $a1[$i] = $i;}$end_1 = memory_get_usage();
$test1 = sprintf('spend memory %d M for A array', (($end_1 - $start_1)/1024)/1024);


code demo2：

*   *   *   *   *   *   *

$start_2 = memory_get_usage();$b1 = [];for ($j=10000000; $j>0; $j--){    $b1[$j] = $j;}$end_2 = memory_get_usage();$test2 = sprintf('spend memory %d M for B array', (($end_2 - $start_2)/1024)/1024);

从效果上来说，$a 跟$b
数组变量实现的效果是一致的没有区别，在实现起来的复杂度也是同样的没有差异。但是实际这两个不同方式的实现的变量数组，对内存的影响却存在较大的差异。

对比结果，$b比$a要多消耗超过100M的内存空间。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXD0bk6icLp2fG2cSZSZ3iaFdVe48ycmFknpBYiceSpDUCUzK8pUYgk3XC7oprOpfPWaicve5xiayCS97TA/640?wx_fmt=png)

在PHPer代码层面，两个变量写法没有差异，但是实际影响的内存的性能差异，确实100多M的浪费。由此这里需要了解一下PHP数组变量的储存结构，从而避免在代码中因为语言本身太随意的特性，从而导致的性能的差异。

PHP数组变量
1、是采取的HashTable的储存。key=》value的储存模型，会把对应的key经过hash函数，转成唯一的h值作为hashTable储存结构体中的唯一快速索引的标志。
2、HashTable存在数组结构的时候，跟进key的类型的不同，会分成packed array 跟 hash
array的不同的两种类型。而packed顾名思义，压缩型储存结构，直接key可以快速的映射到对应的h的索引里面，h直接直接充当索引。而hash
key的，一般是对应key为字符的时候，转成h后，不能直接充当索引，所以维护一张索引表来，通过h跟索引掩码，从而达到快速的映射效果，同时最大程度的利用空间。（hash
array的目的，主要是为了最大程度利用空间，用较小的索引空间，通过掩码，从而可以最大程度的压缩bucket的数组的内存大小。否者bucket空间，会存在大量的浪费空间，从而成为一种稀疏数组~）
回到上面的数组变量的的引发的，差异也就是中间每个index的int32的索引空间的内存消耗。在bucket100W的时候，对应的多消耗的index的100W*4/1024/1024的多余内存消耗。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXD0bk6icLp2fG2cSZSZ3iaFdV721icoRuTJnTgticJtVkibHShSEjPFOic2cC7Xd9Eh5v4stoX1oXCEsc4g/640?wx_fmt=png)


上面这个是最简单的模型，其实php数组变量，远比这个复杂。而且还包括自动的rehash的优化，到达阈值触发rehash操作等~可以多去学习一下。

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