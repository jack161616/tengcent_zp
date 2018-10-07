# -*- coding: utf-8 -*-

# 使用crawlspider类创建的腾讯招聘爬虫

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tengxun.items import TengxunItem


class TxzpCsSpider(CrawlSpider):
    name = 'txzp_cs'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parseContent', follow=True),
    )
    print '--------------------'
    print LinkExtractor(allow=r'start=\d+')
    print '--------------------'

    def parseContent(self, response):
        for each in response.xpath('//tr[@class="odd"]|//tr[@class="even"]'):
            item = TengxunItem()
            name = each.xpath('./td[1]/a/text()').extract()[0]
            detailLink = each.xpath('./td[1]/a/@href').extract()[0]
            positionInfo = each.xpath('./td[2]/text()').extract()
            peopleNumber = each.xpath('./td[3]/text()').extract()[0]
            workLocation = each.xpath('./td[4]/text()').extract()[0]
            publishTime = each.xpath('./td[5]/text()').extract()[0]

            item['name'] = name
            item['detailLink'] = detailLink
            # positionInfo 上有些为空
            if len(positionInfo):
                item['positionInfo'] = positionInfo[0]
            else:
                item['positionInfo'] = None
            item['peopleNumber'] = peopleNumber
            item['workLocation'] = workLocation
            item['publishTime'] = publishTime

            yield item
