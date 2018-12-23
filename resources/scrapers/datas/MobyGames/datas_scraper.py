# -*- coding: UTF-8 -*-

import re
import os
import urllib
from xbmcaddon import Addon

# Return Game search list
def _get_games_list(search):
    results = []
    display = []
    try:
        urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        f = urllib.urlopen('http://www.mobygames.com/search/quick?q='+search.replace(' ','+')+'&sFilter=1&sG=on')
        split_games = f.read()
        split_games = split_games.split('<div class="searchResult">')
        for games in split_games:
            if games.find('<div class="searchTitle">') <> -1:
                game_title = re.findall('<div class="searchTitle">Game: <a href="(.*?)">(.*?)</a>', games)
                if game_title:
                    split_versions = re.findall('nowrap"><a href="(.*?)">(.*?)</a> ', games)
                    if split_versions:
                        for version in split_versions:
                            game = {}
                            game["title"] = unescape(game_title[0][1].replace('&#x26;','&').replace('&#x27;',"'"))
                            game["id"] = version[0]
                            game["gamesys"] = version[1]
                            results.append(game)
                            display.append(game["title"]+" / "+game["gamesys"])
                    else:
                        game = {}
                        game["title"] = unescape(game_title[0][1].replace('&#x26;','&').replace('&#x27;',"'"))
                        one_version = re.findall('<span style="white-space: nowrap">(.*?) \(<em>', games)
                        if one_version:
                            game["id"] = game_title[0][0]
                            game["gamesys"] = one_version[0]
                            results.append(game)
                            display.append(game["title"]+" / "+game["gamesys"])
        return results,display
    except:
        return results,display

# Return 1st Game search
def _get_first_game(search,gamesys):
    platform = _system_conversion(gamesys)
    platform = platform.replace(' ','+')
    results = []
    try:
        urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        f = urllib.urlopen('http://www.mobygames.com/search/quick?q='+search.replace(' ','+')+'&p='+platform+'&sFilter=1&sG=on')
        split_games = f.read()
        split_games = split_games.split('<div class="searchResult">')
        for games in split_games:
            if games.find('<div class="searchTitle">') <> -1:
                game_title = re.findall('<div class="searchTitle">Game: <a href="(.*?)">(.*?)</a>', games)
                if game_title:
                    split_versions = re.findall('nowrap"><a href="(.*?)">(.*?)</a> ', games)
                    if split_versions:
                        for version in split_versions:
                            game = {}
                            game["title"] = unescape(game_title[0][1].replace('&#x26;','&').replace('&#x27;',"'"))
                            game["id"] = version[0]
                            game["gamesys"] = version[1]
                            results.append(game)
                    else:
                        game = {}
                        game["title"] = unescape(game_title[0][1].replace('&#x26;','&').replace('&#x27;',"'"))
                        one_version = re.findall('<span style="white-space: nowrap">(.*?) \(<em>', games)
                        if one_version:
                            game["id"] = game_title[0][0]
                            game["gamesys"] = one_version[0]
                            results.append(game)
        return results
    except:
        return results

# Return Game data
def _get_game_data(game_object):
    gamedata = {}
    gamedata["genre"] = ""
    gamedata["release"] = ""
    gamedata["studio"] = ""
    gamedata["plot"] = ""
    try:
        urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        f = urllib.urlopen(game_object['id'])
        page = f.read().replace('\r', '').replace('\n', '')
        game_genre = re.findall('<a href="https://www.mobygames.com/genre/(.*?)">(.*?)</a>', page)
        if game_genre:
            gamedata["genre"] = unescape(game_genre[0][1])
        game_release = re.findall('<a href="https://www.mobygames.com/(.*?)/release-info">(.*?)</a>', page)
        if game_release[1][1]:
            gamedata["release"] = game_release[1][1]
        game_studio = re.findall('Developed by(.*?)<a href="(.*?)">(.*?)</a>', page)
        if game_studio:
            gamedata["studio"] = unescape(game_studio[0][2])
        game_plot = re.findall('Description</h2>(.*?)<div class', page)
        if game_plot:
            p = re.compile(r'<.*?>')
            gamedata["plot"] = unescape(p.sub('', game_plot[0]))
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
                if result[3]:
                    platform = result[3]
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

