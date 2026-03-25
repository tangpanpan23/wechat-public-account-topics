# 一分钟带你了解一个SQL新引擎的红与黑

![cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXDeHHobNgxF9QibjviaxDbibxYeG867Ht4Kt5deW3tLecK61oYVFsibgQzJfNaOibWamv3Dpvk3RbJcutQ/0?wx_fmt=jpeg)

#  一分钟带你了解一个SQL新引擎的红与黑

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2024年07月23日 19:52_ __ _ _ _ _ _ 北京  _

MySQL除了常见的InnoDB和MyISAM引擎外，还有一种不太常用但在特定场景下非常有用的引擎——Federated引擎。

简单来说，Federated引擎允许本地SQL数据库指向远程SQL数据库，从而实现分布式SQL查询。

两个基本概念：

* 本地SQL数据库中的表是虚拟的，不实际存在，只是建立了一个连接以指向远程真实的表。

* 远程连接包括认证授权等鉴权信息，如远程服务器地址、用户名和密码等。

业务场景应用：

在账号系统任务库中，如果需要依赖上游主数据库中的部分数据，而这两个系统是独立的，那么使用Federated引擎是一种有效的解决方案。在这种情况下，可以在账号系统中像使用本地数据表一样进行各种涉及两个库表的SQL关联操作。

注意事项：

1. Federated引擎中的本地表只是影子表，通过网络将SQL查询拆解并发送到远程库执行，然后返回结果。因此，禁止尝试写操作，以避免变更远程数据库的数据。建议为远程库提供只读权限的连接账号。

2. Federated引擎不支持JSON格式的字段。如果查询包含JSON字段，会直接报错。因此，在创建影子表时，应避免使用JSON字段，只需根据需求创建非JSON格式的字段

3. Federated引擎不支持事务操作。

一分钟，GET一个SQL新玩意。打算后续把自己这些年项目中经历的一些有趣的、有意思的奇奇怪怪的知识点，提取成一个一个一分钟的片段分享出来。跟这个有趣的世界，say
hello~

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXB9kVHSlXxdPbRIRL7gwHwnXfOWCj9A30KrUaRN0f4AkRTB3V700QojwrQJrwPBTOrl9GDfibicNwzw/640?wx_fmt=jpeg)

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