# -*- coding: UTF-8 -*-

import os
import re
import urllib
from xbmcaddon import Addon


# Get Game page
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

# Thumbnails list scrapper
def _get_thumbnails_list(system,search,region,imgsize):
    covers = []
    results = []
    game_id_url = _get_game_page_url(system,search)
    try:
        urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
        f = urllib.urlopen(game_id_url+'cover-art')
        page = f.read().replace('\r\n', '').replace('\n', '')
        page = page.split('<div class="coverHeading">')
        found = 0
        for index, release in enumerate(page):
            if region == 'US':
                if ('<span style="white-space: nowrap">Canada' in release) | ('<span style="white-space: nowrap">United States' in release):
                    release = re.findall('style="background-image:url(.*?);', release)
                    for image in release:
                        if 'front-cover' in image:
                            found = found+1
                            image = 'http://www.mobygames.com/' + image.replace('(', '').replace(')', '')
                            covers.append([image.replace('/s/','/l/'),image,'Cover '+str(found)])
            if region == 'JP':
                if ('<span style="white-space: nowrap">Japan' in release):
                    release = re.findall('style="background-image:url(.*?);', release)
                    for image in release:
                        if 'front-cover' in image:
                            found = found+1
                            image = 'http://www.mobygames.com/' + image.replace('(', '').replace(')', '')
                            covers.append([image.replace('/s/','/l/'),image,'Cover '+str(found)])
            if region == 'EU':
                if ('<span style="white-space: nowrap">Finland' in release) | ('<span style="white-space: nowrap">France' in release) | ('<span style="white-space: nowrap">Germany' in release) | ('<span style="white-space: nowrap">Italy' in release) | ('<span style="white-space: nowrap">The Netherlands' in release) | ('<span style="white-space: nowrap">Spain' in release) | ('<span style="white-space: nowrap">Sweden' in release) | ('<span style="white-space: nowrap">United Kingdom' in release):
                    release = re.findall('style="background-image:url(.*?);', release)
                    for image in release:
                        if 'front-cover' in image:
                            found = found+1
                            image = 'http://www.mobygames.com/' + image.replace('(', '').replace(')', '')
                            covers.append([image.replace('/s/','/l/'),image,'Cover '+str(found)])
            if region == 'All':
                release = re.findall('style="background-image:url(.*?);', release)
                for image in release:
                    if 'front-cover' in image:
                        found = found+1
                        image = 'http://www.mobygames.com/' + image.replace('(', '').replace(')', '')
                        covers.append([image.replace('/s/','/l/'),image,'Cover '+str(found)])
        return covers
    except:
        return covers

# Get Thumbnail scrapper
def _get_thumbnail(image_url):
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

