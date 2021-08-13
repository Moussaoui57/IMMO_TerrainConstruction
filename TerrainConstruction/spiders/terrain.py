# -*- coding: utf-8 -*-
import scrapy
from TerrainConstruction.items import TerrainconstructionItem
from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest
import ast
from datetime import date, timedelta
import logging
import re
import json
import random
import datetime 
import requests

logger = logging.getLogger()


class TerrainSpider(scrapy.Spider):
    today = datetime.date.today()
    name_variable = 'Terrain_'+ (today.strftime("%Y_%m_%d"))
    name = name_variable

    allowed_domains = ['terrain-construction.com']
    def start_requests(self):
        response1 = requests.get('https://www.terrain-construction.com/sitemap.1.xml').text
        liste_urls = re.findall("(https[^<>\"]+)", response1)
        for url in liste_urls:
            if '/search/' in url and url[-1].isdigit():
                yield Request (url, self.parse)
    def parse(self, response):
        articles = response.xpath('//div[@id="block-system-main"]/div[@class[contains(.,"article")]]')
        for article in articles:
            item = TerrainconstructionItem ()
            link = article.xpath('./div/div/div/div[@class="titre_annonce_liste"]/a/@href').extract_first()
            item["ANNONCE_LINK"] = link
            item["FROM_SITE"] = "https://www.terrain-construction.com/"
            item["ID_CLIENT"] = link.split("-")[-1].split(".")[0]
            item["ACHAT_LOC"] = "1"
            item["NOM"] = article.xpath('./div/div/div/div[@class="titre_annonce_liste"]/a/@title').extract_first()
            item["CP"] = article.xpath('./div/div/div/div[@class="titre_annonce_liste"]/a/h3/text()').extract_first().split(" ")[1]
            item["VILLE"] = article.xpath('./div/div/div/div[@class="titre_annonce_liste"]/a/h3/text()').extract_first().split(" ")[0].replace('-',' ')
            item["DEPARTEMENT"] = item["CP"][0:2]
            item["REGION"] = link.split('/')[-2].split('-')[0].replace('_',' ')
            surface = article.xpath('./div/div[@class="zone_grise_annonce_liste"]/span[@class="superficie"]/text()').extract_first()
            if surface is not None:
                item["M2_TOTALE"]= surface.split(":")[1].split("m")[0].strip()
            else:
                item["M2_TOTALE"]= ""
            prix = article.xpath('./div/div/span[@class="prix"]/text()').extract_first()
            if prix is not None:
                item["PRIX"] = prix.replace('€','').replace(' ','').strip()
            else:
                item["PRIX"]= ""
            prix_m = article.xpath('./div/div[@class="zone_grise_annonce_liste"]/span[@class="prix-my"]/text()').extract_first()
            if prix_m is not None:
                item["PRIX_M2"] = prix_m.split(":")[1].replace('€','').replace(' ','').strip()
            else:
                item["PRIX_M2"]= ""
            img = article.xpath('./div/div/div/div[@class="logo-annonce"]/img/@data-src').extract_first()
            dealer = img.split('/')[-1]
            if 'jpg' in dealer:
                item["MINI_SITE_ID"] = dealer.split('.')[0].replace('_','').replace('x','')
                item["PRO_IND"]="Y"
            else:
                item["MINI_SITE_ID"]= ""
                item["PRO_IND"]=""
            yield scrapy.Request(url=link,callback=self.parse_detail,dont_filter=True,meta={'item':item})
        next_page = response.xpath('//div[@class="item-list"]/ul/li[@class[contains(.,"pager-next")]]/a/@href').extract_first()
        if next_page is not None:
            next_page = 'https://www.terrain-construction.com' + next_page
            yield scrapy.Request(url=next_page,callback=self.parse)
    def parse_detail(self, response):
        item = response.meta['item']
        desc = response.xpath('//h4[@class="description"]/div/div/descendant-or-self::text()').extract_first()
        if desc is not None:
            item["ANNONCE_TEXT"] = desc.replace('</p>','').replace('<p>','').replace('<br />','').replace('<BR>','').replace('<br>','').replace(";","").replace('\n','').replace('\t','').replace('\r','')
        else:
            item["ANNONCE_TEXT"]= ""
        item["CATEGORIE"] =response.xpath('//div[@class[contains(.,"type-de-produit")]]/div/div/text()').extract_first().replace('seul','').strip()
        item["PHOTO"] = len(response.xpath('//div[@class="gallery-frame"]/ul/li').extract())
        yield item
