<h2>图书推荐系统BookRecommend说明</h2>

TaChangFeng-2024/1/16编辑
***
<h4>一、项目文件夹基本结构说明</h4>

```
BookRecommend
|  .idea                       //pycharm配置文件
|  BookRecommend               //项目主文件夹
|  |  _pycache_                //配置文件
|  |  migrations               //框架用到的程序
|  |  |  _init_.py             //空文件
|  |  |  admin.py              //Django后台管理
|  |  |  asgi.py               //在PythonWeb中的接口
|  |  |  models.py             //模型文件
|  |  |  settings.py           //框架设置文件
|  |  |  urls.py               //URL地址变量
|  |  |  views.py              //视图(基于用户的协同过滤算法)
|  |  |  wsgi.py               //定义通信方式
|  |  BXdata                   //数据集文件夹BookCrossing
|  |  |  BX-Book-Ratings.csv
|  |  |  BX-Books.csv
|  |  |  BX-Users.csv
|  |  |  cleaned_BX-Book2.csv  //处理后的文件,2为附加数据
|  |  |  cleaned_BX-Book-Ratings.csv
|  |  |  cleaned_BX-Books.csv
|  |  |  cleaned_BX-Users.csv
|  |  static                   //静态文件夹,存放图片,JS,CSS样式
|  |  templates                //前端页面
|  |  |  about.html            //网站说明
|  |  |  hello.html            //网站欢迎页
|  |  |  history.html          //我的足迹
|  |  |  library.html          //图书馆
|  |  |  loginview.html        //登录
|  |  |  mainpage.html         //主界面
|  |  |  search.html           //搜索界面
|  |  |  showbook.html         //图书详情
|  |  |  zhuce.html            //注册界面
|  |  dataclean.py             //数据清洗算法
|  |  dataupload.py            //数据上传数据库算法
|  |  db.sqlite3
|  |  manage.py                //服务器启动
|  |  README.md                //项目说明
|  |  rendering                //项目效果图文件夹
```

<h4>二、项目环境说明</h4>
作品采用Python+Django+MySQL编写，具体环境如下：<br>
基本语言：Python3.9.7<br>
前端：HTML+CSS+JavaScript<br>
后端框架：Django3.1<br>
数据库：MySQL8.0.34 for Win64 on x86_64<br>
控制台终端启动：python manage.py runserver<br>
编译环境：VS Code+PyCharm<br>
系统环境：Windows11

<h4>三、数据库说明</h4>
表auth_user：存储登录用户名密码，由django生成<br>
表bx_book：存储图书数据，列属性包括bid,ISBN,Book_Title,Book_Author,Year_Of_Publication,Publisher,Image_URL_S,Image_URL_M,Image_URL_L<br>
表bx_bookrating：存储评分数据，列属性包括id,User_ID,ISBN,Book_Rating<br>
表userhistory:存储用户历史记录，列属性包括id,user_id,book_id,timestamp<br>

<h4>四、项目主要功能</h4>
用户的登录与注册<br>
图书的展示<br>
图书的搜索<br>
可选显示作者出版社<br>
我的足迹/历史记录<br>
后台管理(支持用户管理、数据管理)<br>
基于用户的协同过滤算法<br>
综合评分展示<br>
页码跳转

<h4>五、主要Python包</h4>
Django 包：<br>
django<br>
Django 分页和查询相关包：<br>
django.core.paginator<br>
django.db.models<br>
数据科学和机器学习相关包：<br>
sklearn<br>
pandas<br>
scipy<br>
numpy<br>
以上为主要用到的包，未全部列出。