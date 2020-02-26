# Factual 爬虫
## 背景
Factual 为美国数据网站四巨头之一. (四巨头包括: yelp, factual, infogroup和foursquare<sup>[[1](https://whitespark.ca/local-search-ecosystem/)]) </sup>   
Factual 公司已不对外公开提供API. 在数据搜索上一个新账号一天只能访问33次, 一个老账号(2014年前注册)一天只能访问3333次.  
[网站首页](https://www.factual.com/)  
[网站数据搜索首页](https://www.factual.com/data-set/global-places/#places-crosswalk)  
[网站数据搜索界面](https://places.factual.com/data/t/places#filters=%7B%22$and%22:[%7B%22country%22:%7B%22$eq%22:%22US%22%7D%7D]%7D)   
[网站注册界面](https://accounts.factual.com/users/register)  

## 账号要求
### 必要性
如不登录进行爬虫, 则每次在[网站数据搜索界面](https://places.factual.com/data/t/places#filters=%7B%22$and%22:[%7B%22country%22:%7B%22$eq%22:%22US%22%7D%7D]%7D)进行搜索时, 均要进行谷歌验证码(recaptcha)验证.  
但若登录进行查询, 则在账号的权限内进行查询, 不需要进行验证码验证.  
### 账号权限
根据网站显示, 目前账号权限级别有两种: 老账号和新账号. 在2014年前注册的为老账号, 2014年后注册的为新账号.   
老账号的权限为每天访问数据搜索网页的次数为3333次左右, 新账号的权限为每天访问数据搜索网页的次数为33次左右.  

## 爬虫相关
### 可用版本
目前可用的版本为factual_v2.py.
### 运行方法
python3 factual_v2.py -F xxx -H True/False
### 超参数
`pageLimitation`: 每个关键词所列出的网页中爬取网页的数量.  
`start`: 从关键词列表中的第start个关键词开始爬取.  
`email`:  factual账号.  
`password`: factual账号密码.



