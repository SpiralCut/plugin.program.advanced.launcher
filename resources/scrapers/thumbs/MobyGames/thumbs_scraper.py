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


# Get Game page
def _get_game_page_url(system,search):
    platform = _system_conversion(system)
    game = search.replace(' ', '+').lower()
    link = ''
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

# Thumbnails list scrapper
def _get_thumbnails_list(system,search,region,imgsize):
    covers = []
    results = []
    game_id_url = _get_game_page_url(system,search)

    try:
        url = game_id_url+'/cover-art'
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)

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
                            image = 'https://www.mobygames.com' + image.replace('(', '').replace(')', '')
                            covers.append([image.replace('/s/','/l/'),image,'Cover '+str(found)])
            if region == 'JP':
                if ('<span style="white-space: nowrap">Japan' in release):
                    release = re.findall('style="background-image:url(.*?);', release)
                    for image in release:
                        if 'front-cover' in image:
                            found = found+1
                            image = 'https://www.mobygames.com' + image.replace('(', '').replace(')', '')
                            covers.append([image.replace('/s/','/l/'),image,'Cover '+str(found)])
            if region == 'EU':
                if ('<span style="white-space: nowrap">Finland' in release) | ('<span style="white-space: nowrap">France' in release) | ('<span style="white-space: nowrap">Germany' in release) | ('<span style="white-space: nowrap">Italy' in release) | ('<span style="white-space: nowrap">The Netherlands' in release) | ('<span style="white-space: nowrap">Spain' in release) | ('<span style="white-space: nowrap">Sweden' in release) | ('<span style="white-space: nowrap">United Kingdom' in release):
                    release = re.findall('style="background-image:url(.*?);', release)
                    for image in release:
                        if 'front-cover' in image:
                            found = found+1
                            image = 'https://www.mobygames.com' + image.replace('(', '').replace(')', '')
                            covers.append([image.replace('/s/','/l/'),image,'Cover '+str(found)])
            if region == 'All':
                release = re.findall('style="background-image:url(.*?);', release)
                for image in release:
                    if 'front-cover' in image:
                        found = found+1
                        image = 'https://www.mobygames.com' + image.replace('(', '').replace(')', '')
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

