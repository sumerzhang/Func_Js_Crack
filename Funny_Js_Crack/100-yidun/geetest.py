# -*- coding: utf-8 -*-
# @Time    : 2019/9/29 18:37
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm


import random
import requests
import json
import time
import traceback
from urllib.parse import urlencode
from yidun.get_trace import _generate_trace
from yidun.chaojiying import image_to_text
from yidun.img_locate import _get_distance, make_word, _pic_download, merge_word
from yidun.encrypt import _reload_js, _encrypt_slider, _encrypt_click
from yidun.encrypt import _encrypt_sense, _get_cb, _get_fp, _encrypt_validate


class YidunCracker:

    def __init__(self, sid, width):
        # 调用网站的 id
        self.sid = sid
        self.token = ''
        # 验证码图片在浏览器上的宽
        self.width = width
        self.slider_js, self.fp_js = _reload_js()
        self.fp = _get_fp(self.fp_js)
        self.session = requests.session()
        self.session.headers = {
            'Referer': 'https://dun.163.com/trial/sense',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
        }

    def _get_conf(self):
        """
        获取验证码初始 token, acToken
        :return:
        """
        url = 'https://c.dun.163yun.com/api/v2/getconf'
        params = {
            'id': self.sid,
            'ipv6': False,
            'referer': 'https://dun.163.com/trial/sense',
            'callback': '__JSONP_sblyxdg_0'
        }
        resp = self.session.get(url, params=params)
        result = json.loads(resp.text.replace('__JSONP_sblyxdg_0(', '').replace(');', ''))
        try:
            self.token = result['data']['ac']['bid']
            self.ac_token = result['data']['ac']['token']
        except:
            traceback.print_exc()

    def _init_captcha(self):
        """
        初始化验证码
        :return:
        """
        url = 'https://c.dun.163yun.com/api/v2/get'
        params = {
            'id': self.sid,
            'fp': self.fp,
            'https': 'true',
            # 控制验证码类型
            # 2: 滑块, 3: 点选, 5: 无感
            'type': 'undefined',
            'version': '2.13.1',
            'dpr': '1',
            'dev': '1',
            'group': '',
            'scene': '',
            'cb': _get_cb(self.slider_js),
            'ipv6': 'false',
            'runEnv': 10,
            'width': '0',
            'token': self.token,
            'referer': 'https://dun.163.com/trial/sense',
            'callback': '__JSONP_55xb89m_0'
        }
        resp = self.session.get(url, params=params)
        result = json.loads(resp.text.replace('__JSONP_55xb89m_0(', '').replace(');', ''))
        if not result['error']:
            return result
        return None

    def _captcha_verify(self, type, token, data):
        """
        验证
        :param type:
        :param token:
        :param data:
        :return:
        """
        params = {
            'id': self.sid,
            'token': token,
            'acToken': self.ac_token,
            'data': data,
            'width': self.width,
            'type': type,
            'version': '2.13.1',
            'cb': _get_cb(self.slider_js),
            'extraData': '',
            'runEnv': 10,
            'referer': 'https://dun.163.com/trial/sense',
            'callback': '__JSONP_bc4jy3y_1'
        }
        cookies = {
            'gdxidpyhxdE': self.fp
        }
        check_url = 'https://c.dun.163yun.com/api/v2/check?' + urlencode(params)
        resp = self.session.get(check_url, cookies=cookies)
        result = json.loads(resp.text.replace('__JSONP_bc4jy3y_1(', '').replace(');', ''))
        print('校验结果: ', result)
        if result['data']['result']:
            return {'validate': result['data']['validate']}
        return result['data']['token']

    def crack(self, is_first=True):
        """
        验证流程
        :return:
        """
        if is_first:
            self._get_conf()
        init_data = self._init_captcha()
        if not init_data:
            return {
                'success': 0,
                'message': '验证码初始化失败! ',
                'data': None
            }
        print('初始化数据: ', init_data)
        token = init_data['data']['token']
        if init_data['data']['type'] == 5:
            print('触发无感验证! ')
            position = ','.join(
                map(str, [random.randint(120, 180), random.randint(10, 30), random.randint(400, 600)]))
            start_time = int(time.time() * 1000)
            time.sleep(random.uniform(0.01, 0.05))
            trace = _generate_trace(random.randint(50, 300), start_time)
            data = _encrypt_sense(self.slider_js, token, trace, position)
        elif init_data['data']['type'] == 2:
            print('触发滑块验证! ')
            bg = init_data['data']['bg']
            front = init_data['data']['front']
            distance = int(_get_distance(front[1], bg[1]) * (self.width / 320))
            start_time = int(time.time() * 1000)
            time.sleep(random.uniform(0.01, 0.05))
            trace = _generate_trace(distance, start_time)
            data = _encrypt_slider(self.slider_js, token, trace, self.width)
        elif init_data['data']['type'] == 3:
            print('触发点选验证! ')
            bg = init_data['data']['bg']
            front = init_data['data']['front']
            captcha = _pic_download(bg[0], 'click_bg')
            words = make_word(front)
            new_captcha = merge_word(captcha, words, self.width)
            with open(new_captcha, 'rb') as f:
                img_data = f.read()
            ok, position = image_to_text(img_data, img_kind=9004)
            if not ok:
                return {
                    'success': 0,
                    'message': '验证码识别失败! ',
                    'data': None
                }
            position = [[int(i.split(',')[0]), int(i.split(',')[1])] for i in position.split('|')]
            start_time = int(time.time() * 1000)
            time.sleep(random.uniform(0.01, 0.05))
            trace = _generate_trace(random.randint(50, 300), start_time)
            data = _encrypt_click(self.slider_js, token, trace, position)
        else:
            raise Exception('未知类型验证码! ')
        # 最终验证
        result = self._captcha_verify(init_data['data']['type'], token, data)
        return result

    def run(self):
        flag = True
        while True:
            result = self.crack(flag)
            if isinstance(result, dict):
                return {
                    'success': 1,
                    'message': '校验通过! ',
                    'data': {
                        'validate': _encrypt_validate(self.slider_js, result['validate'], self.fp)
                    }
                }
            self.token = result
            flag = False


if __name__ == '__main__':
    # 测试:
    # 无感验证: 74b1d03fcaf944b4aa3a862b2a1893e1
    # 点选验证: 347e9080f7a84e3e8cb79311f9e4cd3f
    # 滑块验证: 5a0e2d04ffa44caba3f740e6a8b0fa84
    x = YidunCracker('347e9080f7a84e3e8cb79311f9e4cd3f', 306).run()
    print(x)
