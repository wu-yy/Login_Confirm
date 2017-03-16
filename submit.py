#-*- coding=utf-8 -*-
#登陆成功后与表单交互

import  login
import urllib2
import urllib
#这里是登陆过后修改网页的特定form的值

COUNTRY_URL="http://example.webscraping.com/edit/Aland-Islands-2"

opener=login.login_cookies()
country_html=opener.open(COUNTRY_URL).read()

data=login.parse_form(country_html)

data['population']=int(data['population'])+1
encoded_data=urllib.urlencode(data)
request=urllib2.Request(COUNTRY_URL,encoded_data)
response=opener.open(request)
print response.geturl()
