# coding: utf-8
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import selenium
import urllib.request
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient


def Get_cookie(loginurl):
    driver = selenium.webdriver.Firefox()
    loginurl = 'http://120.76.195.80:8085/welcome'
    driver.get(loginurl)
    try:
        driver.find_element_by_name("username").send_keys("admin")
        print("user is success...")
    except:
        print("user is error...")
    try:
        driver.find_element_by_name("password").send_keys("Jianxun1302,")
        print("password is success...")
    except:
        print("password is error...")
    time.sleep(1)
    try:
        driver.find_element_by_name("submit").click()
        print("click is success...")
    except:
        print("click is error...")
    time.sleep(2)

    curpage_url = driver.current_url
    print(curpage_url)
    if curpage_url == loginurl:
        print("need verify code...")
    else:
        print ("login success...")
    time.sleep(2)
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    print(cookie)
    cookiestr = ';'.join(item for item in cookie)
    print (cookiestr)
    return cookiestr
    driver.close()
    driver.quit()
def Get_content(cookiestr):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
        'Connection': 'keep-alive',
        # 'Content-Length': '201',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ehirelogin.51job.com',
        'Origin': 'http://ehire.51job.com',
        'Referer': 'http://ehire.51job.com/MainLogin.aspx',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'cookie': cookiestr
    }
    homeurl = 'http://120.76.195.80:8085/resume/listajax?rand=Tue%20Sep%2006%202016%2011:26:47%20GMT+0800%20(CST)'
    req = urllib.request.Request(url=homeurl, headers=headers)
    page = urllib.request.urlopen(req).read().decode('utf-8')
    return page

def Get_number(page):
    number = re.findall('<td align="center">(.*?)</td>', page, re.S)
    for n in number:
        print(str(n))
    return number

def Get_txt(cookiestr,number):

    txt_url = 'http://120.76.195.80:8085/resume/detail/'+ str(number)+ '?keywordencode='
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en,zh-CN;q=0.8,zh;q=0.6',
        'Connection': 'keep-alive',
        # 'Content-Length': '201',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
        'cookie': cookiestr
    }

    req = urllib.request.Request(url=txt_url,headers=headers)
    page = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(page)
    #print(soup.body.a.string) 待调整
    Rlist = []
    for string in soup.body.stripped_strings:
        #print(string)                       #此句用来输出完整的简历库
        Rlist.append(string)
    strings = soup.body.stripped_strings
    Rstring = '。。'.join(Rlist)
    return Rstring


def to_str(list):
    str = ''.join(list)
    return str

def In_Mongo1(strings):

    #print(strings)

    conn = MongoClient('localhost', 27017)
    name_list1 = re.findall('(.*?)。。编号：',strings,re.S)
    name_list = re.findall('(.*?)。。',''.join(name_list1),re.S)
    #phone_list = re.findall('联系方式：(.*?)  邮箱',strings,re.S)   #list4
    try:
        phone_group = re.search('(\d{11})',strings,re.S)       #使用match来匹配第一次出现的11位数字作为手机号 type : str
        #print(phone_group)
        phone_str = phone_group.group(0)
    except:
        print('phone number is wrong...')
        phone_str = ''

    email_list = re.findall('邮箱：(.*?)。。',strings,re.S)               #list4
    gender_list = re.findall('性别：(.*?)  ',strings,re.S)     #list2
    marital_list = re.findall('婚姻状况：(.*?)。。',strings,re.S)         #list22
    id_list = re.findall('编号：(.*?)  ',strings,re.S)               #list2

    name_str = to_str(name_list).strip()
    #phone_str = to_str(phone_list).strip()
    email_str1 = to_str(email_list).strip()   #粗邮箱
    try:
        email_str2 = re.findall('(.*?)\.com',email_str1,re.S)     #细邮箱 list
        email_str = to_str(email_str2)                     #细邮箱 字符串
    except:
        email_str = ''
        print('email error...')


    if len(email_str) > 1:
        email_str = email_str + ".com"


    gender_str = to_str(gender_list)
    marital_str = to_str(marital_list)
    id = to_str(id_list)


    if gender_str == '男':
        gender_id = 1
    elif gender_str == '未知':
        gender_id = 0
    elif gender_str == '女' :
        gender_id = 2
    else:
        gender_id = 3       # 3 代表特殊情况

    if marital_str.strip() == '已婚':
        marital_id = 1
    elif marital_str.strip() == '未婚':
        marital_id = 2
    elif marital_str.strip() == '保密':
        marital_id = 0
    else:
        marital_id = 3       #3 代表特殊情况



    print(name_str,phone_str,email_str,gender_id,marital_id,id)


    RESUME_EXAMPLE = {"jx_resume_id":id,
                      "resume_source":{"source":0,"source_resume_id":'',"source_resume_name":'',"last_update":0},
                    "profile":{"name":name_str,"mobile_phone":phone_str,"tele_phone":'',"emali":email_str,"weixin":"","gender":gender_id,"age":'',"marital_status":marital_id
                                },
                    "work_year":{
                         "form":3,
                        "to":5
                                 }
                    }
    db = conn.hunter
    db.hunter.insert(RESUME_EXAMPLE)
    cursor = db.hunter.find()
    #输出数据库中的数据 以便调式
    '''
    for i in cursor:
        print(i)
'''




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

    loginurl = 'http://120.76.195.80:8085/welcome'

    cookiestr = Get_cookie(loginurl)

    Page = Get_content(cookiestr)
    print(tag1)
    number = Get_number(Page)
    print(tag2)


    for n in range(int(number[0])-1000,int(number[0])):
        strings =  Get_txt(cookiestr,n)
        In_Mongo1(strings)




    print('program is down...')




#['JSESSIONID=D09E6448B8C2B239027495DD14F83A44', 'HUNTER_SYSTEM_COOKIES_USER="1,9784ed6e7ca1c8d6d802b0b5ab535185"', 'DWRSESSIONID=w4X*MPXTtO1fm46nUb7V1ljP*rl']