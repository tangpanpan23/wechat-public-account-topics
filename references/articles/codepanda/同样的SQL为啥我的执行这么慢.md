# 同样的SQL为啥我的执行这么慢

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXCNAWZ3fuTuAwjfasbibAyvkmVeRdEiaFw5FeaRyQX7InibtslTVGKUxUVv3aX1e8EYfELDia186SzqOQ/0?wx_fmt=jpeg)

#  同样的SQL为啥我的执行这么慢

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年06月23日 15:58_ __ _ _ _ _

最近又get到一个小的技巧点，把之前一直疑惑的点给解开了。索引隐式转换，不要在索引字段上做函数操作，尽量把表的字符集统一，而且不要写太复杂的SQL语句。都串起来了，而且把疑惑一一解开。知其然，知其所以然。

常用的引发问题就是：MySQL，同样的SQL语句，为啥我的SQL语句执行这么慢？

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXDpj7q0K0Jb0qeHgMAqJGBH510icJQYLIm4psiaR0oBRibp89Fk1qa8OsKCiaeDlicrFAUMxmpRBnsia5vw/640?wx_fmt=jpeg)

1、在索引字段，做函数操作，会导致破坏索引有序性。会导致优化器放弃选择走索引，从而扫描全表。

2、在索引字段，存在隐式转换。字符-》数字
是默认的逻辑。但是数字-》字符，这里会破坏索引的有效性，相当于在索引字段上加上了函数操作，convert强制转换。

3、在索引字段，存在表之间的字符集的差异。也可能会导致索引失效。道理同上，convert从utf8是默认向高集合进utf8mb4进行转换。所以在
join表操作的时候，例如

select B.a from A join B A.aid on B.aid where A.id =1;

如果A是 utf8mb4字符集 B是utf8字符集~

这里sql语句等同于，先A表走主键id索引，找到id=1的记录，然后找到对应的字段aid出去，去扫描B表中全局索引表，依次比对B.aid是否跟A.aid一致。这里在B表中会触发全表扫描操作，因为B表的字段需要等同于convert(B.aid)
字段到utf8mb4字符集，相当于在字段上做函数操作。

这里需要优化的时候，第一，统一字符集。第二，强制把默认的转换过程，转成utf8mb4强制转成utf8.也能解决问题。

结论：

这里同时引发了另外一个问题，MySQL语句尽量单表，简单查询操作。不要做复杂的联表，子查询，嵌套子查询，尽量把业务逻辑，上收在代码层来实现，把数据底层依赖的SQL语句都严格控制在简单可以依赖的地步。也是我编码的一直以来的思想之一。

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