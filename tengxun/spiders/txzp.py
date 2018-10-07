# -*- coding: utf-8 -*-
import scrapy
from tengxun.items import TengxunItem
import re


class TxzpSpider(scrapy.Spider):
    name = "txzp"
    allowed_domains = ["hr.tencent.com"]
    start_urls = (
        'http://hr.tencent.com/position.php?&start=0#a',
    )

    def parse(self, response):
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

            curpage = re.search('(\d+)',response.url).group(1)
            page = int(curpage) + 10
            url = re.sub('\d+', str(page), response.url)

            # 发送发送新的url请求加入待爬队列，并调用回调函数 self.parse
            yield scrapy.Request(url, callback = self.parse)

            # 将获取的数据交给pipeline
            yield item







