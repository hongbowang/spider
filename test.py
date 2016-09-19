import re
import urllib
from bs4 import BeautifulSoup
import zlib
import chardet
import requests
import os
from ericbloom import BloomFilter
from PIL import Image

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
    'Connection': 'keep-alive',
    # 'Content-Length': '201',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'cnodejs.org',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
    'cookie': 'CNZZDATA1254020586=1530231062-1473493748-https%253A%252F%252Fexmail.qq.com%252F%7C1473641213; _ga=GA1.2.1991521211.1473497850; connect.sid=s%3ACXPhxRcjguBzYi9ZtOtGwLRlKhHlKaxn.Ue6DufXu4vfjR%2FdtS2jCd9zvr1QO7JpoRg5y4bdTGB8; _gat=1'
}

init_url = 'https://cnodejs.org/topic/57dde6fc3f3cb94e6b32683a'
req = urllib.request.Request(url = init_url,headers = headers)
com_page = urllib.request.urlopen(req).read()
decompressed_data = zlib.decompress(com_page,16 + zlib.MAX_WBITS)
page = decompressed_data.decode('utf-8')
topic_url = re.findall('<a href="/user/(.*?)"',page,re.S)
for topic in topic_url:
    print(topic)


'''
person_url = 'https://cnodejs.org/user/nsmaomao'
name = 'nsmaomao'
req = urllib.request.Request(url=person_url, headers=headers)
com_page = urllib.request.urlopen(req).read()
decompressed_data = zlib.decompress(com_page,16 + zlib.MAX_WBITS)
per_page = decompressed_data.decode('utf-8')

github1 = re.findall('<i class="fa fa-lg fa-fw fa-github"></i>(.*?)</li>', per_page, re.S)
print(github1)
github = re.findall('href="(.*?)" target=', str(github1), re.S)
print(''.join(github))


place1 = re.findall('<i class="fa fa-lg fa-fw fa-map-marker"></i>(.*?)</li>', per_page, re.S)
print(place1)
n = ''.join(place1)
print(n)
place = re.findall('<span class=\'dark\'>(.*?)</span>',n,re.S)
print( ''.join(place))

profile = re.findall('<div class=\'user_profile\'>(.*?)积分', per_page, re.S)
test = re.search('(\d+)',str(profile),re.S)
print( test.group(0))
print(type(test.group(0)))

signature1 = re.findall('<span<a class='topic_title'  class="signature">\n        “\n        \n            (.*?)\n        \n        ”\n    </span>',per_page.strip(),re.S)
signature = ''.join(signature1)
print (signature)

img_url1 = re.findall('<a class=\'user_avatar\'(.*?)</a>', per_page, re.S)
img_url = re.findall(' <img src="(.*?)" title=',str(img_url1), re.S)

img_url1 = re.findall('<a class=\'user_avatar\'(.*?)</a>', per_page, re.S)
img_url2 = re.findall(' <img src="(.*?)" title=', str(img_url1),  re.S)
img_url = ''.join(img_url2)
print(img_url)
pic = requests.get( img_url)
fp = open(name , 'wb+')
fp.write(pic.content)


fp2 = open(name  , 'rb')
im = Image.open(fp)
im.save('test3.jpg')
print('转换成功！！！！。。')
fp.close()

filename =name + u'.jpg'
print('img downloads is down......')


print('come in ')
f = BloomFilter(0.001, 300)
#[f.add(x) for x in range(10)]
for i in range(20,30):
    print(i)
    for x in range(0,i):
        print('x is ...' + str(x))
        f.insert_element(x)

for i in range(1,2):
    print(i)
print(f.is_element_exist(8))
print(f.is_element_exist(25))
'''