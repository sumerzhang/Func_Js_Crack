# -*- coding: utf-8 -*-
# @Time    : 2019/10/9 19:35
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : wm_crypt.py
# @Software: PyCharm

import random
import base64
from Crypto.Cipher import AES


class AESCipher:

    def __init__(self, key, iv):
        self.key = key.encode('utf-8')
        self.iv = iv.encode('utf-8')

    @staticmethod
    def pad(text):
        """
        填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充
        :param text:
        :return:
        """
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    @staticmethod
    def unpad(text):
        pad = ord(text[-1])
        return text[:-pad]

    def encrypt(self, text):
        """
        加密
        :param text: 明文
        :return:
        """
        raw = self.pad(text)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw.encode('utf-8'))).decode('utf-8')

    def decrypt(self, text):
        """
        解密
        :param text: 密文
        :return:
        """
        enc = base64.b64decode(text)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self.unpad(cipher.decrypt(enc).decode("utf-8"))


def generate_aes_key(cap_key):
    """
    根据验证码 ID 生成 AES 密钥
    :return:
    """
    aes_key = cap_key[1: 3] + cap_key[10: 13] + cap_key[20: 22] + cap_key[26: 31] + cap_key[21:25]
    return aes_key


def process_trace(trace):
    """
    处理轨迹
    :param trace:
    :return:
    """
    if len(trace) <= 100:
        return trace
    new_trace = []
    i = 0
    for r in range(len(trace)):
        n = (100 - i) / (len(trace) - r)
        if n >= random.random():
            i = new_trace.append(trace[r])
    return new_trace


def encrypt(cap_key, text):
    aes_key = generate_aes_key(cap_key)
    return AESCipher(aes_key, aes_key).encrypt(text)


if __name__ == '__main__':
    encrypter = AESCipher("439346f77a5bf74d", "439346f77a5bf74d")
    enc_str = encrypter.encrypt('{"validate":"246,243,184,47,124,262,250,186","time":9196}')
    print('加密: ' + enc_str)
    dec_str = encrypter.decrypt(enc_str)
    print('解密: ' + dec_str)
    x = generate_aes_key("9546c1ec19a841c49e83d9e10411fe1f")
    print('AES 密钥: ', x)
