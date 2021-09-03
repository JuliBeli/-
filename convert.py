import pandas as pd

csv = pd.read_csv('dangdang.csv', encoding='utf-8')
#将csv文件转化为excel的文件类型，不增加下标列：
csv.to_excel('dangdang.xlsx', sheet_name='data',index=False)