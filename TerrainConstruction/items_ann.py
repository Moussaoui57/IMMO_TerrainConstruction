# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TerrainconstructionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    MINI_SITE_URL = scrapy.Field()
    MINI_SITE_ID = scrapy.Field() 
    AGENCE_NOM= scrapy.Field() 
    AGENCE_ADRESSE= scrapy.Field() 
    AGENCE_CP= scrapy.Field() 
    AGENCE_VILLE= scrapy.Field() 
    AGENCE_DEPARTEMENT= scrapy.Field() 
    WEBSITE= scrapy.Field() 
    
