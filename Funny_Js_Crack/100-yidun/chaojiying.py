# -*- coding: utf-8 -*-
# @Time    : 2019/10/9 21:40
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : chaojiying.py
# @Software: PyCharm


import requests
from hashlib import md5


class ChaojiyingClient(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


def image_to_text(img,
                  username='*******',
                  password='********',
                  soft_id='497bc231401f085df56dae7c2e3a9b86',
                  img_kind=1902):
    """
    将图片转化为文字
    :param img: 验证码二进制数据
    :param username:用户名
    :param password: 密码
    :param soft_id: 软件id
    :param img_kind: 验证码类型
    :return:
    """
    chaojiying = ChaojiyingClient(username, password, soft_id)
    result = chaojiying.PostPic(img, img_kind)
    if result['err_no'] == 0:
        return True, result['pic_str']
    else:
        chaojiying.ReportError(result['pic_id'])
        return False, result['err_str']


if __name__ == '__main__':
    chaojiying = ChaojiyingClient('******', '*******', '96001')	# 用户中心>>软件ID 生成一个替换 96001
    im = open('captcha.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    print(chaojiying.PostPic(im, 1902))	 # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
