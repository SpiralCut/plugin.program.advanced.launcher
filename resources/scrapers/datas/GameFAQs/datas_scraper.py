# -*- coding: UTF-8 -*-

import re
import os
import urllib2
from xbmcaddon import Addon
import xbmcgui


__settings__ = Addon( id="plugin.program.advanced.launcher" )
__lang__ = __settings__.getLocalizedString

def __language__(string):
    return __lang__(string).encode('utf-8','ignore')
   


# Return Game search list
def _get_games_list(search):
    display=[]
    results=[]
    try:
        url = 'http://www.gamefaqs.com/search/index.html?platform=0&game='+search.replace(' ','+')+''
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
        gets = {}
        gets = f.read().replace('\r\n', '')
        gets = gets.split('<div class="search_result">')
        for get in gets:
            if get.find('<div class="sr_product_name">') <> -1:
                gameplatforms = {}
                title = {}
                info = {}
                gameplatforms = re.findall('<div class="sr_product_name"><a class="sevent" data-row=".*?" data-col="(.*?)" href="(.*?)">(.*?)</a>', get)                
                title = re.findall('<div class="sr_name"><a class="sevent" data-row=".*?" data-col=".*?" href=".*?">(.*?)</a></div>', get)
                info =  re.findall('<div class="sr_info">(.*?), (.*?), (.*?)</div>', get)
                for gameplatform in gameplatforms:
                    game = {}
                    gamesystem = gameplatform[2]
                    game["id"] =  'http://www.gamefaqs.com'+gameplatform[1]
                    game["title"] =  unescape(title[0])
                    game["gamesys"] = gamesystem
                    game["studio"] = unescape(info[0][0])
                    game["genre"] = unescape(info[0][1])
                    game["release"] = unescape(info[0][2])
                    results.append(game)
                    display.append(game["title"]+" / "+game["gamesys"])
        return results,display
    except urllib2.HTTPError, e:
        if e.reason == "Unauthorized":
            ret = xbmcgui.Dialog().yesno(__language__( 30196 ), __language__( 30197 ), __language__( 30198 ), __language__( 30199 ),__language__( 30207 ), __language__( 30208 ))  
            if ret:
                return results,display
            else:
                results, display = _get_games_list(search)
        return results,display
    except:
        return results,display

# Return 1st Game search
def _get_first_game(search,gamesys):
    platform = _system_conversion(gamesys).replace(' ','+')
    results = []
    try:
        url = 'http://www.gamefaqs.com/search/index.html?platform='+platform+'&game='+search.replace(' ','+')+''
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
        gets = {}
        gets = f.read().replace('\r\n', '')
        gets = gets.split('<div class="search_result">')
        for get in gets:
            if get.find('<div class="sr_product_name">') <> -1:
                gameplatforms = {}
                title = {}
                info = {}
                gameplatforms = re.findall('<div class="sr_product_name"><a class="sevent" data-row=".*?" data-col="(.*?)" href="(.*?)">(.*?)</a>', get)                
                title = re.findall('<div class="sr_name"><a class="sevent" data-row=".*?" data-col=".*?" href=".*?">(.*?)</a></div>', get)
                info =  re.findall('<div class="sr_info">(.*?), (.*?), (.*?)</div>', get)
                for gameplatform in gameplatforms:
                    game = {}
                    gamesystem = gameplatform[2]
                    game["id"] =  'http://www.gamefaqs.com'+gameplatform[1]
                    game["title"] =  unescape(title[0])
                    game["gamesys"] = gamesys
                    game["studio"] = unescape(info[0][0])
                    game["genre"] = unescape(info[0][1])
                    game["release"] = unescape(info[0][2])
                    results.append(game)
        return results
    except urllib2.HTTPError, e:
        if e.reason == "Unauthorized":
            ret = xbmcgui.Dialog().yesno(__language__( 30196 ), __language__( 30197 ), __language__( 30198 ), __language__( 30199 ),__language__( 30207 ), __language__( 30208 ))  
            if ret:
                return results
            else:
                results = _get_first_game(search,gamesys)
        return results
    except:
        return results

# Return Game data
def _get_game_data(game_object):
    print game_object['id']
    gamedata = {}
    gamedata["genre"] = game_object["genre"]
    gamedata["release"] = game_object["release"]
    gamedata["studio"] = game_object["studio"]
    gamedata["plot"] = ""
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
		
		#Only need to fetch plot details
        req = urllib2.Request(game_object['id'], headers=hdr)
        f = urllib2.urlopen(req)
        page = f.read().replace('\r', '').replace('\n', '')
        game_plot = re.findall('<div class="desc">(.*?)</div>', page)
        if game_plot:
            gamedata["plot"] = unescape(game_plot[0])
        return gamedata
    except urllib2.HTTPError, e:
        if e.reason == "Unauthorized":
            ret = xbmcgui.Dialog().yesno(__language__( 30196 ), __language__( 30197 ), __language__( 30198 ), __language__( 30199 ),__language__( 30207 ), __language__( 30208 ))  
            if ret:
                return gamedata
            else:
                gamedata = _get_game_data(game_object)
        return gamedata
    except:
        return gamedata  

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
        
def unescape(s):
    s = s.replace('<br />',' ')
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    s = s.replace("&#039;","'")
    s = s.replace('<br />',' ')
    s = s.replace('&quot;','"')
    s = s.replace('&nbsp;',' ')
    s = s.replace('&#x26;','&')
    s = s.replace('&#x27;',"'")
    s = s.replace('&#xB0;',"°")
    return s

