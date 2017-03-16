#-*- coding=utf-8 -*-
import urllib
import  urllib2
import glob
import  sqlite3
import  os
import  cookielib
import  json
import time
import  lxml.html

##通过lxml 的css选择器遍历表单中的所有的input标签，然后以字典的形式返回其中的name和value属性。
def parse_form(html):
    tree=lxml.html.fromstring(html)
    data={}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')]=e.get('value')

    return data

LOGIN_EMAIL='example@webscraping.com'
LOGIN_PASSWORD='example'
LOGIN_URL='http://example.webscraping.com/user/login'



##如果仅仅是上面的部分，这个登陆的版本依然不能工作，因为缺失了一个重要的组成部分-cookie.当普通用户加载登陆表单的时候，_formkey的值
#将会保存在cookie中，然后该值与提交的表单数据中的_formkey进行对比。使用urllibb2.HTTPCookieProcessor 增加了cookie的支持
cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#获取所有的input
html=opener.open(LOGIN_URL).read()
data=parse_form(html)

'''
{'_formkey': '956874b4-6420-4c18-93c3-bb609a20a402',  #这是隐藏的，服务端使用这个唯一的ID来避免表单的多次提交。每次加载网页时都会产生不同的ID,然后
                                #服务端就可以根据这个给定的ID,来判断这个表单是否提交过。
 '_formname': 'login',
 '_next': '/',
 'email': '',
 'password': '',
 'remember_me': 'on'}

'''
#填充其中的email和password
data['email']=LOGIN_EMAIL
data['password']=LOGIN_PASSWORD
encoded_data=urllib.urlencode(data)

request=urllib2.Request(LOGIN_URL,encoded_data)
response=opener.open(request)

print response.geturl()
