# 从offset跨度太大的慢查询谈MySQL的索引

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXA86dicYen9jEANCcuNpBibjj0g2GWBBK0qzjZalP2GuCK8TG6huf8n1OicFVzibc7DDeGB6p047CFlgw/0?wx_fmt=jpeg)

#  从offset跨度太大的慢查询 谈MySQL的索引

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年01月10日 22:19_ __ _ _ _ _

*

项目背景：业务反馈我们提供出去的一个接口，访问出现超时。

实际本质：最近遇到一个项目中的问题，大offset，表数量级别到达一个量级之后的大跨度查询，出现严重的慢查询。接口返回超时~

* * *

* * *

** 排查问题经过：  **

1. 先前置机的nginx的访问日志，根据对应的接口url参数，定位是否真的打到我们后端服务。因为第一反应，接口运行了一段时间，平稳没有人反馈对应的问题。所以第一反应是否是业务方的DNS服务的问题，没有打到我们后端服务。经过查询，nginx前置机访问日志确实是499的错误。

2. 根据前置机的nginx日志，可以确定是后端服务除了问题。紧接着定位到具体的接口对应的代码，然后从git项目查询近一周的commit变动日志。没有对应的代码改动。可以排除因最近的改动上线导致代码逻辑变动引发的问题。

3. 登录后端的MySQL服务，通过show processlist查询是否有慢查询存在。确实通过show processlist 存在大量的wait任务，因为其中的一条excute执行中的任务夯住~ 可以看到其中excute的中的解析后的sql语句，乍一看是没有啥问题的 。下面就是sql分析。

4.     *     *     select * from table where XX is null limit 1000 offset 900000；

1. 1、XX字段存在索引

2. 2、存在limit 1000 正常来说，有这两个sql的条件，可以保证sql不会出现这种慢查询。

3. 3、而且处于该任务是读场景远大于写的场景，这里还是采用的MyISAM存储引擎。所以通过explain来分析，也没有看出来一个所以然。但是单就这条sql语句执行时间就超过3秒~

至此问题，基本可以确信定位到就是因为这条sql语句引起，但是基本常用的套路，索引、表储存结构、以及limit加以限制是不能解决。而且问题可以确定是落在了offset量太大的问题上。

* * *

* * *

** 分析问题经过：
**

1、offset在跨度大的时候，limit其实限制作用不大了。根据MySQL执行原理， limit n offset
m是实际上执行是获取出m+n的数据量出来。然后再取前n条数据。

2、where条件，是在执行select之前先执行。根据MyISAM引擎，索引跟数据是文件是分离的。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXA86dicYen9jEANCcuNpBibjjRFoHQQwvBN6F04IY7nicjKRwHgG5Tauicq80d5IF6L7xqu725I097zMA/640?wx_fmt=jpeg)

叶子节点，存储都是数据文件的物理地址。所以这里需要查询出来所有符合where条件的叶子节点，然后把对应的data文件都给薅出来。根据data文件都是固定块大小储存，这里主要的开销就花在了从索引到data的IO磁盘开销上面。

* * *

* * *

**解决问题思路：**

将IO查找数据的IO开销，减少到limit n的范围。而不是直接的查询数据范围扩大到 n+m的范围。

*   *

select a.* from (select id from table where XX is null limit 1000 offset 90000) join table as a on a.id=B.id;

依靠子查询，只通过查索引表，把数据结果限定在limit的范围，索引表的查询速度远比查data的IO快得多。但是结果是坑爹的一面出现了，子查询里面如果不带where条件，确实是有效果。但是带上where条件，基本没有效果。依旧是将近3s的执行时间，但是去掉where条件，可以达到毫秒级别。

进一步分析：

由于MyISAM的索引的特性，index索引文件里面叶子节点，存的只是数据的data文件的物理地址。所以这里需要取id数据，对应的id文件其实索引文件中是没有的。所以这里需要data文件里面查找对应的id，这里会引起IO的磁盘消耗。所以达不到减少直接在索引表中解决查询范围缩小的目的。

于是这里通过建立联合索引XX列+id列的联合索引，这样的话相当于模拟innodb的索引储存引擎。sql执行结果，跟预期中的一样。毫秒级别。

问题思考：

MyISAM引擎跟innodb引擎的区别，主要在于索引储存的方式的区别。这也是常用的面试题之一。

innodb主键索引，叶子节点是储存的data数据。所以不论怎么样，innodb一定会有id键，不论你建表的时候主动建一个自增id还是没有自增id。（没有创建的时候会默认生成一个6位的自增的id。
）

innodb非主键索引，叶子节点储存的是主键id。通过再次去主键索引，再查到所需要的数据。所以一般innodb主键索引是非常快的，也建议最好是走主键索引。

MyISAM引擎，不区分主键索引跟非主键索引。叶子节点都是储存的data文件的物理地址。所以MyISAM引擎主键索引跟非主键索引效率相差不大。

这里引发的问题思考在于，select
的字段，如果只需要通过索引表就能解决，而不需要回表查询（IO消耗），可以大大解决查询时间。所以要在解决慢查询耗时的问题，就是往这个MySQL本质问题的上靠。通过索引表来解决99%的所需要的查询任务，最后1%只需要拿到真正要的数据，去数据文件里面拿数据。

PS:一张简陋的手写图~

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXA86dicYen9jEANCcuNpBibjjyP3MqlsSlxyo7GZsNxLMtsLPFiagB3Q37lfe5h79A1eNFmzSvvsuG5w/640?wx_fmt=jpeg)

以前写过数据库文章：

[ 玩转MySQL，PHP最佳搭档
](http://mp.weixin.qq.com/s?__biz=MzA5NTc2NzcxOA==&mid=2448038236&idx=3&sn=03b1de4e896e45301fbd3285efd36c47&chksm=84a4e495b3d36d837cbfd8e045a166349886047b970ab15243c136c2d00b7c71e29ac212adb0&scene=21#wechat_redirect)

[ MySQL索引不超过3层的原因
](http://mp.weixin.qq.com/s?__biz=MzA5NTc2NzcxOA==&mid=2448038164&idx=1&sn=6bc746e51137309e6d5a15b4bf52e738&chksm=84a4e4ddb3d36dcbc09df5b57e001b1a44c15f8d57aa66a42cfb01f1e45486fac8e245588940&scene=21#wechat_redirect)

[ 一次MySQL的实操~权限问题刷新问题
](http://mp.weixin.qq.com/s?__biz=MzA5NTc2NzcxOA==&mid=2448038003&idx=2&sn=7094ade13f14b3a1f73bc78a6958e027&chksm=84a4e5bab3d36cac10ace3b334709f787b3141cca189fd893ed421a14b6fc61f7ba244409a24&scene=21#wechat_redirect)

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