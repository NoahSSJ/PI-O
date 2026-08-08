import json
import os
from pathlib import Path
from pprint import pprint
import subprocess
import time
from typing import Any
import requests
import urllib
import execjs
import re
import random
import lxml
import redis
import math
import sqlite3
from dataclasses import asdict, dataclass
from .base import BaseSpider
from typing import Optional


@dataclass
class TaskItem():
    name: str
    task_id: int
    text: str
    pic_list: list
    video_list: list
    # comments: list[str]


class WeiBoSpider(BaseSpider):
    __name__ = "微博"
    __version__ = "v1.0"
    
    session = requests.Session()
    session.headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'client-version': 'v1.1.237',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.weibo.com/u/7893929649?lpage=profileRecom',
        'sec-ch-ua': '"Not=A?Brand";v="99", "Microsoft Edge";v="151", "Chromium";v="151"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'server-version': 'v2026.08.04.3',
        'traceparent': '00-f3674a031dbfdc7845d9d04a9b18ca9e-f545c849741c8d9e-00',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': 'OpidnecPIHNkhLUm7-FBzW1p',
        'cookie': 'SCF=An5MUm-mu1X6x-0V5FRUjd-LAa4KRORjI-lp2JHLAbsMiD1gFuuG4rKdpQUE6Wobe8QAoqiRfCu5hVy8MnBD5qc.; SINAGLOBAL=46399716003.42463.1772234524992; ULV=1774265938331:6:4:3:3650358741503.078.1774265938329:1774265625480; XSRF-TOKEN=OpidnecPIHNkhLUm7-FBzW1p; SUB=_2A25HdYnADeRhGeFJ4lUR9CvMyTyIHXVkCoMIrDV8PUNbmtAYLRKjkW9Nfr-Ikkz8F6TsHvp-WZ-8sddvSZZJNs1-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh1DLBSZYmiLfaEW7-PxKxc5NHD95QNS0.NehBfehz7Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0M4S05XSK5Ee5tt; ALF=02_1788446352; WBPSESS=BWHVdTaHUrxrFPjSI85rtSHhHy60IqJ5jMnU_veNA6aGYytnnoXoSf6Fxw8UiQsAgJXJ_3KHyBqj_z7o7x6t54tqP7I_mpQK5fyPptTlCZNeB86DWM_FdX6l8ZKp795WmM1LPB2QYtJCoibvB71YEQ==',
    }
    session.proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "https://127.0.0.1:7890"
    }


    def __init__(self, url: Optional[str] = None):
        super().__init__()
        self.uid = url.split('/')[-1].split('?')[0]
    
    def get_userspace_info(self):
        params = {
            'uid': f'{self.uid}',
            'scene': 'profile',
        }
        response = WeiBoSpider.session.get('https://www.weibo.com/ajax/profile/info', params=params)
        json_dict = response.json()
        pprint(json_dict)

    def get_userspace_page(self):
        page = 1
        while True:
            params = {
                'uid': f'{self.uid}',
                'page': f'{page}',
                'feature': '0',
            }
            response = WeiBoSpider.session.get('https://www.weibo.com/ajax/statuses/mymblog', params=params)
            json_dict = response.json()
            # pprint(json_dict)
            for index, item in enumerate(json_dict['data']['list'], start=1):
                task_id = item['id']
                text = item['text']
                name = item['user']['screen_name']
                pic_list = []
                video_list = []
                self.logger.debug(text)
                if h265_mp4_hd := item.get('page_info', {}).get('media_info', {}).get('h265_mp4_hd'):
                    video_url = h265_mp4_hd
                    video_list.append(video_url)
                    
                pic_infos = item.get('pic_infos', {})
                if pic_infos:
                    for key, value in pic_infos.items():
                        pic_url = value.get('largest', {}).get('url', {})
                        self.logger.debug(pic_url)
                        pic_list.append(pic_url)
                if self.r.sismember('wb_set', task_id):
                    self.logger.debug(f"Task: {task_id} exists, skip.")
                    continue
                task = TaskItem(
                    name=name,
                    task_id=task_id,      # 转成 int
                    text=text,
                    pic_list=pic_list,
                    video_list=video_list,       # 留空，后续填充
                )
                task_dict = asdict(task)
                task_json = json.dumps(task_dict)
                self.r.sadd('wb_set', task_id)
                self.r.lpush('wb_list', task_json)
                yield task
            page += 1
    
    def download(self):
        task_list_key = 'wb_list'
        task_cnt = 0
        while True:
            task = self.r.rpop(task_list_key)
            if not task:
                break
            time.sleep(random.uniform(1.5,4.5))
            task_dict = json.loads(task)
            pprint(task_dict)
            task_id = str(task_dict['task_id'])
            task_dir = self.p.joinpath("weibo", task_id)
            task_dir.mkdir(parents=True, exist_ok=True)
            for index, item in enumerate(task_dict['video_list'], start=1):
                video_bytes =  WeiBoSpider.session.get(url=item).content
                video_path = task_dir.joinpath(f'{index}.mp4')
                Path(video_path).write_bytes(video_bytes)
            for index, item in enumerate(task_dict['pic_list'], start=1):
                pic_bytes = WeiBoSpider.session.get(url=item).content
                pic_path = task_dir.joinpath(f'{index}.png')
                Path(pic_path).write_bytes(pic_bytes)
            params = {
                'is_reload': '1',
                'id': f'{task_id}',
                'is_show_bulletin': '3',
                'is_mix': '0',
                'count': '10',
                'uid': f'{self.uid}',
                'fetch_level': '0',
                'locale': 'zh-CN',
            }
            response = WeiBoSpider.session.get('https://weibo.com/ajax/statuses/buildComments', params=params)
            # pprint(response.json())
            json_dict = response.json()
            text_list = []
            for index, item in enumerate(json_dict['data']):
                text = item['text_raw']
                text_list.append(text)
            md = "\n".join([f"- {item}" for item in text_list])
            print(md)
            task_cnt += 1
            if task_cnt == 1:
                break

    @classmethod
    def run(cls, url, flag=True):
        obj = WeiBoSpider(url=url)
        if flag:
            a = obj.get_userspace_page()
            for i in a:
                print(i)
        else:
            obj.download()



        
       

# if __name__ == "__main__":
#     WeiBoSpider.run()