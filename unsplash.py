import requests
import json
import logging
import os
import re
import time

from urllib.request import urlretrieve
from bs4 import BeautifulSoup


class ExceededQuantity(Exception):

    def __init__(self, count):
        self.count = count


logging.basicConfig(level=logging.INFO)


class Unsplash:

    urls = {}  # where contain ulrs

    def __init__(self, folder_path):
        """Contructor will create a corpus to contain your queries"""
        self.path = folder_path
        if os.path.exists(self.path) == False:
            os.mkdir(self.path)
        logging.info('Have created "{}" folder'.format(self.path))

    def listPhotos(self, page=1, per_page=10, order_by='lastest', option='regular'):
        # Get a single page from the list of all photos
        params = {'page': page, 'per_page': per_page, 'order_by': order_by}
        r = requests.get('https://unsplash.com/napi/photos', params=params)
        logging.info('REQUEST: page {}, per_page {}, order_by {}'.format(
            page, per_page, order_by))
        if r.status_code == 200:
            # get urls based on quality
            j = json.loads(r.text)
            for i in j:
                name = i['id']
                url = i['urls'][option]
                self.urls[name] = url
                logging.info('{} --> urls'.format(name))
        return (r.status_code, len(j))

    def randomPhotos(self, count=1, option='regular'):
        """count The number of photos to return. (Default: 1; max: 30)"""
        params = {'count': count}
        r = requests.get(
            'https://unsplash.com/napi/photos/random', params=params)
        logging.info('REQUEST: Random count {}'.format(count))
        if r.status_code == 200:
            j = json.loads(r.text)
            for i in j:
                name = i['id']
                url = i['urls'][option]
                self.urls[name] = url
                logging.info('{} --> urls'.format(name))
        return (r.status_code, len(j))

    def searchPhotos(self, query, page=1, per_page=10, option='regular'):
        # Get a single page of photo results for a query
        params = {'query': query, 'page': page, 'per_page': per_page}
        r = requests.get(
            'https://unsplash.com/napi/search/photos', params=params)
        logging.info('REQUEST: query {}, page {}, per_page {}'.format(
            query, page, per_page))
        if r.status_code == 200:
            # get urls based on quality
            j = json.loads(r.text)
            logging.info(
                'RESPONSE: query {} have {} result(s)'.format(query, j['total']))
            if j['total'] == 0:
                return (r.status_code, j['total'])
            # get list images
            results = j['results']
            for i in results:
                name = i['id']
                url = i['urls'][option]
                self.urls[name] = url
                logging.info('{} --> urls'.format(name))
        return (r.status_code, j['total'])

    def download(self, wait_time=2):
        # Download images based on self.urls
        """Download images from urls\n
        `urls: {'name1':'url1','name2':'url2'}`"""
        logging.info(
            'Start download images from urls ({} items)'.format(len(self.urls)))
        for name, url in self.urls.items():
            time.sleep(wait_time)
            urlretrieve(url, self.path+'/'+name+'.jpg')
            logging.info('DOWNLOAD: {} OK'.format(name))
        return 0


class GraphicRiver:

    listUrls = []

    def __init__(self, folder_path):
        """Contructor will create a corpus to contain your queries"""
        self.path = folder_path
        if os.path.exists(self.path) == False:
            os.mkdir(self.path)

    def __has_a_http_jpg(self, tag):
        # check image's link is https://www.somthing.jpg
        if (tag['class'] == 'is-hidden') and (tag.name == 'a') and (('.jpg' == tag['href'][-4:len(tag['href'])])or('.JPG' == tag['href'][-4:len(tag['href'])])):
            return True

    def getUrls(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            list_tag_a = soup.find_all(
                self.__has_a_http_jpg)  # get link to download
            for i in list_tag_a:
                self.listUrls.append(i['href'])
            return len(list_tag_a)

    def download(self, how_much, wait_time=0):
        check = 0
        for i in self.listUrls:
            url_split = i.split('/')
            name = url_split[6]
            urlretrieve(i, self.path+'/'+name)
            check += 1
            if how_much and check == how_much:
                break
        return check

if __name__ == '__main__':
    a = Unsplash('Dogs')
    a.searchPhotos('dog')
    a.download()
