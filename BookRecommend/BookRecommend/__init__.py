import pymysql
pymysql.version_info = (1, 4, 6, 'final', 0)  # 设置版本信息以避免报错
pymysql.install_as_MySQLdb()
