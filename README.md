# douban_spider
爬取豆瓣电影相关数据


  整个爬虫主要爬取三个方面的内容，电影信息、评论信息、用户信息，其中用户信息里面又包含了用户基本信息，用户关注人信息，用户想看的、正在看的、看过的电影信息。
  整个爬虫共分有三个大的工具类。获取cookie信息，数据库交互，存储数据到文件（包括存储爬取失败的数据和将数据库中的数据保存为文件）。其中获取cookie信息又分为cookie的获取（使用selenium模拟登陆获取，当用户在常用地点登陆时没有移动滑块。本代码没有做移动滑块的处理），cookie的检测（访问某个个人界面，并带有刚获取到的cookie信息，看是否可以获取到数据），cookie失效检测，cookie对外接口。
  每个爬取内容的基本框架为：
init(初始化相关资源)->spider(获取爬取的链接)->request(请求该页面)->parse(解析页面)->end(关闭相关资源，如数据库连接、selenium)
