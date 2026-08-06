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
import logging
import random
import lxml
import redis
import math
import sqlite3
from .base import BaseSpider


class BiliBiliSpider(BaseSpider):
    session = requests.Session()
    session.headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'origin': 'https://space.bilibili.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://space.bilibili.com/1166997747/upload/video',
        'sec-ch-ua': '"Not=A?Brand";v="99", "Microsoft Edge";v="151", "Chromium";v="151"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0',
        'cookie': 'buvid3=4D0EB05A-50B6-9A34-CB63-13AE46228E3F10994infoc; b_nut=1764243310; _uuid=27E16E41-1B83-71064-2988-108C2F3B85210812228infoc; buvid4=89319043-50B8-D786-4796-D9CFA25B248864530-025062200-znwBXc/0EEDfqxuIbZrJ1DhDEjKpVASt8s/PD7B9qaegVmKcURDUpGTnv5AFLzF8; buvid_fp=64cb01ede65563bf96f2d92693c716c9; DedeUserID=688319368; DedeUserID__ckMd5=5f5dc4f07ec63413; theme-tip-show=SHOWED; rpdid=0zbfAGFteD|5Gq0EO8T|1sd|3w1VoAiS; theme-avatar-tip-show=SHOWED; CURRENT_BLACKGAP=0; LIVE_BUVID=AUTO2317677080664267; PVID=4; hit-dyn-v2=1; theme-switch-show=SHOWED; CURRENT_QUALITY=80; home_feed_column=5; browser_resolution=1632-891; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODYwNzAzMzcsImlhdCI6MTc4NTgxMTA3NywicGx0IjotMX0.I8S2lslfZsWCqvb_OQ4UGuQWnNfJL6B-7UEeoRYUcc0; bili_ticket_expires=1786070277; SESSDATA=77c4e131%2C1801439165%2C82ee6%2A82CjBEOxZDfGuNHv_tpCnL-MjGjSQSJbig4cym22bHGGS_QK-_mkSR-uCb9JhA3ggAffYSVi1LT2s3S0pmS1FDcDJUWFJOejhCcWFqZThZSl9ZTHA2SVNTblphNjdsRW5obkI1NnZEYWM4RlVjTnRYRTVBd0k5bFJ4VDM2bmVhVkxEOHg1X18wSUR3IIEC; bili_jct=764d8c64422ac869d6b1581b1f8ed464; sid=7io3elbu; bp_t_offset_688319368=1232930483269009408; CURRENT_FNVAL=4048; b_lsid=A6F7605B_19FD0364730',
    }
    # session.proxies = {
        
    # }
    name: str = "BiliBili"
    save_dir: Path = Path(name)
    def __init__(self):
        pass

    
    @staticmethod
    def get_wbi_key():
        response = BiliBiliSpider.session.get('https://api.bilibili.com/x/web-interface/nav')
        # pprint(response.json())
        wbi_img = response.json()["data"]["wbi_img"]
        img_key = wbi_img["img_url"].split('/')[-1].split('.')[0]
        sub_key = wbi_img["sub_url"].split('/')[-1].split('.')[0]
        wbi_key =  {
            'wbiImgKey': img_key,
            'wbiSubKey': sub_key
        }
        path = Path("a.txt")
        if not path.exists():
            path.write_text(json.dumps(wbi_key, ensure_ascii=False, indent=2))
        return wbi_key

    @staticmethod
    def get_wid_signature(params: dict[str, Any]):
        """
        Note: 获取bilibiliwid签名
        Args:
            params: 请求参数
        Returns:
            dict: 请求参数，包含wid签名
        """
        params.pop('w_rid', None)   # ← 删掉旧的签名
        params.pop('wts', None)     # ← 删掉旧的时间戳
        wbi_key = BiliBiliSpider.get_wbi_key()
        # wbi_key = {
        #     'wbiImgKey': '7cd084941338484aae1ad9425b84077c',
        #     'wbiSubKey': '4932caff0ff746eab6f01bf08b70ac45'
        # }
        js_path = r'signature\wid.js'
        with open(js_path, mode='r', encoding='utf-8') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        wid = ctx.call("XN", params, wbi_key)
        params.update(wid)
        return params

    @staticmethod
    def get_video_info():
        params = {
            'spm_id_from': '333.1387.upload.video_card.click',
            'vd_source': 'cd2f30c4c2b17931e5fe4b95752072ee',
        }
        response = BiliBiliSpider.session.get('https://www.bilibili.com/video/BV1Jb4y1N7RN/', params=params)
        # print(response.text)
        json_str = re.findall(r'window\.__INITIAL_STATE__\s*=\s*({.*?});', response.text, re.DOTALL)[0]
        json_dict = json.loads(json_str)
        # pprint(json_dict)
        aid = json_dict['aid']
        return aid



    def get_userspace_page(self):
        params = params = {
            "pn": "2",
            "ps": "40",
            "tid": "0",
            "special_type": "",
            "order": "pubdate",
            "mid": "1166997747",
            "index": "0",
            "keyword": "",
            "order_avoided": "true",
            "platform": "web",
            "web_location": "333.1387",
            "dm_img_list": '[{"x":5172,"y":4044,"z":0,"timestamp":3085,"k":64,"type":0},{"x":5235,"y":3829,"z":23,"timestamp":3269,"k":106,"type":0},{"x":5486,"y":1846,"z":30,"timestamp":3371,"k":106,"type":0},{"x":5688,"y":7,"z":168,"timestamp":3472,"k":99,"type":0},{"x":5885,"y":7,"z":450,"timestamp":3574,"k":94,"type":0},{"x":5644,"y":-530,"z":476,"timestamp":3676,"k":66,"type":0},{"x":5444,"y":-850,"z":498,"timestamp":3780,"k":96,"type":0},{"x":5065,"y":-1273,"z":159,"timestamp":3881,"k":87,"type":0},{"x":5111,"y":-1274,"z":346,"timestamp":3982,"k":83,"type":0},{"x":5600,"y":-789,"z":916,"timestamp":4082,"k":71,"type":0},{"x":5537,"y":-854,"z":859,"timestamp":4185,"k":83,"type":0},{"x":5772,"y":-619,"z":1094,"timestamp":4292,"k":121,"type":1},{"x":5710,"y":-55,"z":856,"timestamp":4403,"k":107,"type":0},{"x":6505,"y":4945,"z":559,"timestamp":4508,"k":120,"type":0},{"x":7794,"y":6779,"z":1593,"timestamp":4609,"k":73,"type":0},{"x":6489,"y":5670,"z":183,"timestamp":4710,"k":69,"type":0},{"x":7551,"y":6929,"z":1114,"timestamp":4814,"k":116,"type":0},{"x":7018,"y":6498,"z":528,"timestamp":4950,"k":96,"type":0},{"x":7481,"y":6963,"z":985,"timestamp":5058,"k":80,"type":0},{"x":8188,"y":3914,"z":632,"timestamp":6026,"k":63,"type":0},{"x":9039,"y":4751,"z":1732,"timestamp":6127,"k":65,"type":0},{"x":7953,"y":3897,"z":1997,"timestamp":6229,"k":80,"type":0},{"x":4299,"y":-313,"z":1207,"timestamp":7021,"k":78,"type":0},{"x":4662,"y":-263,"z":1497,"timestamp":7131,"k":87,"type":0},{"x":4919,"y":-252,"z":1710,"timestamp":7248,"k":61,"type":0},{"x":3335,"y":-2264,"z":76,"timestamp":7351,"k":79,"type":0},{"x":6214,"y":180,"z":2926,"timestamp":7452,"k":104,"type":0},{"x":5185,"y":-1109,"z":1849,"timestamp":7555,"k":65,"type":0},{"x":5084,"y":-1342,"z":1684,"timestamp":7659,"k":111,"type":0},{"x":6067,"y":-460,"z":2625,"timestamp":7763,"k":119,"type":0},{"x":5218,"y":-1497,"z":1742,"timestamp":7867,"k":100,"type":0},{"x":5406,"y":-1316,"z":1928,"timestamp":7978,"k":123,"type":0},{"x":4515,"y":-2138,"z":1060,"timestamp":8081,"k":97,"type":0},{"x":5472,"y":-381,"z":1917,"timestamp":8181,"k":98,"type":0},{"x":7068,"y":2656,"z":3399,"timestamp":8285,"k":102,"type":0},{"x":4603,"y":3535,"z":1919,"timestamp":16435,"k":64,"type":0},{"x":6615,"y":2441,"z":3819,"timestamp":16538,"k":68,"type":0},{"x":3055,"y":-1250,"z":261,"timestamp":16643,"k":103,"type":0},{"x":3428,"y":-866,"z":624,"timestamp":16745,"k":110,"type":0},{"x":6105,"y":1676,"z":3108,"timestamp":16847,"k":66,"type":0},{"x":3661,"y":-776,"z":688,"timestamp":16961,"k":102,"type":0},{"x":7460,"y":2811,"z":4364,"timestamp":17067,"k":63,"type":0},{"x":4883,"y":-62,"z":1732,"timestamp":17168,"k":66,"type":0},{"x":7094,"y":1067,"z":3762,"timestamp":17272,"k":103,"type":0},{"x":7721,"y":923,"z":4149,"timestamp":17378,"k":91,"type":0},{"x":5153,"y":-1719,"z":1481,"timestamp":17482,"k":118,"type":0},{"x":4765,"y":-2061,"z":1093,"timestamp":17587,"k":74,"type":0},{"x":6417,"y":-346,"z":2786,"timestamp":17691,"k":116,"type":0},{"x":4653,"y":-2031,"z":1061,"timestamp":17794,"k":74,"type":0},{"x":6205,"y":-472,"z":2615,"timestamp":17922,"k":77,"type":0}]',
            "dm_img_str": "V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
            "dm_cover_img_str": "QU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgUlRYIDQwNzAgTGFwdG9wIEdQVSAoMHgwMDAwMjg2MCkgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wLCBEM0QxMSlHb29nbGUgSW5jLiAoTlZJRElBKQ",
            "dm_img_inter": '{"ds":[{"t":7,"c":"dnVpX2J1dHRvbiB2dWlfYnV0dG9uLS1hY3RpdmUgdnVpX2J1dHRvbi0tYWN0aXZlLWJsdWUgdnVpX2J1dHRvbi0tbm8tdHJhbnNpdGlvbiB2dWlfcGFnZW5hdGlvbi0tYnRuIHZ1aV9wYWdlbmF0aW9uLS1idG4tbn","p":[6173,85,9411],"s":[274,444,548]}],"wh":[3906,1932,62],"of":[4688,6472,332]}',
            # "w_rid": "764ce589fe88beb4ae9b9da4362e8017",
            # "wts": "1785900881"
        }
        # params.update(get_a())
        pn = 1
        max_pn = math.ceil(self.get_navnum() / 40)
        while True:
            params = BiliBiliSpider.get_wid_signature(params=params)
            response = BiliBiliSpider.session.get(
                url='https://api.bilibili.com/x/space/wbi/arc/search',
                params=params,
            )
            # pprint(response.json())
            json_dict = response.json()
            
            for index, item in enumerate(json_dict['data']['list']['vlist'], start=1):
                bvid = item['bvid']
                title = item['title']
                url = f'https://www.bilibili.com/video/{item['bvid']}/?spm_id_from=333.1387.upload.video_card.click&vd_source=cd2f30c4c2b17931e5fe4b95752072ee'
                logging.debug(f"{index}, {item['title']}, {url}")
                if r.sismember("task_queue_set", bvid):
                    logging.debug(f"视频 {bvid} 已在队列中，跳过")
                    continue
                task = json.dumps({
                    "index": index,
                    "bvid": bvid,
                    "title": title,
                    "url": url
                })
                r.sadd("task_queue_set", bvid)
                r.lpush("task_queue", task)
            pn += 1
            params["pn"] = str(pn)
            time.sleep(random.uniform(3,10))
            return
            if pn > max_pn:
                return

            # if params["pn"] == 3:
            #     return

    def get_video_page(self):
        params = {
            'spm_id_from': '333.1387.upload.video_card.click',
            'vd_source': 'cd2f30c4c2b17931e5fe4b95752072ee',
        }
        response = BiliBiliSpider.session.get('https://www.bilibili.com/video/BV1NzKN6CEf6/', params=params)
        # print(response.text)
        json_str = re.findall(r'window\.__playinfo__\s*=\s*({.*?});?\s*</script>', response.text, re.DOTALL)[0]
        json_dict = json.loads(json_str)
        # pprint(json_dict)
        audio_url = json_dict['data']['dash']['audio'][0]['backupUrl'][0]
        video_url = json_dict['data']['dash']['video'][0]['backupUrl'][0]
        audio_bytes = BiliBiliSpider.session.get(audio_url).content
        video_bytes = BiliBiliSpider.session.get(video_url).content
        audio_path = "output.mp3"
        video_path = "output.mp4"
        output_path = "final_output.mp4"
        Path(video_path).write_bytes(video_bytes)
        Path(audio_path).write_bytes(audio_bytes)
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c', 'copy',           # 视频和音频都直接拷贝，不重新编码
            '-map', '0:v:0',        # 取第一个视频流
            '-map', '1:a:0',        # 取第一个音频流
            output_path,
            '-y'                    # 覆盖已有文件
        ]
        subprocess.run(cmd)
        os.remove(audio_path)
        os.remove(video_path)

    def get_navnum(self) -> int:
        params = {
            'mid': '1166997747',
            'web_location': '333.1387',
        }
        response = BiliBiliSpider.session.get('https://api.bilibili.com/x/space/navnum', params=params)
        pprint(response.json())
        json_dict = response.json()
        video_num = json_dict['data']['video']
        return video_num
    
    def get_video_comment(self):
        oid = BiliBiliSpider.get_video_info()
        params = {
            'oid': f'{oid}',
            'type': '1',
            'mode': '3',
            'pagination_str': '{"offset":""}',
            'plat': '1',
            'seek_rpid': '',
            'web_location': '1315875',
            # 'w_rid': '49825e02ed10b436c427df7ea124c0d0',
            # 'wts': '1785853247'
        }
        while True:
            params = BiliBiliSpider.get_wid_signature(params=params)
            response = BiliBiliSpider.session.get('https://api.bilibili.com/x/v2/reply/wbi/main', params=params)
            # pprint(response.json())
            next_offset = response.json()['data']['cursor']['pagination_reply']['next_offset']
            print(">>>>>>>>>>>>>>>>>>>>>>>>>" + next_offset)
            params['pagination_str'] = f'{{"offset":"{next_offset}"}}'
            time.sleep(random.uniform(1, 3))

    def get_followings_page(self, pn: int = 1):
        params = {
            'order': 'desc',
            'order_type': '',
            'vmid': '688319368',
            'pn': f'{pn}',
            'ps': '24',
            'gaia_source': 'main_web',
            'web_location': '333.1387',
        }
        while True:
            response = BiliBiliSpider.session.get('https://api.bilibili.com/x/relation/followings', params=params)
            # pprint(response.json())
            json_dict = response.json()
            for index, item in enumerate(json_dict['data']['list']):
                mid = item['mid']
                name = item['uname']
                url = f'https://space.bilibili.com/{mid}?spm_id_from=333.1387.follow.user_card.click'
                logging.debug(f"{index}, {name}, {mid}, {url}")
                cursor.execute(
                    "INSERT OR REPLACE INTO bilibili_users (mid, name, url) VALUES (?, ?, ?)",
                    (mid, name, url)
                )
            pn += 1
            params['pn'] = str(pn)
            time.sleep(random.uniform(1, 5))
            conn.commit()
            conn.close()
            return
        
    @classmethod
    def run(cls):
        obj = BiliBiliSpider()
        obj.get_video_info()
        # obj.get_video_comment()


