# 世上本没有路走的人多了最后才发现都是TM的套路casperJs入门教学

![cover_image](https://mmbiz.qlogo.cn/mmbiz_png/WAcdGrGyFXBImFZIvaOBzpicqQQOkMHibO7v0ib7wn023DKqkZCzKHbUjhGSm8Y1WbrpSPV3ABTjz04iaxsibwFL4vw/0?wx_fmt=png)

#  世上本没有路-走的人多了，最后才发现都是TM的套路--casperJs入门教学

原创  功夫熊猫盼  功夫熊猫盼  [ 码农世界CodePanda ](javascript:void\(0\);)

_2021年01月12日 21:43_ __ _ _ _ _

CasperJs+phantomJs绝对是神器，在模拟浏览器行为上，这绝对是不二的选择。

casperjs就是一个封装在phantomjs纸上的封装包，而phantomjs则是一个具备浏览器内核的无头浏览器。即可以完成各种浏览器行为，而没有不像firefox或者chrome等具备一个实在看得见的存在的浏览器。

似乎新公司OA，每天登陆签到，可以赚积分。然后赚积分还可以换购礼品。本来没做打算，结果同事提醒，积分兑换礼品的门槛很低。于是就是诞生了用casperjs+phantomjs神器来打造一个入门级的登陆签到小工具，然后直接塞入bat脚本中，定时自动执行。

废话少说，上图。
![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBImFZIvaOBzpicqQQOkMHibOcKa676OVDZJibBP7AomFsIiazcB4aej3v5gPPM5iagzB2MLK68m7Jr9cw/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBImFZIvaOBzpicqQQOkMHibO7v0ib7wn023DKqkZCzKHbUjhGSm8Y1WbrpSPV3ABTjz04iaxsibwFL4vw/640?wx_fmt=png)
![](https://mmbiz.qpic.cn/mmbiz_png/WAcdGrGyFXBImFZIvaOBzpicqQQOkMHibORRSNgiceZAnX9YXx2hUTeQ9iclAVCiby91hAtvPuHfG0EapB0GSQLtWFA/640?wx_fmt=png)
话说，我会不会被公司像阿里那样，直接被人事给开除啊？？？哈哈~~话说我们公司应该没有阿里那么牛逼，应该人事也开不了我吧。

有兴趣用casperjs的可以看看简单的代码，简单粗暴，上手快。

var oa_url =
'http://passport.oa.51talk.com/default/logout?from_url=http://web.oa.51talk.com/&with_token=false';

var allagents = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,
like Gecko) Chrome/45.0.2454.99 Safari/537.36','Mozilla/5.0 (Macintosh; Intel
Mac OS X 10_7_5) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94
Safari/537.4','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101
Firefox/41.0','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML,
like Gecko) Chrome/31.0.1650.63 Safari/537.36','Mozilla/5.0 (Windows NT 6.1;
WOW64; rv:41.0) Gecko/20100101 Firefox/41.0','Mozilla/5.0 (Windows NT 6.1;
WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (iPad; CPU OS 6_0 like
Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d
Safari/8536.25','Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L
Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile
Safari/534.30','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,
like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'];


function getRandomUA(array)
{
var randomIndex=Math.floor(Math.random()*array.length);
return array[randomIndex];
}

var vampire = require('casper').create({
verbose: true,
logLevel: 'error',

stepTimeout: 5000,
onStepTimeout: function()
{
console.log(1502);
console.log('single step exec timeout');
vampire.exit();
},

pageSettings:{
loadImages: true,
loadPlugins: true,
},

exitOnError: true,
});


vampire.userAgent(getRandomUA(allagents));

//clear cookies
phantom.clearCookies();

//打开入口文件，登陆页面输入密码跟用户名
vampire.start(oa_url,function(response)
{
var req_status = response.status;
this.capture("1.png");
if(req_status > 400 )
{
console.log(1500);
console.log('portal page load fail');
vampire.exit();
}

this.fill('form[action="/Default/Index"]', {
'userName': 'tangpan',
'pwd': 'XXXXXXX'
}, false);

this.capture("2.png");

});

//登陆OA系统 并且点击签到
vampire.then(function()
{
this.click('input[class="a-log-btn"]');
this.echo('login...');
this.wait(5000,function()
{
//点击签到
this.click('#record');
this.echo('Login and Sing Successfully.');
this.capture("3.png");
});

});


vampire.run(function()
{
console.log(2000);
vampire.exit();
});

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