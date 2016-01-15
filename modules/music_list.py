# -*- coding: utf-8 -*-

import os

class MusicList(object):

    def __init__(self, seed, title='Unknown Title'):
        self.title = title
        self.seed = seed
        self.description = 'Unknown Description'
        self.timestamp = 'Unknown Timestamp'
        self.size = 0
        self.songs = []

    def update(self):
        self.size = len(self.songs)
        rank = 1
        for song in self.songs:
            song.rank = rank
            rank += 1

    def save_to_file(self, path):
        if not path.endswith('/'):
            path = path + '/'
        filename = u'{0}{1} ({2}).tsv'.format(path, self.title, self.timestamp)

        if os.path.exists(filename):
            print 'File {0} already exists.'
            return

        with open(filename, 'w') as f:
            # f.write(self.description.encode("utf-8"))
            # f.write('\n')
            f.write('Rank\tName\tArtists\tAlbum\n')
            for song in self.songs:
                s = u'{0}\t{1}\t{2}\t{3}\n'.format(song.rank, song.name,
                    ', '.join(song.artists), song.album)
                f.write(s.encode("utf-8"))



class Song(object):

    def __init__(self, name, artists, album, id):
        self.name = name
        self.artists = artists
        self.album = album
        self.id = id
        self.rank = -1

    def display(self):
        item = u'No.{0} {1}({2}) - {3}'.format(self.rank, self.name,
            ', '.join(self.artists), self.album)
        print item.encode("utf-8")

