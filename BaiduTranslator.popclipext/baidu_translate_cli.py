#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import os
import json
import urllib
import urllib2
import subprocess

url = 'http://fanyi.baidu.com/v2transapi?' + urllib.urlencode(dict(query=os.environ['POPCLIP_TEXT']))
req = urllib2.Request(url)
req.add_header('Referer', 'http://fanyi.baidu.com/')
req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6,de;q=0.4,zh-TW;q=0.2,ja;q=0.2')
req.add_header('Cache-Control', 'max-age=0')
req.add_header('Connection', 'keep-alive')
req.add_header('Host', 'fanyi.baidu.com')
req.add_header('Upgrade-Insecure-Requests', '1')
req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')

try:
    response = urllib2.urlopen(req)
    content = response.read()
    json_dict = json.loads(content)
    result = json_dict['trans_result']['data'][0]['dst'].encode('utf8')
    if os.environ.get('POPCLIP_OPTION_TOCLIPBOARD') == '1':
        lang = os.environ.get('LANG', 'zh_CN.UTF-8')
        process = subprocess.Popen('pbcopy', env={'LANG': lang}, stdin=subprocess.PIPE)
        process.stdin.write(result)
        process.stdin.close()
        retcode = process.wait()
    print(result)
except Exception, e:
    print str(e)
