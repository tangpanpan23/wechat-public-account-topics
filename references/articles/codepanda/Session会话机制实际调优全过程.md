# Session会话机制实际调优全过程

![cover_image](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLn6XL2cLgUc15reSsTqW1DibnehvD0CBuzkxoYFdMUEoknIiarrlBGvdPQ/0?wx_fmt=jpeg)

#  Session会话机制实际调优全过程

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2024年05月28日 11:59_ __ _ _ _ _ _ 北京  _

记一次工作台打开  ，长时间不动。直到当前的sso登录态过期，再次发起操作时候提示用户信息过期的问题处理全过程。

首先工作台经过sso登录后
，会以session形式保存当前用户登录信息，同时给前端携带对应的cookie储存对应的sessionid过去。保证接下来的在工作台的操作，都是有登录状态。

但是由于某些极端情况  ，用户在打开工作台后就不再有任何操作。直到当前的session过期，再次想在工作台进行操作时候，就会触发工作台登录态过期的报警。

于是为了解决这种极端情况  ，工作台再次对session有效期进行了适当的延长。尽量保证极端情况下，用户登录态也能保存正常。

会话状态（Session）是一种服务器端存储机制
，用于跟踪用户的状态。这是必要的，因为HTTP协议本身是无状态的，这意味着服务器默认情况下不会记住用户的任何信息。

Session通过在服务端保存状态信息来解决这个问题  ，同时通过一个唯一的标识符（通常是Session ID）与客户端进行关联。

当用户第一次访问应用时  ，服务器会创建一个会话，并生成一个唯一的Session ID。

这个ID通常通过Cookie发送到用户的浏览器  ，并在随后的请求中由浏览器返回，这样服务器就可以识别并提供个性化的响应。

在实际工作台项目中
，是采用的redis集群作为持久化的储存。同时解决跨服务器sessionid可以正常识别，以及redis内存读取分布式高效、稳定性的优势。

会话过期机制的实现：在使用Redis作为Session存储时
，会话的过期机制通常依赖于Redis的TTL功能。Redis会自动清理过期的键，从而实现会话的过期。此外，每次访问会话时，都会检查其TTL值，如果会话已过期，则会从存储中删除。

会话回收的触发时机：会话的回收并不是在创建时就开始计时的
。相反，每次用户与服务器交互时（例如，发起HTTP请求），服务器都会更新Session的TTL，从而重置过期倒计时。这意味着会话的有效期是从用户的最后一次活动开始计算的。

多服务器环境下的会话共享：在多服务器环境中  ，为确保任何服务器都能正确解析Session
ID并检索会话信息，通常使用Redis集群或其他分布式缓存解决方案来共享会话数据。这样，无论请求被路由到哪个服务器，会话信息都是可用的，并且会话的高可用性得到保障。

会话状态（Session）是Web应用中不可或缺的组成部分  ，用于在无状态的HTTP协议上保持用户状态。通过服务端存储会话数据，并将Session
ID通过Cookie返回给客户端，我们可以在连续的请求之间保持用户的登录状态和偏好设置。

在Laravel框架中
，会话管理是通过中间件自动处理的。这意味着每次HTTP请求时，中间件都会检查并更新会话，确保会话持续有效。此外，响应时，Session
ID会被重新设置到Cookie中，并且会话数据会被持久化到配置的存储系统（如Redis）中。

Laravel的会话中间件确保了每次用户请求时  ，会话的有效期都会被刷新，这样用户在应用中的活动期间，会话不会过期。

实际laravel框架的session核心实现逻辑代码：

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnQqTRZRnusDibhepa8tmzYDhsLbhxKvay4c6y2PcPEqurNjp6IYUiclGw/640?wx_fmt=png&from=appmsg)

可以看到这段核心逻辑
，就是获取session全局配置，给request请求设置session会话。最后在响应response中，把当前的sessionid加入cookie中。最后才是save前面设置的session会话。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnB6pYaDldPrEvtqvHI9R84PibQZAwmYI0uYMMN45FoewjBt2jf6xWcow/640?wx_fmt=png&from=appmsg)

这里会根据配置的session驱动
，选择对应的session实例进行处理。然后给响应的请求头中，种下cookie，并且根据当前的session的有效时间，设置cookie的过期时间。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnibsicOQ05Vw4ufZ1QTcibldxiabN6XiasQUbzHk48JibqQ9uPRn9w2mrUW2g/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnpzc1TO8HVrwMIqCqls5WuAnr328zKNzUheboChJuAC1HApSf8KySibg/640?wx_fmt=png&from=appmsg)

可以看到这里给设置的cookie有效时间
，是根据给session配置中的lifetime保持一致的。最后是对应的session实例，去save操作。整个session会话设置、回写cookie，以及写入持久化的过程就完成了。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnqQsn719UzSe8VXGrfqOljzHicBJ4qkmdGeE3KdSiahibDZGsPjs2KicvgA/640?wx_fmt=png&from=appmsg)

然后这里对应的handler句柄调用的wirte方法  ，实际上是对应的redis实例，去调用的cache的put操作。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnrZcQhK2J45APicWyTngIU77NhtO2pzibCcTNvBYrBT4xyjFPtWbSTCVQ/640?wx_fmt=png&from=appmsg)

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnpzc1TO8HVrwMIqCqls5WuAnr328zKNzUheboChJuAC1HApSf8KySibg/640?wx_fmt=png&from=appmsg)

可以看到这里handler句柄
，实际是调用的redis的cache持久化进行。同时可以看到这里会根据session的lifetime配置，当时最后设置的持久化落到redis中的TTL有效时间。可以看到这里是配置里面是分钟为单位。

这个session的中间件
，保证了只要有请求过来，就一直保证了session会话的有效期，同时会重新给request种下cookie，跟在服务端调用自身配置的cache进行持久化保存。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnVejswqzZ20PZ85QQavW3xzviarqVgQFxXicAUfT7JxQdEgdZAIZb0eyQ/640?wx_fmt=png&from=appmsg)

而在最外层使用session
，只需要简单的调用全局辅助函数即可实现。可以看到这个全局辅助函数，可以同时key的不同，同时实现获取session跟存取session的作用。

![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnlrD6HeKGYiazicsPnJt4scCmzwDKxBGsdaAW0MxvyrmuiaYrnAFXrIyNw/640?wx_fmt=png&from=appmsg)

这里是框架初始化的
，session的就是初始化时候依赖注入的。实际在调用就是session配置的实例。就回到了session中间件同一个实例的handler操作过程。

![](https://mmbiz.qpic.cn/mmbiz_jpg/WAcdGrGyFXBEo6YwAkDeAqr6bJuqvbLnicphaYIz0NRfWCJooZs48V0mlwuM3qND411qkWJStnib58zZJQLPHMhQ/640?wx_fmt=jpeg&from=appmsg)

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