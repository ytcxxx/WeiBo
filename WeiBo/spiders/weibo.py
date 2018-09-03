# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

from WeiBo.items import UserItem, UserRelationItem


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["m.weibo.cn"]
    start_urls = ['http://m.weibo.cn/']
    "更新代码"
    start_uid = ['6014513352', '1239246050', '2656274875']
    
    user_url = 'https://m.weibo.cn/profile/info?uid={uid}'
    follower_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
    
    def start_requests(self):
        for uid in self.start_uid:
            yield Request(self.user_url.format(uid=uid), self.parse)
    
    def parse(self, response):
        result = json.loads(response.text)
        item = UserItem()
        if result.get('data').get('user'):
            user_info = result.get('data').get('user')
            for field in item.fields:
                if field in user_info.keys():
                    item[field] = user_info.get(field)
                    yield item
                    # 关注
                    uid = user_info.get('id')
                    yield Request(self.follower_url.format(uid=uid, page=1), callback=self.parse_follower, meta={'page': 1, 'uid': uid})
                    # 粉丝
                    yield Request(self.fan_url.format(uid=uid, page=1), callback=self.parse_fan, meta={'page': 1, 'uid': uid})
                    # 微博内容
                    yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibo, meta={'page': 1, 'uid': uid})
    
    def parse_follower(self, response):
        result = json.loads(response.text)
        if result.get('ok') == 1 and result.get('data').get('cards') and len(result.get('data').get('cards')) \
                and result.get('data').get('cards')[-1].get('card_group'):
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), self.parse)
                    # 关注列表
                    uid = response.meta.get('uid')
                    user_relation_item = UserRelationItem()
                    follows = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')} for
                               follow in follows]
                    user_relation_item['id'] = uid
                    user_relation_item['follows'] = follows
                    user_relation_item['fans'] = []
                    yield user_relation_item
                    # 下一页关注
                    page = response.meta.get('page') + 1
                    yield Request(self.follower_url.format(uid=uid, page=page), self.parse_follower, meta={'page': 'page', 'uid': 'uid'})
    
    def parse_fan(self, response):
        pass
    
    def parse_weibo(self, response):
        pass
    