# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'users'
    id = Field()
    description = Field()
    screen_name = Field()
    followers_count = Field()
    gender = Field()
    verified_reason = Field()
    profile_image_url = Field()


class UserRelationItem(scrapy.Item):
    collection = 'users'
    id = Field()
    follows = Field()
    fans = Field()


class WeiboItem(scrapy.Item):
    collection = 'weibos'
    id = Field()
    attitudes_count = Field()
    comments_count = Field()
    reposts_count = Field()
    source = Field()
    pictures = Field()
    text = Field()
    textLength = Field()
    thumbnail = Field()
    user = Field()
    created_at = Field()
    crawled_at = Field()