# 基于Web的教务管理系统

该目录下为该项目的源代码

其中`server/`是后端源代码，`user_interface/`是前端源代码。

## 如何运行

后端是基于Python Flask框架的，依赖MySQL数据库。

启动后端，首先需要配置好MySQL服务，这不是本项目的一部分。然后将数据库连接所需的参数写入`server/config.py`中

然后确保你的Python版本大于3.5，确保你的Python运行环境包含以下第三方库

- flask
- sqlalchemy
- pymysql

然后运行`server/manage.py`



前端，你只需要将后端的ip地址填进`user_interface/js/leader.js`和`user_interface/js/leader.min.js`，然后双击打开`user_interface/index.html`就可以了，或者用一个静态服务器部署它

