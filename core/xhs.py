import json
import os
from pprint import pprint
import random
import re
import time
import requests
from playwright.sync_api import sync_playwright
from pathlib import Path
from .base import BaseSpider

class XhsSpider(BaseSpider):
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.name = 'xhs'

    def open_userspace_page(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False,)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport=None
            )
            page = context.new_page()

            # 1. 先访问小红书
            page.goto("https://www.xiaohongshu.com/")
            cookie_path = self.auth.joinpath("ck.json")
            if cookie_path.exists():
                cookie_str = cookie_path.read_text(encoding='utf-8')
                cookies = json.loads(cookie_str)
                context.add_cookies(cookies)
            else:
                # 2. 等待你扫码登录，等15秒
                self.logger.info("请扫码登录，15秒后自动保存Cookie")
                page.wait_for_timeout(15000)
                cookie = context.cookies()
                cookie_path = self.auth.joinpath("ck.json")
                # Path(cookie_path).read_text(encoding='utf-8')
                cookie_path.write_text(json.dumps(cookie, ensure_ascii=False, indent=2), encoding='utf-8')
                self.logger.debug(f'cookie已保存到:{cookie_path.resolve()}')
            page.on("response", self.on_response) 
            page.goto(self.url)
            page.wait_for_timeout(5000)
            page.mouse.wheel(0, 1000)
            page.on("response", self.on_response)    
            page.wait_for_timeout(1000000)

    def on_response(self, response):
        # 只抓笔记 / 用户相关接口
        # print(response.url)
        if '/v1/user_posted' in response.url:
            print('抓到小红书接口:', response.url)
            data = response.json()
            pprint(data)
            json_dict = data
            for index, item in enumerate(json_dict['data']['notes'], start=1):
                note_id = item['note_id']
                xsec_token = item['xsec_token']
                title = item['display_title']
                url = f'https://www.xiaohongshu.com/explore/{note_id}?xsec_token={xsec_token}&xsec_source=pc_like'
                self.logger.debug(f"{index}, {title}, {url}")
                if self.r.sismember("xhs_set", note_id):
                    self.logger.debug(f"{note_id}已在队列中,跳过")
                    continue
                task = json.dumps({
                    "note_id": note_id,
                    "xesc_token": xsec_token,
                    "title": title,
                    "url": url
                })
                self.r.sadd("xhs_set", note_id)
                self.r.lpush("xhs_list", task)
            time.sleep(random.uniform(3, 10))

    def download(self):
        task_list_key = 'xhs_list'
        task_cnt = 0
        while True:
            task = self.r.rpop(task_list_key)
            if not task:
                break
            task_dict = json.loads(task)
            pprint(task_dict)
            task_id = str(task_dict['note_id'])
            task_dir = self.p.joinpath(self.name, task_id)
            task_dir.mkdir(parents=True, exist_ok=True)

    def get_note_page(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="151", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'cookie': 'webBuild=6.36.7; xsecappid=xhs-pc-web; acw_tc=0a00d0cf17859963020297351e8c62c8e96ebc8ac4210b449ce462eff2de58; abRequestId=01285ceb-b22d-54ee-8d5b-64b6bf37b009; ets=1785996302756; a1=19fd5acd9f8sa66nzgqqdlqnydpr6b51b96npjzl350000352677; webId=434a081285bd4aec4c7659c929444137; websectiga=7750c37de43b7be9de8ed9ff8ea0e576519e8cd2157322eb:72ecb429a7735d4; gid=yjif20Sdj4DKyjif20SfjjVuiYM0KKIukAAfK1q1AIvfUI28FKD2yU888q2JKWW8KfD4KYy8; web_session=040069b0de1d7812247f716c41384bbba7ca13; id_token=VjEAAAQllTJSQCPBEwhWT+N44T/qXr/EoEkakS3gQApDC6BtHn9AhQjC9wqdWEmg4VleWgMcPiDvUnC3aqFtN2pmVJKbORVXXyR/DvzsEgRJf63SzyazOdLR19UASx9bc+FTFaHY; x-rednote-datactry=CN; x-rednote-holderctry=CN; unread={%22ub%22:%226a3def2a000000000603693d%22%2C%22ue%22:%226a3eed470000000008024f57%22%2C%22uc%22:26}; loadts=1785997377748',
        }

        response = requests.get('https://www.xiaohongshu.com/explore/66b604dd000000000502367f?xsec_token=ABSqiIqidUv2vhKQ69Roiu1krKNmhkHhkvVMFlWyRc48Y=&xsec_source=pc_like', headers=headers)
        # print(response.text)
        json_str = re.findall(r'window\.__INITIAL_STATE__\s*=\s*({.*?});?\s*</script>', response.text, re.DOTALL)[0].replace('undefined', 'null')
        json_dict = json.loads(json_str)
        pprint(json_dict)
                    






    @classmethod
    def run(cls, url):
        obj = XhsSpider(url=url)
        # obj.open_userspace_page()
        obj.get_note_page()




