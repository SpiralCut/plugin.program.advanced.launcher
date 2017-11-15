# -*- coding: UTF-8 -*-

import xbmc
import os
import re
import urllib
import urllib2


# Thumbnails list scrapper
def _get_fanarts_list(system,search,imgsize):
    qdict = {'q':search + " Screenshot OR Fanart " + system,'tbm':'isch'}
    query = urllib.urlencode(qdict)
    url = 'https://www.google.com/search?' + query + '&tbs=' + imgsize + '&dcr=0'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
    covers = []
    results = []
    try:
        req = urllib2.Request(url, headers=hdr)
        f = urllib2.urlopen(req)
        search_results = {}
        search_results = f.read()
        results =  re.findall('<div jsname=".*?" class="rg_meta notranslate">.*?"ou":"(.*?)",.*?"tu":"(.*?)".*?}</div>', search_results)
        for index, images in enumerate(results):
            covers.append((images[0],images[0],"Image "+str(index+1)))
        return covers
    except:
        return covers

# Get Thumbnail scrapper
def _get_fanart(image_url):
     return image_url

