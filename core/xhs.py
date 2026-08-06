import json
import os
from pathlib import Path
from pprint import pprint
import subprocess
import time
from typing import Any
from curl_cffi import requests
import urllib
import execjs
import re
import logging
import random
import lxml
import redis
import math
import sqlite3

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'origin': 'https://www.xiaohongshu.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.xiaohongshu.com/',
    'sec-ch-ua': '"Not=A?Brand";v="99", "Microsoft Edge";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0',
    'x-b3-traceid': 'dd8b8b6743ecff2b',
    'x-rap-param': 'ByQBBgAAAAEAAAAUAAAB1CoaZlkAACg9AAAAJAAAAAAAAAAAeGFwdnpoJm3Xw7NJUAVze7+Kg4fN1AAAABAOuYQ2VEbyPa4JtmZRKdAnnoIbDBKlUlsDz4l9wLtbHquhf3Yp+sfttJ0VPvDBKc0xEffsPMLFL/4hlruyzW7z2fhyssGzhaSeTA2kRpYsBQDnNj+Fo+amzgnTEKv+p54zyfNJH+MebPxEvnYd1BZH17FVqfZ2adou3PG6061EC//xZD2IzxBnHDwPm3KE2LbBszFpskerAawZaWc/bDjbw+fEmlECyRA4qEHIKrEadBKXn9t4SrqPWKxdrvCFimxXUgorrh3H72wngugaxTAvOdkUyUGuQuMTLkK3tGCW8iN5n0Cr3IbFUGvmSd0GXXNutPTZeN661rHaOaMd+KMF+UAcWhY5WQ2i+auOGRXMKKcgg09TzGZDcggLrMIWZhsJN8KEU23aH2Q+a9NQQaLdt1ROp3vk4MMg4UQNPUFMQHkkwUC4yDLlI1WQnnr3RrrRnJJYdyCVnZyYviyqED/3m6SYbrsbsWvzlAPF/xVfF9AJ0tUVJXXVteEuWpcJDmzd1wtIBuKElOTCs3gGcv+Nn7qQREPhxfc0/kmGoU7HYiE1DqjVYYjqX+yTID6l2+Zf96CA2dFJVdFAjCsNwKxWSybXwyp6p3wnF8EOD3FZkQAAAcY=',
    'x-s': 'XYS_2UQhPsHCH0c1PUhEHjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIPAZlg94aGLTlLopFpgYDtFYY8Lkb4emk8ebsGD4D+g+awepnqf4x2bDAPLDUy0rM+FDF8eQpPnSxPd8g+SSGLgSI+b8My0pi+9QYJAmnJ9pMzpq6aF4UqFpCq/P7GgHAcLhhLpzg+dSLLBRVanFFPLlNwrTnN9QmPrkHaMY/adYnz9S1Pbz+c9EIqMQCLDkcpnbLP9Il8LT/Jfznnfl0yLLIaSQQyAmOarEaLSz+GFzMGnE9wpYGJsTMcgL7nS4S8rMp/jHVHdWFH0ijHjIj2eLjwjHl+n8DPBcMG0ZI8eYY+eGUG9PlGAmY8fch+0PIP0qAGUHVHdW9H0kvHdYiqUMIGUM78nHjwjQe/b+L+9pPygznLeZ3yok38FzQJS+VaFYLpSLRHdFVHdW7H0kvHdYiqUMIGUM78nHjwjQD8D+APFbYnnEnaBqEG7mC89SyyrQMJLTAqBuIwBMPPjQRKc==',
    'x-s-common': '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',
    'x-t': f'{int(time.time() * 1000)}',
    'x-xray-traceid': 'cfea712285ef3bf1a9dc0da8cc7f0eca',
    'cookie': 'abRequestId=35b100b5-d7f7-5fa6-af52-82151e849f72; a1=19b27173470jmu4jdf8cosnqayhhnh35dqf85zqmf50000136404; webId=a74a82425c063518a289a4f4b44203b0; gid=yjDJWyW4qyfJyjDJWyWq4AuAW8V674VfiYSli6iMIA0vxY28xIxq22888yqK4848DyY2iWdq; xsecappid=xhs-pc-web; ets=1785615270063; web_session=040069b0de1d7812247f8d1b5b384b33ddcc30; id_token=VjEAAJEi1ABvqJj99gHfP/AdDJKXrJLMWd3Dto3SUcVO8XGRu+e1ynWLgFicSX6q9s8E/EHx2UepCbtpWWjz90xZsqRrjiO5xzifQEcDnBQUodUf4Dhgsj0wsuorDxdrrLpAmm2e; x-rednote-datactry=CN; x-rednote-holderctry=CN; webBuild=6.36.7; acw_tc=0a0bb41a17859813951443791e4b954baa6d95848679f3a380d0cdc747a982; unread={%22ub%22:%226a5eeb18000000000402addc%22%2C%22ue%22:%226a6f21860000000028000eb7%22%2C%22uc%22:23}; loadts=1785981550571; websectiga=59d3ef1e60c4aa37a7df3c23467bd46d7f1da0b1918cf335ee7f2e9e52ac04cf; sec_poison_id=8ad306ae-feb5-4ab3-bf48-7de0b1f19393',
}

params = {
    'num':'30',
    'cursor':'699fc54c000000001d0279eb',
    'user_id':'610742f8000000000100b9ca',
    'image_formats':'jpg,webp,avif',
    'xsec_token':'AB4yJzVmuHLnxXKWKYUPp3WvueaRN441n2hgpQYVM-fz0=',
    'xsec_source':'pc_like'
}
q = "/api/sns/web/v1/user_posted"
x_t = str(int(time.time() * 1000))

# 3. 生成签名（确认您的 JS 文件是否接收了 x-t）
data = json.dumps(params, separators=(',', ':'))
pprint(data)
exit()
cmd = ["node", r"D:\pi-main\signature\xhs\function.js", q, data]
text = subprocess.check_output(cmd, encoding='utf-8')

# 4. 提取签名
match = re.search(r'X-s:\s*(.+)', text)
if not match:
    print("签名提取失败")
x_s = match.group(1).strip()


headers['x-s'] = x_s
headers['x-t'] = x_t

response = requests.get(
    'https://edith.xiaohongshu.com/api/sns/web/v1/user_posted?num=30&cursor=675195da0000000002039fb0&user_id=610742f8000000000100b9ca&image_formats=jpg,webp,avif&xsec_token=AB4yJzVmuHLnxXKWKYUPp3WvueaRN441n2hgpQYVM-fz0%3D&xsec_source=pc_like',
    headers=headers,
)
print(response.text)