# 静态网站访问量统计
**彻底解决不蒜子单页面访问量出错的问题**
## [中文文档](#不蒜子docker-简介) | [DEMO](https://www.catatc.cn/post/dcs/manual/)

# Static site visitor and page view counter.
Bring this to you hugo/hexo/jekyll site:
![Counter Demo](img/demo.png)

This project is based on [zkeq/Busuanzi_backend_self](https://github.com/zkeq/Busuanzi_backend_self) with changes to better suit docker deloyments and some added functionalities. (Use the original if you want to cloud-deploy with [Replit](https://replit.com/@zkeq/busuanzi?v=1))

It is a self-hosted alternative to the popular static site visitor counter [busuanzi](http://busuanzi.ibruce.info/), which had been an amazing free service for years. However, it does occasinally suffer from slowdowns due to its popularity. And most importantly, tightening of the default privacy policies in most browsers recent years had a site effect of rendering the per-page view count functionality largely unusable, due its cross-origin nature unfortunately making anti-tracking very unhappy.

This project aim to solve these issues by self-hosting this lightweight service under the same domain. You can observe it working flawlessly on [my flightsim site here](https://www.catatc.cn/post/dcs/manual/) (page view count on top and whole site data at footer). 

### For sites already running for sometime

If you have been using the official busuanzi, it can also fetch those previous data when it first sees a site/page not in database. 

Data in Redis are in plain text. So if you really want to, you can initialize them manually.

### Depoly with Docker-Compose
```yaml
version: "3"
services:
  bsz_redis:
    image: redis:6.0-alpine
    container_name: bsz-redis
    # ports:
    #   - 6379:6379
    volumes:
      - "/path/to/busuanzi/data:/data"  # For persistent Redis data
    environment:
      TZ: Asia/Hong_Kong
    restart: always

  bsz-server:
    image: omltcat/busuanzi
    container_name: bsz-server
    # ports:
    #   - 8080:8080
    environment:
      TZ: Asia/Hong_Kong
      PROD_HOSTS: 'www.your-domain.com,blog.your-domain.com' # Production hosts, or set to 'public' for any host
      TEST_HOSTS: 'localhost:1313,localhost:4000' # Testing hosts, eg: hugo (1313) and hexo (4000). Returns random stats to help with page formatting instead of accessing/altering database
      GET_BEFORE: true  # Get previous stats from official busuanzi if available
      REDIS_HOST: bsz_redis
      REDIS_PORT: 6379
      REDIS_DB: 0
    restart: always
```

Add reverse proxy for busuanzi under your website (Nginx example)
```nginx
	location /busuanzi {
		proxy_pass http://bsz-server:8080/busuanzi;
		proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header REMOTE-HOST $remote_addr;
        add_header X-Cache $upstream_cache_status;
	}
```

Upload this [script](busuanzi.pure.mini.js), which is usually loaded from busuanzi, directly onto your website somewhere. **!!! You must change the domain on line 57 !!!**
```js
// CHANGE THIS URL TO YOURS!!!
bszCaller.fetch("https://www.your-domain.com/busuanzi?jsonpCallback=BusuanziCallback", 
```

Put the following line into your footer in order to find the script above.
```html
<script async src="/path/to/busuanzi.pure.mini.js"></script>
```

Then it will be exactly the same as using the official busuanzi. Its origianl [tutorial](http://ibruce.info/2015/04/04/busuanzi/) is in Chinese. Hugo user may want to see [this](https://github.com/xwi88/xwi88.github.io.source/commit/52ae125ad1b24910c0f3aa61e93a5ab6ef8b2575). If someone find a good English one please let me know to add it here. 

TL;DR:

Add the following elements on you page where you want to show the statistics.

```html
<span id="busuanzi_container_site_pv">
    Whole site vistor count <span id="busuanzi_value_site_pv"></span>次
</span>
```

```html
<span id="busuanzi_container_site_uv">
  Unique visitor count (based on IP) <span id="busuanzi_value_site_uv"></span>人次
</span>
```

```html
<span id="busuanzi_container_page_pv">
  Single page view count <span id="busuanzi_value_page_pv"></span>次
</span>
```

## 不蒜子Docker 简介

本项目基于[zkeq/Busuanzi_backend_self](https://github.com/zkeq/Busuanzi_backend_self)，为了适应Docker部署做了些许调整并增加了一些功能。（如果你想使用[Replit](https://replit.com/@zkeq/busuanzi?v=1)云部署，请使用上面的原版）

多年以来，[不蒜子](http://busuanzi.ibruce.info/)为无数静态网站提供了优质的统计功能。然而，巨大的使用人数也使其有时响应较慢。更重要的问题是，随着近年来各浏览器默认隐私策略的不断升级，不蒜子的单页面阅读量统计功能已基本无法使用。这主要由于其基于referer判定页面，且需要跨域执行脚本。

此处提供了一个快速轻量的Docker部署方案，可以在同域名下运行此服务，避开跨域问题。你可以看到其完美运行在[我的模拟飞行网站上](https://www.catatc.cn/post/dcs/manual/)。

### 已运行一段时间的网站初始化

如果你曾使用官方不蒜子，可以选择当用户访问数据库中没有的网站/页面时，先试图从官方站获取数据。建议当大部分的页面都已经被访问过至少一次之后关闭此功能，免得老是去戳人家的服务器。

Redis数据库里都是明文，你要实在愿意也可以连进去手动初始化。

### Docker-Compose部署
```yaml
version: "3"
services:
  bsz_redis:
    image: redis:6.0-alpine
    container_name: bsz-redis
    # ports:
    #   - 6379:6379
    volumes:
      - "/path/to/busuanzi/data:/data"  # 保存redis数据库
    environment:
      TZ: Asia/Hong_Kong
    restart: always

  bsz-server:
    image: omltcat/busuanzi
    container_name: bsz-server
    # ports:
    #   - 8080:8080
    environment:
      TZ: Asia/Hong_Kong
      PROD_HOSTS: 'www.your-domain.com,blog.your-domain.com' # 网站实际使用的域名，改为'public'则回应所有请求
      TEST_HOSTS: 'localhost:1313,localhost:4000' # 测试用网址，如1313（hugo）、4000（hexo），返回随机数便于排版，不会触及数据库
      GET_BEFORE: true  # 试图从官方不蒜子获取先前的网站和页面统计
      REDIS_HOST: bsz_redis
      REDIS_PORT: 6379
      REDIS_DB: 0
    restart: always
```

为自建不蒜子添加反向代理（以Nginx为例）
```nginx
	location /busuanzi {
		proxy_pass http://bsz-server:8080/busuanzi;
		proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header REMOTE-HOST $remote_addr;
        add_header X-Cache $upstream_cache_status;
	}
```

把这个原本是从不蒜子加载的[脚本](busuanzi.pure.mini.js)直接放进你的网站里某个地方，**!!! 注意更改第57行为你自己的域名 !!!**
```js
// CHANGE THIS URL TO YOURS!!!
bszCaller.fetch("https://www.your-domain.com/busuanzi?jsonpCallback=BusuanziCallback", 
```

然后把页面中引入不蒜子js的地方改成去找上面的脚本
```html
<script async src="/path/to/busuanzi.pure.mini.js"></script>
```

接下来就跟使用官方不蒜子完全一样了，你可以参考其[详细教程](http://ibruce.info/2015/04/04/busuanzi/)，建议hugo用户[看这个](https://xwi88.com/hugo-plugin-busuanzi/)。

在页面中适当的地方添加不蒜子的统计数字：

```html
<span id="busuanzi_container_site_pv">
    本站总访问量<span id="busuanzi_value_site_pv"></span>次
</span>
```

```html
<span id="busuanzi_container_site_uv">
  本站访客数<span id="busuanzi_value_site_uv"></span>人次
</span>
```

```html
<span id="busuanzi_container_page_pv">
  本文总阅读量<span id="busuanzi_value_page_pv"></span>次
</span>
```