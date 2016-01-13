# -*- coding: utf-8 -*-

from modules.crawler import crawl_music_toplist
from modules.music_board import NeteaseBoard



if __name__ == "__main__":
    # NetEase Cloud Music
    netease = NeteaseBoard()
    crawl_music_toplist(netease)