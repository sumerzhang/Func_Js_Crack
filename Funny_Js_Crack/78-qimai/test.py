import requests
import execjs

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.qimai.cn/rank/marketRank',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Sec-Fetch-Mode': 'cors',
}

with open('get_analysis.js', 'r', encoding='utf-8') as f:
    get_analy_js = f.read()

ctx = execjs.compile(get_analy_js)
analy = ctx.call('get_analysis', "/rank/marketRank", {'market': 2, 'category': 198, 'date': '2019-09-09'})

url = 'https://api.qimai.cn/rank/marketRank?analysis={}&market=2&category=198&date=2019-09-09'
response = requests.get(url.format(analy), headers=headers)
for x in response.json()['rankInfo']:
    print(x)

