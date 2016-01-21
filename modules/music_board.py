# -*- coding: utf-8 -*-
import json, time
from music_list import MusicList, Song
from crawler import make_url, request_url

class NeteaseBoard(object):
    def __init__(self):
        self.base_url='http://music.163.com/discover/toplist?id='
        self.prefix = './raw_webpages/netease-'
        self.save_path = './parsed_data/netease/'
        self.seeds = {
            3778678: u"云音乐热歌榜",
            19723756: u"云音乐飙升榜",
            3779629: u"云音乐新歌榜",
            # 2884035: u"网易原创歌曲榜",
            # 71385702: u"云音乐ACG音乐榜",
            # 71384707: u"云音乐古典音乐榜",
            # 10520166: u"云音乐电音榜",
            # 112504: u"中国TOP排行榜（港台榜）",
            # 64016: u"中国TOP排行榜（内地榜）",
            # 21845217: u"KTV唛榜",
            # 60198: u"美国Billboard周榜",
            # 11641012: u"iTunes榜"
        }
        self.music_lists = []

    def get_req_url(self, seed):
        return self.base_url + str(seed)

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

        for song in soup.select('div[id="song-list-pre-cache"] > ul > li > a'):
            name = unicode(song.stirng)
            id = int(song["href"].split("=")[-1])
            mlist.songs.append(music_dict[id])

        mlist.update()
        # for song in mlist.songs:
        #     song.display()
        mlist.save_to_file(self.save_path)


class TencentBoard(object):
    def __init__(self):
        self.base_url = ''
        self.prefix = './raw_webpages/qqmusic-'
        self.save_path = './parsed_data/qqmusic/'
        self.seeds = {
            26: (u"巅峰榜·热歌", 'weekly'),
            # 4: (u"巅峰榜·流行指数", 'daily'),
            # 27: (u"巅峰榜·新歌", 'daily'),
        }

        self.music_lists = []

    def get_req_url(self, seed):
        url_base = 'http://i.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?'
        params = dict(
            page="detail",
            type="top",
            topid=seed,
            format="html",
            tpl=20
        )
        return make_url(url_base, params)

    def get_list_data(self, seed):
        _, freq = self.seeds[seed]
        if freq == 'weekly':
            timestamp = time.strftime('%Y_%W', time.localtime())
            timestamp = '2015_32'
        elif freq == 'daily':
            timestamp = time.strftime('%Y-%m-%d', time.localtime())

        print 'Used time:', timestamp
        url_base = 'http://i.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?'
        params = dict(
            topid=seed,
            date=timestamp,
            page="detail",
            type="top",
            tpl=20,
            g_tk=5381,
            loginUin=0,
            hostUin=0,
            format="json",
            inCharset="GB2312",
            outCharset="utf-8",
            notice=0,
            platform="yqq",
            needNewCode=0,
        )

        url = make_url(url_base, params)
        data_json = request_url(url)

        try:
            data = json.loads(data_json)
        except Exception, e:
            data = None

        return data, timestamp


    def parse_webpage(self, soup, seed, debug=False):
        title = unicode(soup.title.string)
        assert self.seeds[seed][0] in title
        mlist = MusicList(seed, self.seeds[seed][0])
        print 'Music Toplist:', mlist.title

        data, timestamp = self.get_list_data(seed)
        if not data:
            print 'Music top list is unavailable for', timestamp
            return

        # with open('qqmusic.json', 'w') as f:
        #     f.write(json.dumps(data, indent=4))
        mlist.timestamp = data["date"]
        for song in data["songlist"]:
            name = unicode(song["data"]["songname"])
            album = unicode(song["data"]["albumname"])
            artists = []
            for artist in song["data"]["singer"]:
                artists.append(unicode(artist["name"]))
            id = song["data"]["songid"]
            mlist.songs.append(Song(name, artists, album, id))

        mlist.update()
        mlist.save_to_file(self.save_path)









# class Musicboard(object):
#     def __init__(self):
#         pass

#     @abstractmethod
#     def parse_webpage(self, soup):
#         pass



