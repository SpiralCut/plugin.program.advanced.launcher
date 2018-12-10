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
    results = []
    link = ''
    try:
        url = 'http://www.gamefaqs.com/search/index.html?platform='+platform+'&game='+game+'&s=s'
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
        gets = {}
        gets = f.read().replace('\r\n', '')
        gets = gets.split('<div class="search_result">')
        counter = 0
        for get in gets:
            if get.find('<div class="sr_product_name">') <> -1:
                gameplatforms = {}
                title = {}
                info = {}
                counter = counter + 1
                gameplatforms = re.findall('<div class="sr_product_name"><a class="sevent" data-row=".*?" data-col="(.*?)" href="(.*?)">(.*?)</a>', get)                
                title = re.findall('<div class="sr_name"><a class="sevent" data-row=".*?" data-col=".*?" href=".*?">(.*?)</a></div>', get)
                info =  re.findall('<div class="sr_info">(.*?), (.*?), (.*?)</div>', get)
                for gameplatform in gameplatforms:
                    games = {}
                    if platform == gameplatform[2]:
                        if gameplatform[1]:
#                       Immediately return game link if platform matches and it is in the top 3 results
                            if counter <= 3:
                                link = gameplatform[1]
                                return link
                    else:
                        if gameplatform[1]:
                            if link == "":
                                link = gameplatform[1]
        return link
    except urllib2.HTTPError, e:
        if e.reason == "Unauthorized":
            ret = xbmcgui.Dialog().yesno(__language__( 30196 ), __language__( 30197 ), __language__( 30198 ), __language__( 30199 ),__language__( 30207 ), __language__( 30208 ))  
            if ret:
                return link
            else:
                link = _get_game_page_url(system,search)
        return link
    except:
        return link

# Thumbnails list scrapper
def _get_thumbnails_list(system,search,region,imgsize):
#   Gamesystem,title,self.region,imagesize
    covers = []
    game_id_url = _get_game_page_url(system,search)
    try:
        url = 'http://www.gamefaqs.com'+game_id_url+'/images'
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
        page = {}
        page = f.read().replace('\r\n', '')
        results =  re.findall('<div class="img boxshot"><a href="(.*?)"><img class="img100 imgboxart" src="(.*?)" alt=".*?" /></a><div class="region">(.*?)</div>.*?</div>', page)
        for result in results:
            result = [result[1].replace('_thumb.jpg', '_front.jpg'), result[1], result[2]]
            if (region <> "All" ):
                if region in result[2]:
                    covers.append(result)
            else:
                covers.append(result)
        return covers
    except urllib2.HTTPError, e:
        if e.reason == "Unauthorized":
            ret = xbmcgui.Dialog().yesno(__language__( 30196 ), __language__( 30197 ), __language__( 30198 ), __language__( 30199 ),__language__( 30207 ), __language__( 30208 ))  
            if ret:
                return covers
            else:
                covers = _get_thumbnails_list(system,search,region,imgsize)
        return covers
    except:
        return covers

# Get Thumbnail scrapper
def _get_thumbnail(image_url):
    try:
        return image_url
    except:
        return ""

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
                if result[2]:
                    platform = result[2]
                    return platform
    except:
        return ''
