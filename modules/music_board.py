# -*- coding: utf-8 -*-
import json
from music_list import MusicList, Song

class NeteaseBoard(object):
    def __init__(self):
        self.base_url='http://music.163.com/discover/toplist?id='
        self.prefix = './raw_webpages/netease-'
        self.save_path = './parsed_data/'
        self.seeds = {
            3778678: u"云音乐热歌榜",
            19723756: u"云音乐飙升榜",
            3779629: u"云音乐新歌榜",
            2884035: u"网易原创歌曲榜",
            71385702: u"云音乐ACG音乐榜",
            71384707: u"云音乐古典音乐榜",
            10520166: u"云音乐电音榜",
            112504: u"中国TOP排行榜（港台榜）",
            64016: u"中国TOP排行榜（内地榜）",
            21845217: u"KTV唛榜",
            60198: u"美国Billboard周榜",
            11641012: u"iTunes榜"
        }
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

    def parse_webpage(self, soup, seed, debug=False):
        title = unicode(soup.title.string)
        assert self.seeds[seed] in title
        mlist = MusicList(seed, self.seeds[seed])
        print 'Music Toplist:', mlist.title

        for meta in soup.find_all('meta'):
            if meta.get("name") == 'description':
                description = meta.get("content")
                break
        mlist.description = unicode(description)
        mlist.timestamp = description.split(u'：')[-1].split(u'（')[0]

        print 'Description:', mlist.description
        print 'Timestamp:', mlist.timestamp

        music_dict = self.get_music_info(soup)

        if debug:
            for k, v in music_dict.iteritems():
                v.display()

        for music in soup.select('div[id="song-list-pre-cache"] > ul > li > a'):
            name = unicode(music.stirng)
            id = int(music["href"].split("=")[-1])
            mlist.songs.append(music_dict[id])

        mlist.update()
        for song in mlist.songs:
            pass# song.display()

        mlist.save_to_file(self.save_path)



# class Musicboard(object):
#     def __init__(self):
#         pass

#     @abstractmethod
#     def parse_webpage(self, soup):
#         pass



