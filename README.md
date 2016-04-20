# green

## 说明

本仓库是微信公众号 **Ms_haoqi** 的源代码，扫码关注：

![二维码](http://img.blog.csdn.net/20160419140351193)

更多介绍可以参考博客 [Python快速搭建自动回复微信公众号](http://blog.csdn.net/tobacco5648/article/details/51190039)。

## 使用配置

需要在根目录下添加```conf.json```文件，内容为：

```json
{
	"token": "your_weixin_token",
	"appid": "your_weixin_appid",
	"secret": "your_weixin_appsecret",
	"mode": "normal",

	"mongo_db": "green",

	"max_host_count": 5,

	"auto_reply": "yes",
	"tuling_key": "1d2679920f734bc0a23734ace8aec5b1",
    "tuling_url": "http://www.tuling123.com/openapi/api"
}
```

其中需要修改的参数有：

- ```token``` : 修改为微信公众号的Token(令牌)
- ```appid``` : 修改为微信公众号的AppID(应用ID)
- ```secret``` : 修改为微信公众号的AppSecret(应用密钥)
- ```tuling_key``` : 修改为申请的图灵API KEY

另外需要本地安装有MongoDB
