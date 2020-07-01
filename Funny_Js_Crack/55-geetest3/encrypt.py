# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 16:10
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : encrypt.py
# @Software: PyCharm

import math
import re
import binascii, json, os
import time
import random
import hashlib
import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class Encrypter:

    def __init__(self):
        self.modulus = "00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81"
        self.pub_key = '10001'


