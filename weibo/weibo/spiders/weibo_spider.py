# -*- coding: utf-8 -*-
import scrapy
from weibo.items import WeiboItem


class WeiboSpiderSpider(scrapy.Spider):
    name = "weibo_spider"
    allowed_domains = ["m.weibo.cn"]

    # start_urls = (
    #     'http://www.m.weibo.cn/',
    # )

    def start_requests(self):
        with open('uid') as f:
            for line in f:
                uid = line.strip()
                yield scrapy.Request("http://m.weibo.cn/users/" + uid,
                                     cookies={
                                         'SSOLoginState': '1470023148',
                                         'SUHB': '0V5Vbex0fCEZA8',
                                         'SUB': '_2A2565PX0DeTxGeRG6VYV-SjPzjmIHXVWJpu8rDV6PUJbkdAKLWylkW1nsB79K5VTvQgMbd4I1Rt3b1X7_A..'
                                     },
                                     callback=self.parse_info,
                                     meta={
                                         'uid': uid
                                     })

    def parse_info(self, response):
        user = WeiboItem()
        info_mapping = {
            u'昵称': 'screen_name',
            u'性别': 'gender',
            u'所在地': 'location',
            u'生日': 'birthday'
        }
        user['uid'] = response.meta['uid']
        for info in response.xpath('//div[@class="item-info-page"]'):
            if info.xpath('span/text()').extract():
                key = info.xpath('span/text()').extract()[0]
            if key in info_mapping:
                user[info_mapping[key]] = info.xpath('p/text()').extract()[0]
        return user
