#-*- coding=utf-8 -*-

#在分析验证码图像之前，需要从表单中获取图像，这次的网页图像是嵌入在网页中的，而不是从其他的网页中加载过来的
#需要使用Pillow处理该图像
#Pillow提供了一个便捷的Image类，其中包含了很多用于处理验证码图像的高级方法
from io import BytesIO
import lxml.html
from PIL import Image
import cookielib
import urllib
import urllib2
import string
import pytesseract

##通过lxml 的css选择器遍历表单中的所有的input标签，然后以字典的形式返回其中的name和value属性。
def parse_form(html):
    tree=lxml.html.fromstring(html)
    data={}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')]=e.get('value')

    return data


#下面的函数使用注册页的HTML作为输入参数，返回包含验证码图像的Image对象
def extract_image(html):
    tree=lxml.html.fromstring(html)
    img_data=tree.cssselect('div#recaptcha img')[0].get('src')
    img_data=img_data.partition(',')[-1]
    binary_img_data=img_data.decode('base64')
    file_like=BytesIO(binary_img_data)
    img=Image.open(file_like)
    #img.save('test.png')
    return img

#光学字符识别 OCR
'''
用于从图像中抽取文本，该引擎由最初的惠普公司开发，目前由Google主导
Python封装的版本 pytesseract
下面是直接把原始的验证码图像传给pytesseract ，解析结果一般都会很糟糕
img=get_captcha(html)
pytessetact.img_to_string(img)
是因为Tesseract 设计初衷抽取更加一般的典型文本，比如背景统一的书页，所以需要先修改验证码图像，去除背景噪音，只保留
文本部分。
'''


'''
如何去除背景噪音？
验证码文本一般是黑色的，背景则会更加明亮，我们可以通过检查像素是否为黑色将文本分离出来
该处理过程又称为阈值化，通过pillow很容易实现

img.save('captcha_original.png')
gray=img.convert('L')
gray.save('captcha_gray.png')
bw=gray.point(lambda x:0 if x<1 else 255,'1')
bw.save('captcha_thresholded.png')
此时只有阈值为1的像素才会保留，也就是说只有全黑的像素才会保留下来。
'''
def captcha_fn(img):
    gray = img.convert('L')
    #gray.save('captcha_gray.png')
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    word=pytesseract.image_to_string(bw)
    ascii_word=''.join(c for c in word if c in string.letters).lower()
    return ascii_word

register_url='http://example.webscraping.com/user/register'
def register(first_name,last_name,email,password):
    cj=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html=opener.open(register_url).read()
    form=parse_form(html)
    form['first_name']=first_name
    form['last_name']=last_name
    form['email']=email
    form['password']=form['password_two']=password
    img = extract_image(html)
    captcha = captcha_fn(img)
    form['recaptcha_response_field'] = captcha
    encoded_data = urllib.urlencode(form)
    request = urllib2.Request(register_url, encoded_data)
    response = opener.open(request)
    success = '/user/register' not in response.geturl()
    return success

#测试
register('wuyy','wuyy','we@test.com','123456')
