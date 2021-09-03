from scrapy import cmdline

# 把字符串分割为列表后执行命令,输出储存了爬虫数据的dangdang.csv:
cmdline.execute('scrapy crawl dangdangspider -o dangdang.csv'.split())