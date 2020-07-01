# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 15:59
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import os
import re
import time
import json
import requests
import base64
import hashlib
from PIL import Image
from Crypto.Cipher import AES
from dajie.chaojiying import image_to_text


headers = {
    'Referer': 'https://www.dajie.com/account/newreg?from=header_register',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def aes_encrypt(key, text):
    """
    AES ECB Pkcs7Padding
    :param key: 密钥
    :param text: 明文
    :return:
    """
    bs = AES.block_size
    # Pkcs7 填充
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    encrypter = AES.new(key.encode(), AES.MODE_ECB)
    cipher = encrypter.encrypt(pad(text).encode())
    return base64.b64encode(cipher).decode()


def aes_decrypt(key, text):
    """
    AES 解密
    :param key: 密钥
    :param text: 密文
    :return:
    """
    unpad = lambda s: s[0:-ord(s[-1])]
    decrypter = AES.new(key.encode(), AES.MODE_ECB)
    cipher = decrypter.decrypt(base64.b64decode(text.encode()))
    return unpad(cipher.decode())


def md5_encrypt(text):
    """
    md5 加密
    :param text: 明文
    :return:
    """
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def generate_aes_key(text):
    """
    生成 AES 密钥
    :return:
    """
    return md5_encrypt(text)[0:16]


def generate_ev(aes_key):
    """
    生成验证码初始化环境参数 ev
    :param aes_key: AES 密钥
    :return:
    """
    params = ';sep;'.join([headers['User-Agent'], headers['Referer'], str(int(time.time() * 1000)), ''])
    return aes_encrypt(aes_key, params)


def generate_env(aes_key, position):
    """
    生成验证参数 env
    :param aes_key: AES 密钥
    :param position: 位置
    :return:
    """
    x = "regSource=1&identity=1&phoneNumber=&password=&name=&capToken=&agreeclause=1&newreg=newregnormal&appKey=normal&customVerifyMailFlag=1&redir=https%3A%2F%2Fwww.dajie.com%2Faccount%2Fregguide%3Fredir%3Dhttps%253A%252F%252Fwww.dajie.com%252F&_CSRFToken="
    params = ';sep;'.join([position, headers['User-Agent'], headers['Referer'], x])
    return aes_encrypt(aes_key, params)


def init_click(aes_key):
    """
    初始化点选验证码
    :return:
    """
    url = 'https://captcha.dajie.com/api/qazwsxedcrfvtgbyhnujmikloqazwled.json'

    ev = generate_ev(aes_key)
    params = {
        'callback': '',
        'ajax': 1,
        'ev': ev,
        '_': int(time.time() * 1000)
    }
    resp = requests.get(url, params=params, headers=headers)
    result = json.loads(resp.text.replace('(', '').replace(');', ''))
    return result


def _pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = save_path + '\\' + '{}.jpg'.format(type)
    cookies = {
        'csid': re.search('csid=(.*?)&', url).group(1)
    }
    img_data = requests.get(url, headers=headers, cookies=cookies).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def merge_img(init_data, url):
    """
    还原验证码
    :param init_data:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = _pic_download(url, 'captcha')
    captcha = Image.open(img_path)
    new_captcha = Image.new('RGB', captcha.size)

    aes_key = generate_aes_key(init_data['xyParamKeyt'])
    decrypt_data = aes_decrypt(aes_key, init_data['imgSplitEncryptData'])
    d = decrypt_data.split(';s;')
    sequence = [int(x) for x in d[2].split(',')]
    x = int(d[0])
    y = int(d[1])
    col = int(d[3])
    for i in range(len(sequence)):
        if i >= col:
            num = 1
        else:
            num = 0
        imgcrop = captcha.crop((sequence[i] % col * x, num * y, sequence[i] % col * x + x, num * y + y))
        new_captcha.paste(imgcrop, (i % col * x, num * y))
    new_captcha.show()
    new_cappath = save_path + '\\' + 'new_captcha.jpg'
    new_captcha.save(new_cappath)
    with open(new_cappath, 'rb') as f:
        img_data = f.read()
    return img_data


def click_verify(position, init_data, csid, timestamp):
    """
    点选验证
    :return:
    """
    url = 'https://captcha.dajie.com/api/qazwsxedcrfvtgbyhnujmikloqazwled.cv'

    ven = generate_env(init_data['xyParamKeyt'], position)
    params = {
        'callback': '',
        'ajax': 1,
        'csid': csid,
        'xyParamKeyt': init_data['xyParamKeyt'],
        'p': position,
        'time': timestamp,
        'ven': ven,
        '_': int(time.time() * 1000)
    }
    resp = requests.get(url, headers=headers, params=params, cookies={'csid': csid})
    result = json.loads(resp.text.replace('(', '').replace(');', ''))
    print(result)
    if result['state'] == 'ok':
        return result['msg']
    return None


def click():
    aes_key = generate_aes_key("qazwsxedcrfvtgbyhnujmikloqazwled")
    init_data = init_click(aes_key)
    url = 'https:' + init_data['base64img']
    csid = re.search('csid=(.*?)&', url).group(1)
    img_data = merge_img(init_data, url)
    ok, result = image_to_text(img_data, img_kind=9004)
    timestamp = int(time.time() * 1000)
    if ok:
        position = result.replace('|', ';') + ';'
        result = click_verify(position, init_data, csid, timestamp)
        if result:
            return {
                'success': 1,
                'message': '校验通过! ',
                'data': {
                    'msg': result
                }
            }
        return {
            'success': 0,
            'message': '校验失败! ',
            'data': None
        }
    else:
        return {
            'success': 0,
            'message': '验证码识别失败! ',
            'data': None
        }


if __name__ == '__main__':
    x = click()
    print(x)
