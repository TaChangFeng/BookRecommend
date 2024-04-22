import pandas as pd
from sqlalchemy import create_engine

# 使用绝对路径指定文件位置
csv_file_path = 'C:/cleaned_BX-Book2.csv'

# 读取CSV文件
df = pd.read_csv(csv_file_path, sep=';', encoding='utf-8')

# 修改 DataFrame 列名，替换破折号和空格为下划线
df.columns = [col.replace('-', '_').replace(' ', '_') for col in df.columns]

# 为 DataFrame 添加一个新的列 bid，并赋予唯一的值
#df['bid'] = range(21017, 21017 + len(df))

# 连接到 MySQL 数据库
#engine = create_engine('mysql+pymysql://用户名:密码@本地端口/数据库名称)
engine = create_engine('mysql+pymysql://###')

# 将数据追加到 MySQL 数据库（replace）
df.to_sql('bx_book', engine, index=False, if_exists='append', method='multi')
print("finish")

