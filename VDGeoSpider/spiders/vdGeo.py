# -*- coding: utf-8 -*-
import scrapy
from VDGeoSpider.items import VdgeospiderItem
from scrapy.selector import Selector
from time import sleep


class VdGeoSpider(scrapy.Spider):
    name = 'vdgeo'
    allowed_domains = ['https://chi.timegenie.com']
    start_urls = ['https://chi.timegenie.com']

    def start_requests(self):

        url = self.allowed_domains[0] + '/latitude_longitude/'
        yield scrapy.Request(url, callback=self.parse, meta={'type': 0}, dont_filter=True)

    def parse(self, response):
        countries = response.xpath(
            '/html/body/div/div[2]/div[1]/a[@class="links"]').extract()
        # 国家
        for country in countries:
            countryItem = VdgeospiderItem()
            countryNode = Selector(text=country)
            nextUrl = countryNode.xpath('//@href').extract_first().strip()
            countryItem['name'] = countryNode.xpath(
                '//h5//text()').extract_first()
            countryItem['parent'] = ''
            countryItem['type'] = response.meta.get('type')
            countryItem['sname'] = nextUrl.split('/')[-1]
            countryItem['lng'] = ''
            countryItem['lat'] = ''
            if nextUrl:
                yield scrapy.Request(self.allowed_domains[0] + nextUrl, callback=self.parse_state, meta={'type': 1}, dont_filter=True)

            yield countryItem

    def parse_state(self, response):
        lngLatEle = response.xpath(
            '/html/body/div/div[2]/div[1]/div[@class="searchMatch"]').extract_first()
        if lngLatEle:
            cities = response.xpath(
                '/html/body/div/div[2]/div[1]/*[@class="links" and not(@itemprop="breadcrumb")]').extract()
            title = response.xpath(
                '/html/body/div/div[2]/div[1]/h1[@class="description"]//text()').extract_first()

            i = 0
            for index in range(len(cities)):
                if i == index:
                    cityItem = VdgeospiderItem()
                    url = Selector(text=cities[index]).xpath(
                        '//@href').extract_first().strip()
                    cityItem['name'] = Selector(text=cities[index]).xpath(
                        '//h5//text()').extract_first()
                    cityItem['parent'] = title
                    cityItem['type'] = response.meta.get('type')
                    cityItem['sname'] = url.split('/')[-1]
                    cityItem['lng'] = Selector(
                        text=cities[index + 2]).xpath('//span//text()').extract_first().strip()
                    cityItem['lat'] = Selector(
                        text=cities[index + 2]).xpath('//h5//text()').extract_first().strip()
                    i += 3
                    yield cityItem

        else:
            states = response.xpath(
                '/html/body/div/div[2]/div[1]/a[@class="links" and not(@itemprop="breadcrumb")]').extract()
            title = response.xpath(
                '/html/body/div/div[2]/div[1]/h1[@class="description"]//text()').extract_first()
            for state in states:
                stateItem = VdgeospiderItem()
                stateNode = Selector(text=state)
                nextUrl = stateNode.xpath('//@href').extract_first().strip()
                stateItem['name'] = stateNode.xpath(
                    '//h5//text()').extract_first()
                stateItem['parent'] = title
                stateItem['type'] = response.meta.get('type')
                stateItem['sname'] = nextUrl.split('/')[-1]
                stateItem['lng'] = ''
                stateItem['lat'] = ''

                if nextUrl:
                    yield scrapy.Request(self.allowed_domains[0] + nextUrl, callback=self.parse_city, meta={'type': 2},  dont_filter=True)
                yield stateItem

    def parse_city(self, response):
        cities = response.xpath(
            '/html/body/div/div[2]/div[1]/*[@class="links" and not(@itemprop="breadcrumb")]').extract()
        title = response.xpath(
            '/html/body/div/div[2]/div[1]/h1[@class="description"]//text()').extract_first()
        i = 0
        for index in range(len(cities)):
            if i == index:
                cityItem = VdgeospiderItem()
                url = Selector(text=cities[index]).xpath(
                    '//@href').extract_first().strip()
                cityItem['name'] = Selector(text=cities[index]).xpath(
                    '//h5//text()').extract_first()
                cityItem['parent'] = title
                cityItem['type'] = response.meta.get('type')
                cityItem['sname'] = url.split('/')[-1]
                cityItem['lng'] = Selector(
                    text=cities[index + 2]).xpath('//span//text()').extract_first().strip()
                cityItem['lat'] = Selector(
                    text=cities[index + 2]).xpath('//h5//text()').extract_first().strip()
                i += 3
                yield cityItem
