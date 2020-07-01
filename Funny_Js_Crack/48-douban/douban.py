import requests
import execjs  # 这个库是PyExecJS
import re


response = requests.get('https://book.douban.com/subject_search?search_text=%E7%BD%91%E7%BB%9C%E6%98%AF%E6%80%8E%E6%A0%B7%E8%BF%9E%E6%8E%A5%E7%9A%84&cat=1001')
r = re.search('window.__DATA__ = "([^"]+)"', response.text).group(1)  # 加密的数据

# 导入js
with open('main.js', 'r', encoding='gbk') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
data = ctx.call('decrypt', r)
for item in data['payload']['items']:
    print(item)
