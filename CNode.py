# coding: utf-8
import re
import urllib
from bs4 import BeautifulSoup
import zlib
from pymongo import MongoClient
from ericbloom import BloomFilter
import requests

def Get_page(headers,page_url):
    req = urllib.request.Request(url = page_url,headers = headers)
    com_page = urllib.request.urlopen(req).read()
    decompressed_data = zlib.decompress(com_page, 16 + zlib.MAX_WBITS)
    page = decompressed_data.decode('utf-8')
    return page

def Get_topic(init_url):
    init_url = 'https://cnodejs.org/'
    req = urllib.request.Request(url=init_url, headers=headers)
    com_page = urllib.request.urlopen(req).read()
    decompressed_data = zlib.decompress(com_page, 16 + zlib.MAX_WBITS)
    page = decompressed_data.decode('utf-8')
    topic_url = re.findall('<a class=\'topic_title\' href=\'(.*?)\' title=', page, re.S)
    return topic_url
#第二层参与话题人员

def Person_page(headers,name):
    person_url = 'https://cnodejs.org/user/'+name
    req = urllib.request.Request(url = person_url,headers = headers)
    com_page = urllib.request.urlopen(req).read()
    decompressed_data = zlib.decompress(com_page,16 + zlib.MAX_WBITS)
    per_page = decompressed_data.decode('utf-8')
    return per_page

def Get_github(per_page):
    github1 = re.findall('<i class="fa fa-lg fa-fw fa-github"></i>(.*?)</li>',per_page,re.S)
    github = re.findall('href="(.*?)" target=',str(github1),re.S)
    return ''.join(github)

def Get_twitter(per_page):
    weibo1 = re.findall('<i class="fa fa-lg fa-fw fa-weibo"></i>(.*?)</li>',per_page,re.S)
    weibo = re.findall('herf="(.*?) target=',str(weibo1),re.S)
    return ''.join(weibo)

def Get_home(per_page):
    home1 = re.findall('<i class="fa fa-lg fa-fw fa-home"></i>(.*?)</li>',per_page,re.S)
    home = re.findall('herf="(.*?) target=',str(home1),re.S)
    return ''.join(home)

def Get_place(per_page):
    place1 = re.findall('<i class="fa fa-lg fa-fw fa-map-marker"></i>(.*?)</li>',per_page,re.S)
    place = re.findall('<span class=\'dark\'>(.*?)</span>',str(place1),re.S)
    return ''.join(place)

def Get_profile(per_page):
    test = re.findall('<div class=\'user_profile\'>(.*?)积分', per_page, re.S)
    profile = re.search('(\d+)', str(test), re.S)
    return profile.group(0)

def Get_jpg(name,per_page):
    img_url1 = re.findall('<a class=\'user_avatar\'(.*?)</a>', per_page, re.S)
    img_url2 = re.findall(' <img src="(.*?)" title=', str(img_url1), re.S)
    img_url = ''.join(img_url2)
    print('url is ................' + img_url)
    with open('/root/CNode1/untitled1/.idea/picture/' + name, 'wb') as fp:
        try:
            pic = requests.get(img_url,timeout = 3)
            fp.write(pic.content)
            return '/root/CNode1/untitled1/.idea/picture/'+name

        except:
            #print('maybe he is a manager')
            print('修正后的url是............https:' + img_url)
            try:
                pic = requests.get('https:' + img_url,timeout = 3)
                fp.write(pic.content)
            except:
                print('!!!!!!!!!!!!!timeout!!!!!!!!!!!!!')
            return '/root/CNode1/untitled1/.idea/picture/' + name
#BUG排除记录，本机运行没有问题，但是在服务器中会在某些（固定）用户的头像下载模块中出现正常的http://***无法访问的问题，此时会有访问链接超时，从而进入except，url就会变为https://https://****
#requests就会报错这不是一个正常的链接，处理办法是在每次链接前打印该url，打印之后问题就消失了。


def Get_signature(per_page):
    signature1 = re.findall('<span class="signature">\n        “\n        \n            (.*?)\n        \n        ”\n    </span>',per_page.strip(), re.S)
    signature = ''.join(signature1)
    return signature


