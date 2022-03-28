# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 11:23:54 2021

@author: Szymon
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import re


class Imdb_scraper(scrapy.Spider):
    
    name = "imdbspider"
    
    start_urls = [ f'https://www.imdb.com/list/ls058011111/?sort=list_order,asc&mode=detail&page={n}'\
                  for n in range(1,11)]
    
    custom_settings = {
        'DOWNLOAD_DELAY': '2.0',
        'ROBOTSTXT_OBEY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'USER_AGENT': 'My Bot (szymon19314@gmail.com)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json'
    }
    
    top_url = "https://www.imdb.com"
    
    def parse(self, response):
        
        self.logger.info('Got successful response from %s', response.url)
        soup =  BeautifulSoup(response.body, 'lxml')        
        links = [ self.top_url + link.a.get('href') for link 
                 in soup.find_all("h3", class_ = "lister-item-header")]
        names_surnames = [link.a.text.strip() for link 
                 in soup.find_all("h3", class_ = "lister-item-header")]
        famous_movie = [movie.a.text.strip() for movie 
                 in soup.find_all("p", class_ = "text-muted text-small")]
        profession = [ sex.text[:sex.text.rfind('|')].strip() for sex 
                      in soup.find_all("p", class_ = "text-muted text-small")]
        index = [ re.sub(r'\D','',i.text) for i 
                 in soup.find_all("span",class_="lister-item-index unbold text-primary")]
       
        for url in links[:]:
           yield scrapy.Request(url, self.parse_item,
                                meta={'link':links.pop(0), 
                                      'names_surnames':names_surnames.pop(0),
                                      'famous_movie': famous_movie.pop(0),
                                      'profession': profession.pop(0),
                                      'index': index.pop(0)
                                      }
                                )
            
    def parse_item(self, response):
        self.logger.info('Got successful response from %s', response.url)
        soup =  BeautifulSoup(response.body, 'lxml')
        birth = soup.find("div", id="name-born-info").text.split(' in\n')
        
        birth[0] = re.sub(r'Born:\s', '', birth[0])
        birth[0] = re.sub(r'(\n\s*)', '', birth[0])
        birth[1] = re.sub(r'(\s){2,}||\n$', '', birth[1])
        
        oscars = soup.find("span", class_="awards-blurb").text.strip()
        oscars = re.sub(r'[^0-9]','',oscars)
        
        number_of_acts = soup.find("div", id=["filmo-head-actor",
                                              "filmo-head-actress"]).text
        number_of_acts = re.sub(r'[^0-9]','',number_of_acts)
        profession = soup.find("div", id=["filmo-head-actor",
                                              "filmo-head-actress"]).a.text
        star_sign = soup.find("div",id="dyk-star-sign").text.strip()
        star_sign = re.sub(r'Star Sign:\s*','',star_sign)
        
        nickname = soup.find("div", id="dyk-nickname")
        try:
            nickname = re.sub(r'Nickname:\s*','',nickname.text.strip()) 
                       
        except AttributeError:
            nickname = ''

        height = soup.find("div", id="details-height").text
        height = re.sub(r'\nHeight:\n.*(\d.\d).*',r'\1',height)
  
        
        yield { 'index': response.meta.get('index'),
                'link': response.meta.get('link'),
                'names_surnames': response.meta.get('names_surnames'),
                'nickname': nickname,
                'date_of_birth': birth[0],
                'place_of_birth': birth[1],
                'height': height,
                'profession': profession,
                'famous_movie': response.meta.get('famous_movie'),
                'number_of_acts': number_of_acts,
                'oscars': oscars,
                'star_sign': star_sign
                
                
                }
        
process = CrawlerProcess()
process.crawl(Imdb_scraper)
process.start()

