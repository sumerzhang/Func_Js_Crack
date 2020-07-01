# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 16:12
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import requests
import traceback
from PIL import Image
from geetest3.chaojiying import image_to_text
from geetest3.encrypt import *
from geetest3.img_locate import ImgProcess
from geetest3.get_trace import *


class GeetestV3:

    def __init__(self, gt, challenge):
        self.gt = gt
        self.challenge = challenge


if __name__ == "__main__":
    pass
