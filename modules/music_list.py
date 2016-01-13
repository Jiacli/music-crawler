# -*- coding: utf-8 -*-

class MusicList(object):

    def __init__(self, title='Unknown Title'):
        self.title = title
        self.size = 0
        self.songs = []

    def update(self):
        self.size = len(self.songs)
        rank = 1
        for song in self.songs:
            song.rank = rank
            rank += 1


class Song(object):

    def __init__(self, name, artists, album, id):
        self.name = name
        self.artists = artists
        self.album = album
        self.id = id
        self.rank = -1

    def display(self):
        item = u'No.{0} {1}({2}) - {3}'.format(self.rank, self.name,
            ','.join(self.artists), self.album)
        print item.encode("utf-8")

