# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 21:03
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm


import re
import json
import time
import random
import execjs
import requests
from tengxun.img_locate import get_distance
from tengxun.get_trace import generate_trace

session = requests.session()
session.headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://ssl.captcha.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def process_distance(distance):
    """
    处理距离
    :param distance:
    :return:
    """
    return xxx


def encrypt_data(env_data, trace):
    with open('tx_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('getData', env_data, trace)


def encrypt_ua(ua):
    """
    window.btoa(UA)
    :param ua:
    :return:
    """
    with open('tx_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('encryptUA', ua)


def u_challenge(cap_challenge):
    with open('u_challenge.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('challenge', cap_challenge)


def format_data(sid, trace, start_time, pass_time, referer):
    """
    构造加密 collect_data
    :param sid:
    :param trace:
    :param start_time:
    :param pass_time:
    :param referer
    :return:
    """
    # 环境校验参数一个有42个, 这几个是变化的, 其他的都可以固定, 我这里就不列出来了, 请自己调试
    env_data = [
        [sid], [start_time], [start_time + pass_time], [referer]
    ]
    # 包括验证码刷新次数、验证次数在内的8个参数, 轨迹加密字符串: '"sd": {具体参数}}', 自己调试填充
    trace_data = json.dumps({'slideValue': trace})[1:]
    return encrypt_data(env_data, trace_data)


def get_session(aid, referer):
    """
    首次验证, 无感验证, 判断用户环境风险
    :return:
    """
    url = 'https://ssl.captcha.qq.com/cap_union_prehandle'

    params = {
        'subsid': 1,
        'aid': aid,
        'captype': '',
        'curenv': 'inner',
        'protocol': 'https',
        'clientype': 2,
        'disturblevel': '',
        'apptype': 1,
        'noheader': '',
        'color': '',
        # ua: window.btoa('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36')
        'ua': 'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzc1LjAuMzc3MC44MCBTYWZhcmkvNTM3LjM2',
        'collect': format_data('', [], int(time.time()), random.randint(100, 200), referer),
        'showtype': 'point',
        'fb': 1,
        'theme': '',
        'lang': 2052,
        'grayscale': 1,
        'uid': '',
        'cap_cd': '',
        'height': 54,
        'rnd': 812249,
        'forcestyle': 'undefined',
        'firstvrytype': 1,
        'random': random.random(),
        '_': int(time.time() * 1000)
    }

    result = session.get(url, params=params).json()
    if result['state']:
        return {
            'session_id': result['sess'],
            'sid': result['sid'],
        }
    return None


def get_fpsig():
    """
    传输环境参数, 获取设备指纹, 设备指纹可以固定
    :return:
    """
    url = 'https://ssl.captcha.qq.com/dfpReg'
    params = {
        '0': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
        '1': 'zh-CN',
        '2': '1.8',
        '3': '1.9',
        '4': '24',
        '5': '4',
        '6': '-480',
        '7': '1',
        '8': '1',
        '9': '1',
        '10': 'u',
        '11': 'function',
        '12': 'u',
        '13': 'Win32',
        '14': '0',
        '15': '9dcc2da81f0e59e03185ad3db82acb72',
        '16': '6a6476965e1bf1d8031a3e0c72354a1b',
        '17': 'a1f937b6ee969f22e6122bdb5cb48bde',
        '18': '0',
        '19': '0ec8b778a64692203feec04be22f49d0',
        '20': '728136624768136624',
        '21': '1;',
        '22': '1;1;1;1;1;1;1;0;1;object0UTF-8',
        '23': '0',
        '24': '0;0',
        '25': '8f20d85f1f86b554991f798c7a1a9d2e',
        '26': '48000_2_1_0_2_explicit_speakers',
        '27': 'd7959e801195e05311be04517d04a522',
        '28': 'ANGLE(Intel(R)HDGraphics530Direct3D11vs_5_0ps_5_0)',
        '29': '7e884543c6009bb52269970b0ea58020',
        '30': 'cee2ad1773391cdf6e49e9964bc7303c',
        '31': '0',
        '32': '0',
        '33': '0',
        '34': '0',
        '35': '0',
        '36': '0',
        '37': '0',
        '38': '0',
        '39': '0',
        '40': '0',
        '41': '0',
        '42': '0',
        '43': '0',
        '44': '0',
        '45': '0',
        '46': '0',
        '47': '0',
        '48': '0',
        '49': '0',
        '50': '0',
        'fesig': '16916546741225850026',
        'ut': '1799',
        'appid': '0',
        'refer': 'https://ssl.captcha.qq.com/cap_union_new_show',
        'domain': 'ssl.captcha.qq.com',
        'fph': '11005F9FD4AA9989744D70495BAA1C0A31A38CD66129C76892277E3DE8C0F6AA8A37A68CEF10F44C60F82A90CA10A1BB8B3D',
        'fpv': '0.0.15',
        'ptcz': 'df3735dd1f598cd86380ea36edfacac272765b8b1ed28714a7c284ee8dbdae35',
        'callback': '_fp_047795'
    }
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('_fp_047795(', '').replace(')', ''))
    fpsig = result['fpsig']
    return fpsig


def get_eks(tdc_js):
    """
    获取 eks
    :param tdc_js:
    :return:
    """
    url = 'https://ssl.captcha.qq.com/' + tdc_js
    resp = session.get(url)
    try:
        eks = re.search('info="(_.*?)";', resp.text).group(1)
        return eks
    except:
        return None


def init_slider(aid, page_session):
    """
    初始化滑块
    :param aid
    :param page_session
    :return:
    """

    url = 'https://ssl.captcha.qq.com/cap_union_new_show'
    params = {
        'aid': aid,
        'captype': '',
        'curenv': 'inner',
        'protocol': 'https',
        'clientype': 2,
        'disturblevel': '',
        'apptype': 1,
        'noheader': '',
        'color': '',
        'showtype': 'point',
        'fb': 1,
        'theme': '',
        'lang': 2052,
        'grayscale': 1,
        'uid': '',
        'cap_cd': '',
        'height': 54,
        'rnd': 812249,
        'forcestyle': 'undefined',
        'rand': random.random(),
        'sess': page_session['session_id'],
        'firstvrytype': 1,
        'sid': page_session['sid'],
        'subsid': 1
    }
    resp = session.get(url, params=params)

    init_data = re.search('window.captchaConfig=(.*?);', resp.text).group(1)
    init_data = json.loads(init_data.replace('{', '{"').replace(',', ',"').replace(':', '":').replace('"://', '://'))
    cap_challenge = re.search(r'window.captchaConfig\.capChallenge=JSON.parse\("(.*?)"', resp.text).group(1)
    cap_challenge = json.loads(cap_challenge.replace('&quot;', '"'))
    return init_data, cap_challenge


def _slider_verify(start_time, ans, trace, page_session, init_data, fpsig, eks, cdata, referer):
    """
    最终验证
    :return:
    """
    url = 'https://ssl.captcha.qq.com/cap_union_new_verify'
    pass_time = int(time.time()) - start_time
    collect_data = format_data(page_session['sid'], trace, start_time, pass_time, referer)
    data = {
        'aid': init_data['aid'],
        'accver': 1,
        'showtype': 'popup',
        'ua': 'TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzc1LjAuMzc3MC44MCBTYWZhcmkvNTM3LjM2',
        'noheader': 1,
        'fb': '1',
        'ptcz': 'df3735dd1f598cd86380ea36edfacac272765b8b1ed28714a7c284ee8dbdae35',
        'fpinfo': f'fpsig={fpsig}',
        'tkid': '3344496876',
        'grayscale': '1',
        'clientype': '2',
        'subsid': '2',
        'sess': page_session['session_id'],
        'fwidth': 0,
        'sid': page_session['sid'],
        'forcestyle': 'undefined',
        'wxLang': '',
        'tcScale': 1,
        'uid': init_data['uid'],
        'cap_cd': '',
        'rnd': '691820',
        'TCapIframeLoadTime': 'undefined',
        'prehandleLoadTime': random.randint(50, 100),
        'createIframeStart': start_time * 1000 - random.randint(500, 1000),
        'ans': ans,
        'vsig': init_data['vsig'],
        'cdata': cdata,
        'websig': init_data['websig'],
        'subcapclass': init_data['subcapclass'],
        init_data['collectdata']: collect_data,
        'eks': eks,
        'tlg': len(collect_data),
        'vlg': '0_0_0'
    }
    resp = session.post(url, data=data).json()
    return resp


def crack(aid, referer):
    # 获取 session_id
    page_session = get_session(aid, referer)
    # 初始化滑块 iframe
    init_data, cap_challenge = init_slider(aid, page_session)
    print('初始化数据: ', init_data)
    # 获取 js 文件标识
    eks = get_eks(init_data['dcFileName'])
    start_time = int(time.time())
    # 获取设备指纹
    fpsig = get_fpsig()
    # 获取缺口距离
    distance = get_distance(session, init_data['cdnPic2'], init_data['cdnPic1'])
    # 图片尺寸处理
    distance = int(round(distance * (341 / 680)))
    # ans 距离处理
    ans = f'{process_distance(distance)},{init_data["spt"]};'
    print('缺口距离', distance)
    # 伪造轨迹
    trace = generate_trace(distance)
    cdata = u_challenge(cap_challenge)
    trace.append([0, 0, cdata])
    # 停顿一秒
    time.sleep(1)
    # 最终校验
    result = _slider_verify(start_time, ans, trace, page_session, init_data, fpsig, eks, cdata, referer)
    print('校验结果: ', result)
    return result


if __name__ == '__main__':
    # app_id, 使用的网站标识
    aid = 2100049389
    # 网站 url, 环境校验里会用到加密
    referer = "https://aq.qq.com/v2/uv_aq/html/reset_pwd/pc_reset_pwd_input_account.html?rand=1512991986334"
    x = crack(aid, referer)
    print(x)
