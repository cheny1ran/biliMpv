#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# author: ewnit <chenyr626@gmail.com>

import urllib2
import urllib
import re
import sys
import hashlib
import zlib
import os

biliUrl = 'http://www.bilibili.com/video/av{av}'
ifUrl = 'http://interface.bilibili.com/playurl?&cid={cid}&from=miniplay&player=1&sign={sign}'
pattern = re.compile(r'http:/[a-z0-9A-Z_\.?=&/-]+&rate=0')
headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, sdch',
    # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    # 'Host': 'www.bilibili.com',
    # 'Pragma': 'no-cache',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
}


class bilivideo:
    # appkey and secretkey from you-get: https://github.com/soimort/you-get
    appkey = 'f3bb208b3d081dc8'
    secretkey = '1c15888dc316e05a15fdd0a02ed6584f'
    cid = ''
    av = ''

    def __init__(self, av):
        if av.find('av') > -1:
            av = av[2:]
        self.av = av

    def getSign(self):
        return (hashlib.md5(
            'cid={cid}&from=miniplay&player=1{secretkey}'.format(cid = self.cid, secretkey = self.secretkey))).hexdigest()

    def getCid(self):
        url = biliUrl.format(av = self.av)
        print url
        try:
            request = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(request)
            text = ''
            if response.info().get('Content-Encoding') == 'gzip': 
                text = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
            if text.find('cid') == -1:
                print '未找到对应的视频！请检查 av 号！'
                return -1
            pos = text.index('cid')                
            posaid = text.index('&aid')
            self.cid = text[pos + 4 : posaid]
            # print self.cid
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def getFlv(self):
        errCode = self.getCid()
        if errCode == -1:
            return -1
        url = ifUrl.format(cid = self.cid, secretkey = self.secretkey, sign = self.getSign())
        print url
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            text = response.read()
            rst = pattern.findall(text)
            return rst[0]
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def play_video(self):
        url = self.getFlv()
        print url
        if url != -1:
            cmd = 'mpv \'' + url + '\''
            os.system(cmd)

        


if __name__ == '__main__':
    if len(sys.argv) == 2:
        x = bilivideo(sys.argv[1])
        x.play_video()
    else:
        print '参数有误！请输入av号！'

    
