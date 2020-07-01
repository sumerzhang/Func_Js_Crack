# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 8:41
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : lsm_crypt.py
# @Software: PyCharm

import base64
import hashlib
from Crypto.Cipher import AES


def aes_encrypt(key, iv, text):
    """
    AES 加密, CBC 模式, ZeroPadding补全
    :param key: 密钥
    :param iv: 偏移量
    :param text: 明文
    :return: 密文
    """
    length = 16
    count = len(text)
    if count < length:
        add = (length - count)
        text = text + ('\0' * add)
    elif count > length:
        add = (length - (count % length))
        text = text + ('\0' * add)

    encrypter = AES.new(key.encode(), AES.MODE_CBC, iv.encode())

    cipher_text = encrypter.encrypt(text.encode())
    return base64.b64encode(cipher_text).decode()


def md5_encrypt(text):
    """
    md5 加密
    :param text: 明文
    :return: 密文
    """
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


if __name__ == '__main__':
    x = aes_encrypt("6aafc455d869a1eedfe55739a1a724c5", "2801003954373300", "108,225")
    print(x)
