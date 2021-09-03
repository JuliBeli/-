from scrapy import Spider,Request

class DangdangspiderSpider(Spider):
    # spider的名称:
    name = 'dangdangspider'
    # 设置请求头：
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                      'Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    # 起始url：
    start_urls = ['http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-1']


    def start_requests(self):
        #请求的url:
        for i in range(1,26):
            urls="http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-"+str(i)
            # 设置scrapy.Request的参数：
            yield Request(url=urls,callback=self.parse,headers=self.header)

# 使用CSS选择器通过for循环遍历书本（商品）的排名、书（商品）名、评论数、作者和出品方、出版社、价格
    def parse(self, response):
        for quote in response.css('div.bang_list_box>ul>li'):
            yield{
                "rank":quote.css('div.list_num::text').get(),
                "title": quote.css('div.name a::text').get(),
                "comments":quote.css('div.star a::text').get(),
                "author_and_producer":quote.css('div:nth-child(5) > a::text').getall(),
                "publisher":quote.css('div:nth-child(6) > a::text').getall(),
                "price":quote.css('div.price p span.price_n::text').get()
            }
