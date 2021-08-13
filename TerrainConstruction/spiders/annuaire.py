# -*- coding: utf-8 -*-
import scrapy
from TerrainConstruction.items_ann import TerrainconstructionItem
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
    name_variable = 'annuaire_'+ (today.strftime("%Y_%m_%d"))
    name = name_variable

    allowed_domains = ['terrain-construction.com']
    start_urls = ['https://www.terrain-construction.com/search/professionnels/-/18_Constructeur_traditionnel-21_Constructeur_bois-1_Agence_immobiliere-2_Lotisseur']
    def parse(self, response):
        articles = response.xpath('//div[@id="block-system-main"]/div[@class[contains(.,"article")]]')
        for article in articles:
            item = TerrainconstructionItem ()
            item["MINI_SITE_URL"] = "https://www.terrain-construction.com" + article.xpath('./div/div/a/@href').extract_first()
            item["MINI_SITE_ID"] = article.xpath('./div/div/a/@href').extract_first().split('-u_')[1].split('-')[0]
            item["AGENCE_NOM"] = article.xpath('./div[@class="group-middle"]/div[@class="nom-pro"]/text()').extract_first()
            adresse = article.xpath('./div[@class="group-middle"]/div[@id="adresse-pro"]').extract_first()
            adresse = adresse.replace('<div id="adresse-pro">','').replace('</div>','').replace('\n', ' ')
            n = adresse.split('<br>')[1].strip().split(' ')
            if len(n) > 1:
                item["AGENCE_CP"] = adresse.split('<br>')[1].strip().split(' ')[0]
                item["AGENCE_VILLE"] = ''.join(adresse.split('<br>')[1].strip().split(' ')[1:])
                item["AGENCE_DEPARTEMENT"] = item["AGENCE_CP"][0:2]
                item["AGENCE_ADRESSE"] = adresse.replace('<br>','').replace(";","")
            else:
                item["AGENCE_CP"] = ""
                item["AGENCE_VILLE"] = ""
                item["AGENCE_DEPARTEMENT"] = ""
                item["AGENCE_ADRESSE"] = ""
            item["WEBSITE"] = article.xpath('./div[@class="group-right"]/div[@class="site-cons"]/span/a/@href').extract_first()
            yield item
        next_page = response.xpath('//div[@class="item-list"]/ul/li[@class[contains(.,"pager-next")]]/a/@href').extract_first()
        if next_page is not None:
            next_page = 'https://www.terrain-construction.com' + next_page
            yield scrapy.Request(url=next_page,callback=self.parse)
