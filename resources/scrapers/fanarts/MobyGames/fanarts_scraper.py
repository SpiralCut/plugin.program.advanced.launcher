# -*- coding: UTF-8 -*-

import os
import re
import urllib
from xbmcaddon import Addon

# Get Game first page
def _get_game_page_url(system,search):
    platform = _system_conversion(system)
    params = urllib.urlencode({'q': search.replace(' ','+'), 'p': platform, 'sFilter': '1', 'sG': 'on'})
    games = []
    try:
        urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        f = urllib.urlopen('http://www.mobygames.com/search/quick', params)
        games = f.read().replace('\r\n', '')
        games = re.findall('<div class="searchTitle">Game: <a href="(.*?)">(.*?)</a></div>',games)
        if games:
            return 'http://www.mobygames.com'+games[0][0]+'/'
    except:
        return ""

# Fanarts list scrapper
def _get_fanarts_list(system,search,imgsize):
    full_fanarts = []
    results = []
    game_id_url = _get_game_page_url(system,search)
    try:
        urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        f = urllib.urlopen(game_id_url+'screenshots')
        game_page = f.read().replace('\r\n', '').replace('\n', '')
        results = re.findall('style="background-image:url(.*?);', game_page)
        for index, line in enumerate(results):
            line = line.replace('(', '').replace(')', '')
            full_fanarts.append(['http://www.mobygames.com'+line.replace('/s/','/l/'),'http://www.mobygames.com'+line,'Image '+str(index+1)])
        return full_fanarts
    except:
        return full_fanarts

# Get Fanart scrapper
def _get_fanart(image_url):
    return image_url

# Game systems DB identification
def _system_conversion(system_id):
    try:
        rootDir = Addon( id="plugin.program.advanced.launcher" ).getAddonInfo('path')
        if rootDir[-1] == ';':rootDir = rootDir[0:-1]
        resDir = os.path.join(rootDir, 'resources')
        scrapDir = os.path.join(resDir, 'scrapers')
        csvfile = open( os.path.join(scrapDir, 'gamesys'), "rb")
        conversion = []
        for line in csvfile.readlines():
            result = line.replace('\n', '').replace('"', '').split(',')
            if result[0].lower() == system_id.lower():
                if result[3]:
                    platform = result[3]
                    return platform
    except:
        return ''

