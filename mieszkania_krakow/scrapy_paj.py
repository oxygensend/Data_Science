# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import sys
import re
import requests
import urllib.parse

class OtodomSpider(scrapy.Spider):
    
    name = "OTOspider"
    
    start_urls = [f'https://www.otodom.pl/sprzedaz/mieszkanie/krakow/?search%5Bregion_id%5D=6&search%5Bcity_id%5D=38&page={n}' 
                  for n in range(300)]
    
    custom_settings = {
        'DOWNLOAD_DELAY': '1.5',
        'ROBOTSTXT_OBEY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'USER_AGENT': 'My Bot (szymon19314@gmail.com)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json'
    }
    
    top_url = 'https://www.otodom.pl'


    def parse(self, response):
        
        self.logger.info('Got successful response from %s', response.url)
        soup =  BeautifulSoup(response.body, 'lxml')
        titles = [flat.text  for flat in soup.find_all("header", class_="offer-item-header")]
        links = [link.find('a').get('href') for link in soup.find_all("header", class_="offer-item-header")
                  ]
        prices = [flat.text for flat in soup.find_all("li",
                   class_ = "offer-item-price")]

        for url in links[:]:
            yield scrapy.Request(url, self.parse_item ,
                                 meta={'link':links.pop(0),
                                     'title': titles.pop(0),
                                     'price': prices.pop(0)
                                      }
                                )
        
        
        
    def parse_item(self, response):
        
        self.logger.info('Got successful response from %s', response.url)
        soup = BeautifulSoup(response.body, 'lxml')
        
        title = response.meta.get('title')
        link = response.meta.get('link')
        price = response.meta.get('price')
        

        location = soup.find('a',class_='css-1qz7z11 e1nbpvi61').text
        try:
            surface = soup.find('div', class_='css-1ytkscc ev4i3ak0').text
        except AttributeError:
            surface = ''
        try:
            rooms = soup.find('div', {"class":"css-18h1kfv ev4i3ak3","aria-label":"Liczba pokoi"}).contents[-1].text
        except AttributeError:
            rooms = ''
        try:
            market = soup.find('div', {"class":"css-18h1kfv ev4i3ak3","aria-label":"Rynek"}).contents[-1].text
        except AttributeError:
            market = ''
        try:  
            level = soup.find('div', {"class":"css-18h1kfv ev4i3ak3","aria-label":"Piętro"}).contents[-1].text
        except AttributeError:
            level = ''
        try:
            year= soup.find('div', {"class":"css-18h1kfv ev4i3ak3","aria-label":"Rok budowy"}).contents[-1].text
        except AttributeError:
            year = ''
        try:
            fin_condition= soup.find('div', {"class":"css-18h1kfv ev4i3ak3","aria-label":"Stan wykończenia"}).contents[-1].text
        except AttributeError:
            fin_condition = ''
        try:
            type_of_bld = soup.find('div', {"class":"css-18h1kfv ev4i3ak3","aria-label":"Rodzaj zabudowy"}).contents[-1].text
        except AttributeError:
            type_of_bld = ''
        try:
            owner = soup.find('div', {"class":"css-18h1kfv ev4i3ak3","aria-label":"Forma własności"}).contents[-1].text
        except AttributeError:
            owner = ''
        try:
            desc = soup.find('section', {"class":'css-8frsuk e1r1048u3'}).text
        except AttributeError:
            desc = ''
        try:
            own = soup.find('div', {"class": 'css-r698rx efr87w020'}).text
        except AttributeError:
            own = ''

        # Pobieranie współrzędnych geograficznych
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(location) +'?format=json'
        response = requests.get(url).json()
        lat = response[0]["lat"]
        lon = response[0]["lon"]
                
        yield { "link": link, 
                "title":title, 
                "price": price, 
                "localisation": location,
                'surface': surface,
                'rooms':rooms,
                'market': market,
                'level': level,
                'year': year,
                'finish_condition': fin_condition,
                'type_of_bulding': type_of_bld,
                'property_type': owner,
                'describtion': desc,
                'own': own,
                'lon': lon,
                'lat': lat
                } 
        
  
process = CrawlerProcess()
process.crawl(OtodomSpider)
process.start()