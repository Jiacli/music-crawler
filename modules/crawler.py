# -*- coding: utf-8 -*-

import os, json, time
from bs4 import BeautifulSoup
from urllib2 import urlopen, Request, URLError, HTTPError

def make_url(url_base, params):
    params_list = []
    for k, v in params.iteritems():
        params_list.append('{0}={1}'.format(k, v))
    return url_base + '&'.join(params_list)


def request_url(url):
    """
    Open URL with dummy headers
    """
    dummy_header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, \
            image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 \
            Safari/537.36'
    }

    try:
        req = Request(url, headers=dummy_header)
        response = urlopen(req)
        data = response.read()
    except URLError, e:
        if hasattr(e, 'code'):
            print 'Error code:', e.code, '. Cannot finish request.'
        elif hasattr(e, 'reason'):
            print 'Request failed:', e.reason, 'Cannot connect to server.'
    else:
        return data


def make_soup(url, filename='undefined', persist=False):
    """
    Create BeautifulSoup object for requested URL
    """

    if 0: #os.path.exists(filename):
        with open(filename, 'r') as f:
            data = f.read()
    else:
        data = request_url(url)
        # write to file for analysis
        with open(filename, 'w') as f:
            f.write(data)

    return BeautifulSoup(data)


def crawl_music_toplist(board):
    for seed in board.seeds.keys():
        url = board.get_req_url(seed)
        print 'crawling:', url
        soup = make_soup(url, filename=board.prefix+str(seed))
        if soup is None:
            print 'Cannot make soup for url:', url
            continue
        board.parse_webpage(soup, seed)

