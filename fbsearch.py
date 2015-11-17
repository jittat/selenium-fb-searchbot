#!/usr/bin/env python3

import time
import sys
import requests
from selenium import webdriver

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
        print(link_url, r.status_code)


def main():
    if len(sys.argv)!=4:
        print('Usage: python fbsearch.py [facebook-url] [post-url] [post-param]')
        quit()
    find_post(*sys.argv[1:])


if __name__ == '__main__':
    main()
