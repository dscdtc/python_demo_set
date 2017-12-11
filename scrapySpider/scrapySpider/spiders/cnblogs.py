# -*- coding: utf-8 -*-
import sys
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapySpider.items import ScrapyspiderItem

reload(sys)
sys.setdefaultencoding("utf-8")


class CnblogsSpider(CrawlSpider):
    # 爬虫名称
    name = 'cnblogs' # 唯一标识，启动spider时即指定该名称
    # 下载延时
    download_delay = 2
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['https://news.cnblogs.com/']
    # 爬取规则,不带callback表示向该类url递归爬取
    rules = (
        # 下面是符合规则的网址,但是不抓取内容,只是提取该页的链接
        Rule(SgmlLinkExtractor(allow=(r'https://news.cnblogs.com/n/page/\d',))),
        # 下面是符合规则的网址,提取内容
        Rule(SgmlLinkExtractor(
            allow=(r'https://news.cnblogs.com/n/\d+',)),
            callback='parse'
        )
    )

    # 解析内容函数
    def parse(self, response):
        # 当前URL
        for resp in response.selector.xpath('//div[@class="content"]'):
            item = ScrapyspiderItem()

            title = resp.xpath('h2/a/text()').extract()
            item['title'] = title[0].decode('utf-8')

            url = resp.xpath('h2/a/@href').extract()
            item['url'] = 'https://news.cnblogs.com' + url[0].decode('utf-8')

            author = resp.xpath('div[@class="entry_footer"]/a/text()').extract()
            item['author'] = author[0].strip().decode('utf-8')

            date = resp.xpath('div[@class="entry_footer"]/span[@class="gray"]/text()').extract()
            item['date'] = date[0].decode('utf-8')

            yield item