if __name__ == '__main__':

    usage = '''
      __  __  _____       _     _
     |  \/  |/ ____|     (_)   | |
     | \  / | (___  _ __  _  __| | ___ _ __
     | |\/| |\___ \| '_ \| |/ _` |/ _ \ '__|
     | |  | |____) | |_) | | (_| |  __/ |
     |_|  |_|_____/| .__/|_|\__,_|\___|_|
                   | |
                   |_|
                            Author: Eric
        '''


    tag1 = '''
    ..................................................
    '''
    tag2 = '''
    **************************************************
    '''
    print(usage)

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


    bf = BloomFilter(0.001, 100000)             #建立一个布隆过滤器，第一个参数为容错率，第二个参数为容器空间大小，在上线的时候需要修改

    for i in range(1,500):                      #主网页的循环控制
        page_url = 'https://cnodejs.org/?tab=all&page='+str(i)
        page = Get_page(headers,page_url)
        soup = BeautifulSoup(page)
        content = soup.find_all('a')
        name_tag = re.findall('<a class="user_avatar pull-left" href="/user/(.*?)">',str(content),re.S)

        conn = MongoClient('localhost', 27017)                    #建立monogoDB链接


        for name in name_tag:                 #网页内用户的循环控制
            if bf.is_element_exist(name) is False:
                print(name)

                per_page = Person_page(headers,name)     #获得个人页面的html代码数据

                place = Get_place(per_page)              #获得居住地，没有则为空字符
                print('test 1......................................')
                home = Get_home(per_page)                #获得主页
                print('test 2......................................')
                twitter = Get_twitter(per_page)          #获得微博
                print('test 3......................................')
                github = Get_github(per_page)            #获得github
                print('test 4......................................')
                profile = Get_profile(per_page)          #获得积分
                print('test 5......................................')
                signature = Get_signature(per_page)      #获得签名
                print('test 6......................................')
                img_path = Get_jpg(name,per_page)        #获得图片路径
                print('test 7......................................')
                person_url = 'https://cnodejs.org/user/' + name                          #注意图片下载部分耗时较长

                bf.insert_element(name)                  #将不重复的名字（tag）插入布隆过滤器中

                USER_INFORMATION = {
                    'name': name,
                    'home': home,
                    'twitter': twitter,
                    'github': github,
                    'profile': profile,
                    'signature': signature,
                    'place': place,
                    'head_portrait': img_path,             # 服务器中的照片存储路径
                    'url':person_url,                      # 个人页面 url链接
                    'page':per_page                        # 页面源代码

                }  # 除了积分项都是string

                #向monogo中添加数据的模块
                db = conn.CNode1
                db.CNode1.insert(USER_INFORMATION)
                #cursor = db.CNode.find()                  #输出所有的表格

        print('.......................参与话题人员.......................')

        init_url = 'https://cnodejs.org'
        topic_url_list = Get_topic(init_url)

        for topic in topic_url_list:
            topic_url = init_url + topic
            print(topic_url)
            req = urllib.request.Request(url=topic_url, headers=headers)
            com_page = urllib.request.urlopen(req).read()
            decompressed_data = zlib.decompress(com_page, 16 + zlib.MAX_WBITS)
            page = decompressed_data.decode('utf-8')

            name_list = re.findall('<a href="/user/(.*?)"',page,re.S)  #获得在当前话题页面中的所有name标签

            for name in name_list:
                if bf.is_element_exist(name) is False:
                    print(name + '.....................')
                    try:
                        per_page = Person_page(headers, name)  # 获得个人页面的html代码数据
                    except:
                        print('不存在这个用户。。。。。。。')
                    place = Get_place(per_page)            # 获得居住地，没有则为空字符
                    print('test 1......................................')
                    home = Get_home(per_page)              # 获得主页
                    print('test 2......................................')
                    twitter = Get_twitter(per_page)        # 获得微博
                    print('test 3......................................')
                    github = Get_github(per_page)          # 获得github
                    print('test 4......................................')
                    profile = Get_profile(per_page)        # 获得积分
                    print('test 5......................................')
                    signature = Get_signature(per_page)    # 获得签名
                    print('test 6......................................')
                    img_path = Get_jpg(name, per_page)     # 获得图片路径
                    print('test 7......................................')
                    person_url = 'https://cnodejs.org/user/' + name  # 注意图片下载部分耗时较长

                    bf.insert_element(name)                # 将不重复的名字（tag）插入布隆过滤器中

                    USER_INFORMATION = {
                        'name': name,
                        'home': home,
                        'twitter': twitter,
                        'github': github,
                        'profile': profile,
                        'signature': signature,
                        'place': place,
                        'head_portrait': img_path,  # 服务器中的照片存储路径
                        'url': person_url,          # 个人页面 url链接
                        'page': per_page            # 页面源代码

                    }  # 除了积分项都是string

                    # 向monogo中添加数据的模块
                    db = conn.CNode1
                    db.CNode1.insert(USER_INFORMATION)
                    # cursor = db.CNode.find()                  #输出所有的表格






#/home/ericwang/PycharmProjects/untitled1/.idea/pictuer/      本机 图片存储url
#/root/CNode/untitled1/.idea/picture/                               服务器存储url