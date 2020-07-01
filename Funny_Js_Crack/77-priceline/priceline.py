import requests
import execjs
import re
import json


def get_js(text):
    z = ''
    b = re.search('b="([^"]+)"', text, re.S).group(1)
    for i in range(0, len(b), 2):
        sub = b[i:i + 2]
        num = int(sub, 16)
        z += chr(num)
    return z


# js 文件
with open(r'E:\JavaScriptCode\Node\test.js', 'r', encoding='utf-8') as f:
    get_cookie = f.read()

session = requests.session()
headers = {
    # 'Host': 'www.priceline.com.au',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Connection': 'keep-alive',
    # 'Upgrade-Insecure-Requests': '1',
    # 'TE': 'Trailers',
    }


# 请求获取更新的参数，生成cookie需要
r = requests.get('https://www.priceline.com.au/?tdsourcetag=s_pcqq_aiomsg', headers=headers)
# 获取响应的cookie
ses_cookie = re.search('(incap_ses_\d+_\d+=.*?) ', str(r.cookies)).group(1) + '; '
visid_cookie = re.search('(visid_incap_\d+=.*?) ', str(r.cookies)).group(1)
headers['Cookie'] = visid_cookie + ses_cookie

response = requests.get('https://www.priceline.com.au/_Incapsula_Resource?SWJIYLWA=5074a744e2e3d891814e9a2dace20bd4,719d34d31c8e3a6e6fffd425f7e032f3', headers=headers)
js = get_js(response.text)
with open(r'test.js', 'w', encoding='utf-8') as f:
    f.write(js)

nums = re.findall(';}\(_0x[0-9a-z]+,(0x[0-9a-z]+)\)\);', js)  # 排序数组需要
img_change_num = int(nums[0], 16)
num = int(nums[1], 16)

change = re.findall("\)\]\('',.*?\('(.*?)', '(.*?)'\)\);con", js)  # 加密需要，一个是在数组中的位置，另一个是加密的数据
# 这两个是获取 img url 需要的
img_num = int(change[0][0], 16)
img_data = change[0][1].encode('latin-1').decode('unicode_escape')  # 需要解码，不然会出现乱码
# 这两个是cookie需要的数据
change_num = int(change[1][0], 16)
change_data = change[1][1].encode('latin-1').decode('unicode_escape')

arrs = re.findall("var [_0-9a-z]+=(\['.+?'\]);\(function\(", js)  # 两个数组，加密数据需要
# 需要请求一张图片，不带 utmvc cookie
img_arr = json.loads(arrs[0].encode('latin-1').decode('unicode_escape').replace("'", '"'))
# 转json时需要将单引号替换成双引号，要不然会出错json.decoder.JSONDecodeError: Expecting value: line 1 column 2 (char 1)
arr = json.loads(arrs[1].encode('latin-1').decode('unicode_escape').replace("'", '"'))


# 执行js获取cookie
ctx = execjs.compile(get_cookie)


data = ctx.call('get_cookie', ses_cookie, arr, num, change_num, change_data, img_arr, img_change_num, img_num, img_data)

requests.get(data[0], headers=headers)
headers['Cookie'] = headers['Cookie'] + '; ' + data[1]
requests.get('https://www.priceline.com.au' + data[2], headers=headers)
response = requests.get('https://www.priceline.com.au/?tdsourcetag=s_pcqq_aiomsg', headers=headers)
print(response.text)
print(data[0])
print(data[1])
