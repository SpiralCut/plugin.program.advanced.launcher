# -*- coding: UTF-8 -*-

import os
import re
import urllib2
from xbmcaddon import Addon
import xbmcgui

__settings__ = Addon( id="plugin.program.advanced.launcher" )
__lang__ = __settings__.getLocalizedString

def __language__(string):
    return __lang__(string).encode('utf-8','ignore')
    
# Get Game first page
def _get_game_page_url(system,search):
    platform = _system_conversion(system)
    game = search.replace(' ', '+').lower()
    games = []
    try: 
        url = 'https://www.mobygames.com/search/quick?q='+game+'&p='+platform+'&sfilter=1&search=Go'
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
        games = f.read().replace('\r\n', '')
        games = re.findall('<div class="searchTitle">Game: <a href="(.*?)">(.*?)</a></div>',games)
        if games:
            return games[0][0]
    except:
        return ""

# Fanarts list scrapper
def _get_fanarts_list(system,search,imgsize):
    full_fanarts = []
    results = []
    game_id_url = _get_game_page_url(system,search)
    try:
        url = game_id_url+'/screenshots'
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
        game_page = f.read().replace('\r\n', '').replace('\n', '')
        results = re.findall('<div class="thumbnail-image-wrapper">(.*?)<a href="(.*?)" title=(.*?)style="background-image:url(.*?);', game_page)
        for index, line in enumerate(results):
            thumb_image = line[3].replace('(', '').replace(')', '')
            full_fanarts.append([line[1],'https://www.mobygames.com'+thumb_image,'Image '+str(index+1)])

        return full_fanarts
    except:
        return full_fanarts

# Get Fanart scrapper
def _get_fanart(image_url):
    return_url = ""
    try: 
        url = image_url
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
        image_page = f.read().replace('\r\n', '').replace('\n', '')
        results = re.findall('<div class="screenshot doubled">(.*?)<img(.*?) src="(.*?)"', image_page)
        if results:
            return_url = 'https://www.mobygames.com' + results[0][2]
        return return_url
    except:
        return

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

