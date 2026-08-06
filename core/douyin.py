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

@dataclass
class DataItem():
    name: str
    sec_user_id: str
    aweme_id: str
    desc: str
    pic_list: list[bytes]
    video_list: list[bytes]

class DouyinSpider(BaseSpider):
    session = requests.Session()
    session.headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com/user/MS4wLjABAAAAjtoaYQ96ZRXpuyeXR_emrMPqMD2OpaYnktsMdn_ZBZe8Um7VFd7uWChCOJkBzlJ9?from_tab_name=main&vid=7669013193251735272',
        'sec-ch-ua': '"Not=A?Brand";v="99", "Microsoft Edge";v="151", "Chromium";v="151"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'uifid': '29a1f63ec682dc0a0df227dd163e2b46e3a6390e403335fa4c2c6d1dc0ec5ffa8aa6438c57fda3f18128b16e092adfd0bee65d4dc8858ba767cd584c3a76aee55be56012dffde7c23c10f7c09e01d8e7cc89656607415db684e60776b43fbac457ad15a0e1ccd09fe52ba7c81e2d0cd64431c06eb29927d3094726bdfb6263acb7aff8159e4a787cbe677f88a6821f1f7209084d97ca445990a4eb956b93618d',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36 Edg/151.0.0.0',
        'cookie': 'enter_pc_once=1; UIFID_TEMP=29a1f63ec682dc0a0df227dd163e2b46e3a6390e403335fa4c2c6d1dc0ec5ffa30111749c74fb73c84e778e8eadb65802f59608c9e983ed8c22ceca6592f05f717c6c28f94bbb00fb53ed1d3b86dc11c3a624dcfd50f3817b86933e365efd4a789330a612bab1d34a5ac143f2c250541; hevc_supported=true; fpk1=U2FsdGVkX1+P5GYYz4dUXtDPA7+5/DniDTJSO16isMZwImnb5DCq//CVHNiDek46RzyJ48xv++R7CDsrZbaqnQ==; fpk2=800cce95768a9a4605cb3f6b181e9057; UIFID=29a1f63ec682dc0a0df227dd163e2b46e3a6390e403335fa4c2c6d1dc0ec5ffa8aa6438c57fda3f18128b16e092adfd0bee65d4dc8858ba767cd584c3a76aee55be56012dffde7c23c10f7c09e01d8e7cc89656607415db684e60776b43fbac457ad15a0e1ccd09fe52ba7c81e2d0cd64431c06eb29927d3094726bdfb6263acb7aff8159e4a787cbe677f88a6821f1f7209084d97ca445990a4eb956b93618d; xgplayer_device_id=82175310514; xgplayer_user_id=305054426302; SEARCH_UN_LOGIN_PV_CURR_DAY=%7B%22date%22%3A1765539693418%2C%22count%22%3A4%7D; my_rd=2; SEARCH_RESULT_LIST_TYPE=%22single%22; theme=%22dark%22; manual_theme=%22dark%22; d_ticket=d0275762bccab2aedd0cd67b6a4644e5a669c; n_mh=lYcY7BLdmTEXV1EP3f8GdNh6MVYSRtVifLe4-4eubLc; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.131%7D; SelfTabRedDotControl=%5B%7B%22id%22%3A%226910181298262788103%22%2C%22u%22%3A132%2C%22c%22%3A0%7D%5D; __ac_nonce=06a73b8d80081c0a8301c; __ac_signature=_02B4Z6wo00f01ttCpaAAAIDCVQ.Tl9luItrbYqEAANywec; s_v_web_id=verify_msgnquc2_xaJkawK5_IWN1_4kdb_Bwwy_sUCkKJQUsFMi; douyin.com; device_web_cpu_core=32; device_web_memory_size=32; architecture=amd64; is_support_rtm_web_ts=1; dy_swidth=2048; dy_sheight=1280; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2048%2C%5C%22screen_height%5C%22%3A1280%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A32%2C%5C%22device_memory%5C%22%3A32%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; is_dash_user=1; strategyABtestKey=%221785968866.571%22; passport_csrf_token=9caff46c37e395c775b04471d20affce; passport_csrf_token_default=9caff46c37e395c775b04471d20affce; bd_ticket_guard_client_web_domain=2; gulu_source_res=eyJwX2luIjoiM2E4YWFkNDhmZWMyYWRhMDVhNjVkYWU2ZGQ2OTRkMzg0Nzg2NWEyNzc3MjA5MDgzZTA1N2ZmZWE3NDRjNTE2YSJ9; download_guide=%221%2F20260806%2F0%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A0%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; ttwid=1%7C5T9Q_FfTCayu_wY0tEFz49lUU43H4Xtz4ekaBkvH_zc%7C1785968931%7C68523add32db5579650b3a7c8372b4b50f01f6cec40e209d003d31326159305a; passport_assist_user=Cj0OJccre_vd8VYCdnjTwbUyG3ufYCq-hu-UaF1JQRDqB9R6f97G727ZWrQqH_4Je731TkEzR3t9OEcyFGQHGkoKPAAAAAAAAAAAAABQvgR92Uw_qdxoireY5ALZQnQSp4Jrqfvd07rEbNq0JlPlIzTaxjJOw9NUhNg1HU3CyBDI4pgOGImv1lQgASIBA4Ha-N0%3D; sid_guard=b23d1a617985b576668bd4a7edb5d7c3%7C1785968964%7C5184000%7CSun%2C+04-Oct-2026+22%3A29%3A24+GMT; uid_tt=8138434ff4b6a449247d994442f0db9e; uid_tt_ss=8138434ff4b6a449247d994442f0db9e; sid_tt=b23d1a617985b576668bd4a7edb5d7c3; sessionid=b23d1a617985b576668bd4a7edb5d7c3; sessionid_ss=b23d1a617985b576668bd4a7edb5d7c3; session_tlb_tag=sttt%7C13%7Csj0aYXmFtXZmi9Sn7bXXw_________-o0mL-sl6ORJmy2M3518OvwOxGwSXGSp7KISDlfdsIaAg%3D; is_staff_user=false; has_biz_token=false; sid_ucp_v1=1.0.0-KGEyMmEyNjczMDA3MTMyZWFmNzYwOTZkYTFmNjg5MjFjNWZjNTIzOWIKHwiEwauR_gIQxPLO0wYY7zEgDDD4wKDbBTgHQPQHSAQaAmhsIiBiMjNkMWE2MTc5ODViNTc2NjY4YmQ0YTdlZGI1ZDdjMw; ssid_ucp_v1=1.0.0-KGEyMmEyNjczMDA3MTMyZWFmNzYwOTZkYTFmNjg5MjFjNWZjNTIzOWIKHwiEwauR_gIQxPLO0wYY7zEgDDD4wKDbBTgHQPQHSAQaAmhsIiBiMjNkMWE2MTc5ODViNTc2NjY4YmQ0YTdlZGI1ZDdjMw; bd_ticket_guard_generate_ticket_time=2026-08-06/06:29:24; bd_ticket_guard_ts_sign_id=ts.2.7c8e2cc77d1310b; _bd_ticket_crypt_cookie=8c6a4e3e220d9b36c88e6c2f436fc336; __security_mc_1_s_sdk_sign_data_key_web_protect=86f05d71-4801-b838; __security_mc_1_s_sdk_cert_key=ab88abde-44a2-ac3a; __security_mc_1_s_sdk_crypt_sdk=003378bc-479e-af7a; __security_server_data_status=1; login_time=1785968964549; publish_badge_show_info=%220%2C0%2C0%2C1785968965794%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAsSnYSMZLcUc12iKKd2zu28mCgBEmKNQ3jpis7dBEgak%2F1786032000000%2F0%2F1785968965990%2F0%22; __druidClientInfo=JTdCJTIyY2xpZW50V2lkdGglMjIlM0E1ODMlMkMlMjJjbGllbnRIZWlnaHQlMjIlM0ExMDUzJTJDJTIyd2lkdGglMjIlM0E1ODMlMkMlMjJoZWlnaHQlMjIlM0ExMDUzJTJDJTIyZGV2aWNlUGl4ZWxSYXRpbyUyMiUzQTEuMjUlMkMlMjJ1c2VyQWdlbnQlMjIlM0ElMjJNb3ppbGxhJTJGNS4wJTIwKFdpbmRvd3MlMjBOVCUyMDEwLjAlM0IlMjBXaW42NCUzQiUyMHg2NCklMjBBcHBsZVdlYktpdCUyRjUzNy4zNiUyMChLSFRNTCUyQyUyMGxpa2UlMjBHZWNrbyklMjBDaHJvbWUlMkYxNTEuMC4wLjAlMjBTYWZhcmklMkY1MzcuMzYlMjBFZGclMkYxNTEuMC4wLjAlMjIlN0Q=; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAsSnYSMZLcUc12iKKd2zu28mCgBEmKNQ3jpis7dBEgak%2F1786032000000%2F0%2F1785968980987%2F0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCS01IdnRFaHE1Wk5BRFcwQVprYnhmNFB1cjNGZExpbVZQcTdaT3IreXNsRDJSMzFqalBuM0t2QS95aEY0WGNaeEhhWVZuWk9UbC9MbTBPaVVWOHUvdmc9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; home_can_add_dy_2_desktop=%221%22; odin_tt=ea7809db320a2cd5b555e3aff131bbd1be3586d4ea04ca9ffccb17ae32015e382ca40f9c6557e2354b4a082c17b1ec57f4f9e8588d3056fd27d514ad6001685150e9a250a36c796e4d90a3801afc27e9; sdk_source_info=7e276470716a68645a606960273f276364697660272927676c715a6d6069756077273f276364697660272927666d776a68605a607d71606b766c6a6b5a7666776c7571273f275e5927666d776a686028607d71606b766c6a6b3f2a2a756e756e636d6b666c63666e686e6e63606e6f686a616f636b6f6b63666368602a6c6b6f6066715666776c75712b6f76592758272927666a6b766a69605a696c6061273f27636469766027292762696a6764695a7364776c6467696076273f275e582729277672715a646971273f2763646976602729277f6b5a666475273f2763646976602729276d6a6e5a6b6a716c273f2763646976602729276c6b6f5a7f6367273f27636469766027292771273f273d323c3034343c333c303d3234272927676c715a75776a716a666a69273f2763646976602778; bit_env=Qt7e7TKscWiFxkxGt7j8FbLj9g_YXE9ZpcgfDBkj_wOMeMvMkHEbIUgWPjgB9C8RHFwr8ctMeWYzUjaF8XbIr4CdsrSZHZbvZU4ubc5bSJGCiV8ZeXFLvSws7xl8KWae-QvogDoM7U1lEgAaYMAVzkTAE2EmPL6PpEfeYiCa53YdabMh0r4N_FA0yuhaqvW0jXX35JebWEvI--E6TQx1dlX8H1EkQqoRuAWiSbZ_Xh6Dp52nj_uvPPnFcAyxF5IWefVyBRYsSd3WorxuWDL3PGJyjyq1WFV84HfuPJqqSZDZKRDknzKX4MyAesrcDUlQuPXVFnt9typrNi8UP1gsOepEH1y6xY9MjkRaCTXlTRpkD4BTAouvUyPK84Cj6o1l00JNARdBAjpgLHuTqKTH2iMMurEilczbzMwFug_IHvxUVFk2dEw1akuK-Yy-i1n6FJWRpBM7G84d1XfimFn6zxQiUH-OyWO2rRttuqu4lemd82O7Nc4B1qgldipwHz2qmL0G2VsiLyJ3rJJVBPW-my4vlgnRli7ozZ4r3copdjw%3D; passport_auth_mix_state=0gznjlem5hrjj3yr27o3u9p7kp61lj7i; biz_trace_id=a599d280; bd_ticket_guard_client_data_v2=eyJyZWVfcHVibGljX2tleSI6IkJLTUh2dEVocTVaTkFEVzBBWmtieGY0UHVyM0ZkTGltVlBxN1pPcit5c2xEMlIzMWpqUG4zS3ZBL3loRjRYY1p4SGFZVm5aT1RsL0xtME9pVVY4dS92Zz0iLCJ0c19zaWduIjoidHMuMi43YzhlMmNjNzdkMTMxMGI3YjJhOTMxNjYxZGQ5MmYxZTkwYjBmMTRiZjg1Yjg2YzFiNzI3NDM3MjUzOTU0MTIwYzRmYmU4N2QyMzE5Y2YwNTMxODYyNGNlZGExNDkxMWNhNDA2ZGVkYmViZWRkYjJlMzBmY2U4ZDRmYTAyNTc1ZCIsInJlcV9jb250ZW50Ijoic2VjX3RzIiwicmVxX3NpZ24iOiI1Mmpwb1NrOHVGeGc4ODdCb1lHRGU1VVA4TUxiMnErNXpNaHEyZmpmSW1VPSIsInNlY190cyI6IiN0endYam5aUklVOE5rcHRaNlhVcy8xeERMTFZqMFZkUjB0M2RHZENEV2NmdXVHbGVza1k4V3BNbFRaWkwifQ%3D%3D; IsDouyinActive=true',
    }
    session.proxies = {}
    def __init__(self, url):
        super().__init__()
        self.url = url

    def get_userspace_page(self):
        params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'channel': 'channel_pc_web',
            'sec_user_id': 'MS4wLjABAAAAQXVbKMP5YXy8o8orFAYqFJXd_lpJTHg0_WmTL0wn3T4',
            'max_cursor': '0',
            'locate_query': 'false',
            'show_live_replay_strategy': '1',
            'need_time_list': '1',
            'time_list_query': '0',
            'whale_cut_token': '',
            'cut_version': '1',
            'count': '18',
            'publish_video_strategy_type': '2',
            'from_user_page': '1',
            'update_version_code': '170400',
            'pc_client_type': '1',
            'pc_libra_divert': 'Windows',
            'support_h265': '1',
            'support_dash': '1',
            'cpu_core_num': '32',
            'version_code': '290100',
            'version_name': '29.1.0',
            'cookie_enabled': 'true',
            'screen_width': '2048',
            'screen_height': '1280',
            'browser_language': 'zh-CN',
            'browser_platform': 'Win32',
            'browser_name': 'Edge',
            'browser_version': '151.0.0.0',
            'browser_online': 'true',
            'engine_name': 'Blink',
            'engine_version': '151.0.0.0',
            'os_name': 'Windows',
            'os_version': '10',
            'device_memory': '32',
            'platform': 'PC',
            'downlink': '10',
            'effective_type': '4g',
            'round_trip_time': '50',
            'webid': '7641624767225775631',
            'uifid': '29a1f63ec682dc0a0df227dd163e2b46e3a6390e403335fa4c2c6d1dc0ec5ffa8aa6438c57fda3f18128b16e092adfd0bee65d4dc8858ba767cd584c3a76aee55be56012dffde7c23c10f7c09e01d8e7cc89656607415db684e60776b43fbac457ad15a0e1ccd09fe52ba7c81e2d0cd64431c06eb29927d3094726bdfb6263acb7aff8159e4a787cbe677f88a6821f1f7209084d97ca445990a4eb956b93618d',
            'msToken': 'ULebQ4UgO75zrbJVuAcVdVCFCzpb0SqPFJE77MSLVoFWXXVIBa7UfHwFsvd_QdOoECadGf38fnvmyrHFt22brqLwg7nug84eej-7kVfB0KPtEx6cj1MNKiWXowsp0DKLM6YPlzPiMuaarQBL_yUSJWz1vTIRbKbcayQ5hr4dIigzzH_cpQBvuQ==',
            'a_bogus': 'EX05gqyjQNQcKdKGYOaOCC9UGSyMNsuymeioWyPTyOOcaH0aI8NXQxt/noqa4dEvBuBTkCI7xDFAbxncuTU0ZFrpLmkfSLXSzTVInh6oZHpZGPJ21NRLCSUFoXsO8csueA53iI46hUrwIE5-ZqQg/Q3yHKLCQObkONQWkMYbE9k61FgAg1cHPBbkYXGqiD==',
            'verifyFp': 'verify_msgnquc2_xaJkawK5_IWN1_4kdb_Bwwy_sUCkKJQUsFMi',
            'fp': 'verify_msgnquc2_xaJkawK5_IWN1_4kdb_Bwwy_sUCkKJQUsFMi',
            'timestamp': '1785971195',
            'x-secsdk-web-signature': 'ff9ce3bd134d2d2bd3a59c0fec8de0db',
        }

        response = DouyinSpider.session.get('https://www.douyin.com/aweme/v1/web/aweme/post/', params=params)
        # pprint(response.json())
        json_dict = response.json()
        for index, item in enumerate(json_dict['aweme_list'], start=1):
            aweme_id = item['aweme_id']
            desc = item['desc']
            self.logger.debug(f" >>>>>>>>>>正在第{index}个:")
            video_list = []
            image_list = []
            if video := item.get('video', {}):
                if video.get('bit_rate', {}):
                    video_url = video['bit_rate'][0]['play_addr']['url_list'][0]
                else:
                    video_url = video['play_addr']['url_list'][0]
                # self.logger.debug(video_url)
                video_list.append(video_url)
            if images := item.get('images', {}):
                # print(images)
                for index, item in enumerate(images, start=1):
                    image_list.append(item["url_list"][0])
                self.logger.debug(image_list)
                
            task = DataItem(
                name='',
                sec_user_id='',
                aweme_id=aweme_id,
                desc=desc,
                pic_list=image_list,
                video_list=video_list
            )
            
            




    @classmethod
    def run(cls):
        obj = DouyinSpider(url='https://www.douyin.com/user/MS4wLjABAAAAQXVbKMP5YXy8o8orFAYqFJXd_lpJTHg0_WmTL0wn3T4')
        obj.get_userspace_page()


