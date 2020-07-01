import requests
import json
import execjs

headers = {
    'cookie': 'Last-Event-ID=65736c61662f38392f38356666393765643936312f67736d2d616964656d2d756e656d2d6e776f64706f72642d71792065646968112246b0fd1004bdb6f4',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}


with open('17track.js', 'r', encoding='utf-8') as f:
    track_js = f.read()

data = '{"guid":"","data":[{"num":"2781355999994"},{"num":"2781356000002"},{"num":"2781356000019"},{"num":"2781356000026"},{"num":"2781356000033"},{"num":"2781356000040"},{"num":"2781356000057"},{"num":"2781356000064"},{"num":"2781356000071"},{"num":"2781356000088"},{"num":"2781356000095"},{"num":"2781356000101"},{"num":"2781356000118"},{"num":"2781356000125"},{"num":"2781356000132"},{"num":"2781356000149"},{"num":"2781356000156"},{"num":"2781356000163"},{"num":"2781356000170"},{"num":"2781356000187"},{"num":"2781356000194"}],"timeZoneOffset":-480}'

ctx = execjs.compile(track_js)
event_id = ctx.call('get_cookie', data)
headers['cookie'] = 'Last-Event-ID=' + event_id
response = requests.post('https://t.17track.net/restapi/track', headers=headers, data=data)
content = response.json()
print(json.dumps(content, indent=2, ensure_ascii=False))
