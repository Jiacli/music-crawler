# -*- coding: utf-8 -*-

class MusicList(object):

    def __init__(self):
        self.title = None
        self.size = 0
        self.songs = []        


class Song(object):

    def __init__(self, name, artists, album, id):
        self.name = name
        self.artists = artists
        self.album = album
        self.id = id
        self.rank = -1

    def display(self):
        item = u'Name: {0}; Artists: {1}; Album: {2}; ID: {3}'.format(
            self.name, ','.join(self.artists), self.album, self.id)
        print item.encode("utf-8")

