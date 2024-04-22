import pandas as pd

# 读取原始CSV文件，遇到错误直接跳过包含错误的行
csv_file_path = 'C:/BX-Books.csv'
try:
    df = pd.read_csv(csv_file_path, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error parsing CSV: {e}")
    # 如果发生错误，可以手动跳过错误行，然后继续读取文件
    df = pd.read_table(csv_file_path, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')

# 保留指定的 ISBN 数据
specified_isbn_list = ['0345431707']  # 替换为你想要保留的 ISBN 列表
df = df[df['ISBN'].isin(specified_isbn_list)]

# 删除多余的列
df = df.iloc[:, :3]

# 删除包含空值的行
df.dropna(inplace=True)

# 在插入数据前，删除重复的 ISBN 值，保留第一个出现的
df.drop_duplicates(subset='ISBN', keep='first', inplace=True)

# 打印清洗后的数据集信息
print("Cleaned DataFrame:")
print(df.info())

# 保存清洗后的数据到新的CSV文件
output_csv_path = 'C:/cleaned_BX-Book2.csv'
df.to_csv(output_csv_path, index=False, sep=';', encoding='utf-8')
print("Finish!")
