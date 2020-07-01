### 如若侵犯到贵公司权益，请发邮件到2217532592@qq.com告知，看到信息之后必删除，谢谢合作

### 文件说明
1. **get_analysis.js**: 获取七麦链接的加密参数 analysis
2. **test.py**: 通过python执行上面的 js 获取app排行榜

#### get_analysis.js 参数说明
需要传两个参数，一个为子 url，另一个为url的参数，比如这个链接**https://api.qimai.cn/rank/marketRank?analysis=dTBfAixaeUd9ZFtEdSBcTClgd1xwEx9CUV5bFwlWSg9RQjNRXltwEwUCAVYGClcFDlUIcBMB&market=2&category=198&date=2019-09-10**，穿得参数分别是**/rank/marketRank**、**{'market': 2, 'category': 198, 'date': '2019-09-09'}**,即可返回加密之后的 analysis 值