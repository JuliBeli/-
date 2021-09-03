import pandas as pd
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib import cm
from collections import Counter
########################################## 数据处理：#####################################

#读取文件中的数据：
df=pd.read_excel('dangdang.xlsx')
# 将数据按照图书畅销榜顺序排序:
df.sort_values(by='rank',inplace=True,ascending=True,ignore_index=True)
# 按照图书畅销榜顺序提取每个商品的数据：
# 1.以列表的形式提取价格：
df_price = df.price.tolist()
# 去掉rmb符号：
df_price=[i.replace('¥', '') for i in df_price]
# 转化为浮点数：
df_price=list(map(lambda item:float(item),df_price))

# 2.以列表的形式提取评论数：
df_comments = df.comments.tolist()
# 只保留数字：
df_comments=[i.replace('条评论','')for i in df_comments]
# 转化为整数：
df_comments=list(map(lambda item:int(item),df_comments))

# 3.以列表的形式提取出版社相关数据：
df_publisher = df.publisher.tolist()
#以出版社名为键，出现的次数为值创建字典：
dict_publisher=Counter(df_publisher)
#将字典中的键值对进行排序，返回包含单个键值对元组的列表：
re_publisher=sorted(dict_publisher.items(), key=lambda item:item[1], reverse=True)
#创建空列表存放出现次数排名前十的出版社名称、对应的出现次数和其他出版社对应的出现次数：
top10_publisher=[]
counter_of_top10=[]
counter_of_rest=[]
# 获得上述列表需要的数据：
for i in re_publisher:
    if re_publisher.index(i)<10:
        top10_publisher.append(i[0])
        counter_of_top10.append(i[1])
    else:
        counter_of_rest.append(i[1])
# 将其他出版社出现的次数求和：
sum_of_cor=[sum(counter_of_rest)]
# 得到4个列表top10_publisher  ,  counter_of_top10  ,   counter_of_rest  ,  sum_of_cor

# 4.以列表的形式提取作者和出品方相关数据：
# 删除含有空白数据的行：
re_df=df.dropna()
# 获得列表形式的数据：
df_aap = re_df.author_and_producer.tolist()
# 对数据进行分割
str_df_aap=','.join(df_aap)
df_aap=str_df_aap.split(',')
# 以作者和出品方为键，出现的次数为值创建字典：
dict_aap=Counter(df_aap)
# 将字典中的键值对进行排序，返回包含单个键值对元组的列表：
re_aap=sorted(dict_aap.items(), key=lambda item:item[1], reverse=True)
# 创建空列表存放出现次数大于等于7次的作者和出品方名称、对应的出现次数：
e7aap=[]
counter_of_e7aap=[]
# 获得上述列表需要的数据：
for j in re_aap:
    if j[1]>=7:
        e7aap.append(j[0])
        counter_of_e7aap.append(j[1])
# 得到2个列表e7aap  ,  counter_of_e7aap

########################################### 数据可视化：##############################################

# 1.3d散点图：

# 设置中文字体：
myfont = fm.FontProperties(fname=r"C:\Windows\Fonts\STZHONGS.TTF")
# 创建画布和图表：
fig = plt.figure()
ax1 = fig.add_subplot(projection='3d')
# 为坐标赋值：
xs = df_price
ys = np.arange(1, 501)
zs = df_comments
# 设置图标的样式：
ax1.scatter(xs, ys, zs,c = ys,cmap='hsv',marker=',')
# 设置坐标轴的标签：
ax1.set_xlabel('价格/元',fontproperties = myfont,fontsize = 12)
ax1.set_ylabel('排名',fontproperties = myfont,fontsize = 12)
ax1.set_zlabel('评论数量/条',fontproperties = myfont,fontsize = 12)
# 标题：
plt.title('当当网近30日畅销书排行榜中商品的排名、价格与评论数量间的关系',fontproperties = myfont,fontsize = 15)
# 不使用科学计数法：
ax1.ticklabel_format(style='plain')

# 2.饼图：

# 数据和标签：
shapes1=top10_publisher+[f'其他（{len(counter_of_rest)}家）']
values1=counter_of_top10+sum_of_cor
# 使饼图的第一块和第六块偏移：
explode1 = (0.2,0,0,0,0,0.2,0,0,0,0,0)
# 设置颜色：
colors = cm.Spectral(np.arange(len(values1))/len(values1))
# 新建画布和图表：
fig2, ax2_1 = plt.subplots()
# 设置饼图的参数：
patches, texts, autotexts = ax2_1.pie(values1, explode=explode1, labels=shapes1, autopct='%1.0f%%',
        shadow=False, startangle=170,colors=colors)
# 标题：
ax2_1.set_title('当当网近30日畅销书排行榜中出现次数最多的前10名出版社及分布情况', loc='center',fontproperties=myfont,fontsize=20)
# 设置饼图中的中文字体：
plt.setp(autotexts, fontproperties=myfont)
plt.setp(texts, fontproperties=myfont)
# 使饼图呈现为一个圆：
ax2_1.axis('equal')

# 3.条形图：
# 为坐标赋值：
y =  e7aap
x = counter_of_e7aap
# 设置颜色：
colors2 = cm.Set3(np.arange(len(x))/len(x))
# 新建画布和图表
fig3, ax3_1 = plt.subplots()
# 绘制横向条形图：
hbars = ax3_1.barh(y,x,color=colors2)
# 设置y轴刻度的位置
ax3_1.set_yticks(y)
# 设置y轴的刻度（即添加中文标签）：
ax3_1.set_yticklabels(y,fontproperties=myfont)
# 反转y轴：
ax3_1.invert_yaxis()
# x轴的标签：
ax3_1.set_xlabel('出现次数/次',fontproperties=myfont)
# 标题：
ax3_1.set_title('当当网近30日畅销书排行榜中出现次数较多（大于或等于7次）的作家与出品方',fontproperties=myfont,fontsize=20)
# 添加x轴的数据标签：
ax3_1.bar_label(hbars)
# 显示图表：
plt.show()