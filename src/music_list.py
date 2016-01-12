# -*- coding: utf-8 -*-

class MusicList(object):

    def __init__(self):
        self.name = None
        self.size = 0
        self.entries = []        


class MusicEntry(object):

    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
