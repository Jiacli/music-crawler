# -*- coding: utf-8 -*-
import json
from music_list import MusicList, Song

class NeteaseBoard(object):
    def __init__(self):
        self.base_url='http://music.163.com/discover/toplist?id='
        self.prefix = 'netease-'
        self.seeds =[
            3778678,  # 云音乐热歌榜
            # 19723756, # 云音乐飙升榜
        ]
        self.music_lists = []

    def get_music_info(self, soup):
        textarea = json.loads(soup.textarea.string)
        music_dict = {}

        for song in textarea:
            name = unicode(song["name"])
            id = song["id"]
            artists = []
            try:
                album = unicode(song["album"]["name"])
            except Exception, e:
                album = u'Unknown'            
            for artist in song["artists"]:
                artists.append(unicode(artist["name"]))

            # create a music entry & save into dict
            entry = Song(name, artists, album, id)
            music_dict[id] = entry

        return music_dict

    def parse_webpage(self, soup, debug=False):
        mlist = MusicList()
        mlist.title = unicode(soup.title.string)
        print 'Music Toplist:', mlist.title
        music_dict = self.get_music_info(soup)
        
        if debug:
            for k, v in music_dict.iteritems():
                v.display()

        for music in soup.select('div[id="song-list-pre-cache"] > ul > li > a'):
            name = unicode(music.stirng)
            id = int(music["href"].split("=")[-1])
            mlist.songs.append(music_dict[id])
        # print soup.select('a[href^="/song?id="]')

        for song in mlist.songs:
            song.display()



# class Musicboard(object):
#     def __init__(self):
#         pass

#     @abstractmethod
#     def parse_webpage(self, soup):
#         pass



