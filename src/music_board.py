# -*- coding: utf-8 -*-
import json
from music_list import MusicList, MusicEntry

class NeteaseBoard(object):
    def __init__(self):
        self.base_url='http://music.163.com/discover/toplist?id='
        self.prefix = 'netease-'
        self.seeds =[
            3778678,  # 云音乐热歌榜
            19723756, # 云音乐飙升榜
        ]
        self.music_list = []

    def parse_webpage(self, soup):
        print json.dumps(json.loads(soup.textarea.string)[0], indent=4)
        print 'page title:', soup.title.string



# class Musicboard(object):
#     def __init__(self):
#         pass

#     @abstractmethod
#     def parse_webpage(self, soup):
#         pass



