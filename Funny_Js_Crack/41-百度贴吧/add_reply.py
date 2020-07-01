import execjs
import requests
import re
import random
import time


class Reply(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }
        self.add_href = "https://tieba.baidu.com/f/commit/post/add"
        self.session = requests.session()
        self.cookies = {
            # 'BDUSS': 'lJBWmxEYk5lOFUFBJCQAAAAAAAAAAAEAAAAsoIBBg9XS5MTjqnDcg52rgvsAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHC6c11wunNdS'
        }

        with open('get_form_data.js', 'r', encoding='utf-8') as f:
            get_bsk_js = f.read()
        self.ctx = execjs.compile(get_bsk_js)

        self.session.get('https://tieba.baidu.com/', headers=self.headers)

    def get_html(self, href):
        response = self.session.get(href, headers=self.headers)
        if "贴吧404" in response.text:
            print('请输入正确的标题或者该贴已被删除\n')
        elif response.status_code == 200:
            return response.text
        else:
            print('get_html 出问题了')

    def get_detail(self, href):
        html = self.get_html(href)
        if html:
            title = re.search("'threadTitle': '([^']+)'", html, re.S).group(1)
            fname = re.search('"forum_name":"([^"]+)"', html).group(1)
            fid = re.search('"forum_id":([\d]+),', html).group(1)
            tbs = re.search("tbs:\s*'([^']+)',", html).group(1)
            return {
                'title': title,
                'fname': fname,
                'fid': fid,
                'tbs': tbs
            }

    def get_form_data(self, tdata):
        bsk = self.ctx.call('get_bsk_data', tdata['tbs'])
        data = {
            'ie': 'utf-8',
            'kw': tdata['fname'],  # 吧名
            'fid': tdata['fid'],  # 吧 id
            'tid': tdata['tid'],  # 贴的id
            'vcode_md5': '',
            'floor_num': '28',  # 当前楼层数，可以随意
            'rich_text': '1',
            'tbs': "e5a55a45df7944b41567906433",  # 帖子首页就有，一定需要登陆
            'content': tdata['content'],  # 需要发的内容
            'basilisk': '1',
            'files': '[]',
            # 鼠标的轨迹 + 时间戳，直接模拟即可
            'mouse_pwd': bsk['mouse_pwd'],
            'mouse_pwd_t': bsk['mouse_pwd_t'],  # 时间戳
            'mouse_pwd_isclick': '1',
            'nick_name': '',
            '__type__': 'reply',
            'geetest_success': '1',
            '_BSK': bsk['bsk']
        }
        return data

    def add(self, tdata):
        succ = 0
        self.headers['Referer'] = tdata['href']
        data = self.get_form_data(tdata)
        for x in range(int(tdata['num'])):
            response = requests.post(self.add_href, headers=self.headers, data=data, cookies=self.cookies)
            data['floor_num'] = int(data['floor_num']) + 1
            if response.json()['no'] == 0:
                succ += 1
                time.sleep(0.5)
                data['content'] += str(random.randint(0, 100))
        print('顶贴成功 {} 次'.format(succ))
        flag = input('如果继续顶这贴请输入 1 ，输入任意键重新选择贴子\n>')
        if flag == '1':
            num = input('输入顶贴次数(一次性回复)\n>')
            while not re.match('^\d+$', num):
                num = input('请输入正确的数字\n>')
            tdata['num'] = num
            self.add(tdata)

    def run(self):
        while True:
            href = input('请输入你要进行顶贴的链接(比如：https://tieba.baidu.com/p/6248363819),退出请输入 #\n>')
            if href == '#':
                print('程序已退出，有问题或者建议请联系微信公众号：日常学python 进行改进，谢谢\n')
                break
            tid = re.search('/p/([\d]+)', href)
            if tid:
                tid = tid.group(1)
                href = "https://tieba.baidu.com/p/" + tid
                tdata = self.get_detail(href)
                print('贴吧：{}\n贴子：{}'.format(tdata['fname'], tdata['title']))
                content = input('输入你的顶贴内容\n>')
                num = input('输入顶贴次数(一次性回复)\n>')
                while not re.match('^\d+$', num):
                    num = input('请输入正确的数字\n>')
                tdata['tid'] = tid
                tdata['href'] = href
                tdata['content'] = content
                tdata['num'] = num

                self.add(tdata)

            else:
                print("请输入正确的链接")


if __name__ == '__main__':
    reply = Reply()
    reply.run()
