#!/usr/bin/env python3

import time
import sys
import os
import yaml
import requests
import logging
import coloredlogs
from selenium import webdriver


logging.getLogger('requests').setLevel(logging.WARNING)
coloredlogs.DEFAULT_LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
coloredlogs.install(level=logging.INFO)

PAGE_LOAD_WAIT = 5


def find_post_links(url):
    links = []
    driver = webdriver.Chrome()
    driver.get(url)

    #print('waiting...')
    time.sleep(PAGE_LOAD_WAIT)

    results = driver.find_elements_by_css_selector(".userContentWrapper .fsm")
    for r in results:
        content_links = r.find_elements_by_css_selector("a._5pcq")
        if len(content_links) > 0:
            try:
                url = content_links[0].get_attribute('href')
                if url and url != '':
                    links.append(url)
            except:
                pass

    driver.close()
    return links


def find_post(url, post_url, post_param):
    links = find_post_links(url)
    for link_url in links:
        r = requests.post(post_url,
                          data={post_param: link_url})
        if r.status_code // 100 == 2:
            logging.info('%s %s', r.status_code, link_url)
        else:
            logging.warning('%s %s', r.status_code, link_url)


def find_posts(data):
    default = data.get('default', {})
    for search in data['searches']:
        for hashtag in search.get('hashtags', []):
            logging.info('hashtag: %s', hashtag)
            find_post('https://facebook.com/hashtag/{}'.format(hashtag),
                      search.get('post-url') or default.get('post-url'),
                      search.get('post-param') or default.get('post-param'))


def get_config(path=None):
    if path is None:
        basedir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(basedir, 'config.yaml')
    if not os.path.isfile(path):
        return {}
    return yaml.load(open(path))


def main():
    if len(sys.argv) == 4:
        find_post(*sys.argv[1:])
    elif len(sys.argv) == 1 and get_config():
        find_posts(get_config())
    else:
        print('Usage: ./fbsearch.py  --  has config file at ./config.yaml')
        print('Usage: ./fbsearch.py [facebook-url] [post-url] [post-param]')
    quit()


if __name__ == '__main__':
    main()
