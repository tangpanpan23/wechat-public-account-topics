# Redis 服务部署前期Tips

![cover_image](https://mmbiz.qlogo.cn/mmbiz_jpg/WAcdGrGyFXDu2icsuZfyAibOHFBKewgYB17umDOTiaPibXsgW88kVzkVT04XtlvSGAGxibpoyaCRv2EKasJQgfzgkuQ/0?wx_fmt=jpeg)

#  Redis 服务部署前期Tips

原创  Tank  Tank  [ 码农世界CodePanda ](javascript:void\(0\);)

_2019年07月20日 09:42_ __ _ _ _ _

###  Redis简介：

Redis 是完全开源免费的，是一个高性能的key-value数据库。用来提供系统平台的整体的性能，是一个很好的选择。
Redis 与其他 key - value 缓存产品有以下三个特点：

* Redis支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。

* Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash等数据结构的存储。复杂的数据结构。

* Redis支持数据的备份，即master-slave模式的数据备份。支持分布式部署。


主要的一点读写性能：
性能极高 – Redis能读的速度是110000次/s,写的速度是81000次/s 。
另外数据安全性：
支持写入磁盘。从内存写入磁盘，从而永久保存。这个要根据实际情况来判断，是否有必要以及有必要的情况下，使用什么样的保存模式。
最后数据一致性：
支持原子性。要么都成功，要么都失败。支持类似于数据库的事务。

###  查看redis的配置：


CONFIG GET * 命令可以查看redis的所有的配置以及配置情况。

redis具体配置项参考：
https://kefeng.wang/2017/08/12/redis-config  /
https://www.runoob.com/redis/redis  -conf.html

###  具体的redis服务相关核心配置  ：  redis.conf

###
常用核心配置：

* daemonize 配置是否以守护进程运行。在充当redis服务提供服务的时候这里应该开启守护进程运行。yes。这个是一般生成环境的实用方式。

* pidfile 这个是配套 daemonize的守护进程的id的文件保存位置。

* loglevel 设置日志报警级别 notice 适量日志信息，使用于生产环境。

* logfile 配套loglevel记录日志的位置。日志文件的位置，当指定为空字符串时，为标准输出，如果redis已守护进程模式运行，那么日志将会输出到/dev/null。

* slowlog-log-slower-than 记录慢查询类比于mysql的 slowlog慢查询日志。这里配置的单位是毫秒。redis慢查询日志存在的内存中，直接通过slowlog 命令来查看。

* slowlog-max-len 制定慢查询命令记录的条数。集合慢查询日志一起使用。

####  网络相关：

* bind IP地址 （127:0:0:1 ::1 这个是绑定的主机地址， 表示只能本地连接、unix domain sockets连接。如果是0.0.0.0 表示可以任何主机连接。不安全，不推荐。）

* prot 监听开放的端口 默认是6379

* protected-mode 是否开启安全开关 （redis3.2版本后新增protected-mode配置，默认是yes，即开启。设置外部网络连接redis服务，设置方式如下：1、关闭protected-mode模式，此时外部网络可以直接访问 2、开启protected-mode保护模式，需配置bind ip或者设置访问密码）

* tcp-backlog 配置tcp的连接数 在高并发的环境下 可以尽量避免客户端连接缓慢的问题。

* timeout 关闭超时时间设置 client 空闲多少秒之后关闭连接

* keep-alive  用来定时向client发送tcp_ack包来探测client是否存活的。单位是秒 ，  一般默认是关闭的。

####  安全配置

* requirepass 设置连接的密码 （这个密码要设置复杂一些，尤其是在外网环境的话，否则在redis每秒可以处理15W的速度，容易被暴力破解）

* rename-command 重命名命令，主要是对一些敏感重要的命令给监管起来，将命令直接置空，表示该命令禁用。CONFIG ""

* maxclients 客户端最大的并发连接数。

* maxmemory 指定Redis最大内存限制，Redis在启动时会把数据加载到内存中，达到最大内存后，Redis会先尝试清除已到期或即将到期的Key。当此方法处理 后，仍然到达最大内存设置，将无法再进行写入操作，但仍然可以进行读取操作。Redis新的vm机制，会把Key存放内存，Value会存放在swap区，格式：maxmemory <bytes>

* maxmemory-policy 当内存使用达到最大限制的时候，淘汰数据的机制。配合maxmemory的设置。
当内存使用达到最大值时，redis使用的清楚策略。有以下几种可以选择：
1）volatile-lru 利用LRU算法移除设置过过期时间的key (LRU:最近使用 Least Recently Used ) 这个
应该是正常生产环境采用的淘汰策略。
2）allkeys-lru 利用LRU算法移除任何key
3）volatile-random 移除设置过过期时间的随机key
4）allkeys-random 移除随机key
5）volatile-ttl 移除即将过期的key(minor TTL)
6）noeviction 不移除任何key，只是返回一个写错误 ，默认选项。  生产环境估计没有人会采用这个。

####  快照现场-持久化：

* save 把数据保存到硬盘的设置。用来持久化数据，保证关键数据不会因断点丢失。save <seconds> <changes> 多少秒发生多少变化，直接存入硬盘。save "" 跟不使用save 效果一样，不会保存。

* stop-writes-on-bgsave-error 这个是当写入disk硬盘失败的时候，停止用户的写入redis，但是不影响读操作。目的是为了保证数据的一致性。yes开启。

* rdbcompression 是否压缩存入db文件的数据。一般是开启压缩。

* dbfilename 数据保存disk的文件。

* dir 结合dbfilename，唯一确定db文件存储的位置。这里是指定文件目录，不包含文件。

* appendonly 以追加的方式写入文件，是否开启。与默认的rdb的持久化方式相对应。以保证数据的安全性。视情况而定，是否开启aof持久化功能开关。一般情况下，redis充当缓存服务器的话，rdb方式持久化就可以保证正常的功能服务。

* appendfilename 命令追加的指定文件

* appendfsync aof持久化策略。

no表示不执行fsync，由操作系统保证数据同步到磁盘，速度最快。

always表示每次写入都执行fsync，以保证数据同步到磁盘。这个太消耗性能，一般不采用。

everysec表示每秒执行一次fsync，可能会导致丢失这1s数据。

####  主从集群配置：（主要是提升数据的高可用，通过集群来部署提升整体的redis的服务能力）

* replicaof 指定master redis服务器的地址。<masterip> <masterport>

* masterauth master服务器的验证密码 登录密码。<master-password>

* replica-serve-stale-data 这里是主要是配置当从服务器丢失master的连接之后，是继续响应cliet的服务还是直接报错不再响应服务。

* replica-read-only 从库服务只读标记位 yes

* repl-diskless-sync 是否启用硬盘备份，（ 1、硬盘备份：redis主站创建一个新的进程，用于把RDB文件写到硬盘上。过一会儿，其父进程递增地将文件传送给从站。2、无硬盘备份：redis主站创建一个新的进程，子进程直接把RDB文件写到从站的套接字，不需要用到硬盘。）

* repl-diskless-sync-delay 这个是结合无硬盘同步备份的设置，等待多少秒，统一对从库redis进行数据同步。采用无硬盘同步，更适用于高带宽硬盘低速的情况下。

* repl-ping-slave-period 从库向master主库周期性发起心跳检测时间间隔

* repl-timeout 检测的超时时间

* replica-priority 当主库crash的时候，从库提升成主库的权值。

* cluster-enabled 开启集群的开关。默认是不开启。

###
Reids监控管理工具：


快速搭建redis-
live，redislive核心服务包括一个web服务跟redis自带的info跟monitor监控命令服务。这也是几乎所有的redis监控工具的核心。通过脚本定时or上报的方式，将这个命令的获取到的redis服务信息进行状态监控。

redis服务监控工具的选择，这个需要根据所需要的实际场景来选择，如果是只是单纯的监控的话，可以选择redis-
live来搭建。如果是需要根据一些监控指标的变化来进行报警的话，这个可以考虑prometheus来搭建。


理想监控方案：Prometheus+grafana来做监控管理。这个方案不仅可以监控各种可视化指标，还可以监控报警。其他的redis监控工具，只能可视化指标。（这个是更加通用的监控管理工具。）

redis-live的搭建教程：
https://www.cnblogs.com/huangxincheng/p/5571185.html

promethus+grafana搭建教程：
https://www.cnblogs.com/sfnz/p/6566951.html

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