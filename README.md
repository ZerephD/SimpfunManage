# SimpfunManage-简幻欢服务器运维

---

**详细教程可以到我的[ 博客 ](https://blog.zereph.online/archives/1702112813409)去阅读**

## 简述
适用平台：[简幻欢v4](https://simpfun.cn/)

版本：1.1.0

有疑问联系：[Zereph](https://t.me/Zereph_Dandre)

## 使用
### 一键部署：

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/ZerephD/SimpfunManage)

### 添加环境变量：

**在控制台的`settings/Environment Variables`中添加环境变量：(注意大小写)**

|   变量名    |                    简述                     | 必填  |
|:--------:|:-----------------------------------------:|:---:|
|   Name   |                你在简幻欢的账号的名称                |  是  |
| PassWord |                你在简幻欢的账号的密码                |  是  |
|  Token   |                简幻欢的账号的验证凭证                |  否  |
| BotToken | TG机器人的Token，详情自行[谷歌](https://google.com/) |  是  |

Token在`2024.1.6`更新中已移除，如需获取方式请[联系我](https://t.me/Zereph_Dandre)

### 初始化:
访问 `http://你的域名/ini` ，等待返回数据(时间可能稍长)

***注意！：请尽量用你自己的域名，Vercel的域名在POST请求时会有验证导致TG的Webhook失效***

## 更新日志： 
- 2024.1.6 支持Token自动获取，信息配置方式改为Vercel环境变量 
- 2024.1.6 Telegram机器人webhook链接自动设置