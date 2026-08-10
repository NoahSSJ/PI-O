from pprint import pprint
import requests
import json
from pathlib import Path
import urllib
import execjs

class XhsSpider():
    session = requests.Session()
    session.headers = {
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
        'x-b3-traceid': '9340abcec209ea5c',
        'x-rap-param': 'ByQBBgAAAAEAAAAUAAABlCzQkjEAACg9AAAAHQAAAAAAAAAAcnp1NXAwcxwfTFVkns+87C1VoYXEZAAAABCnqEU22J1Noasq6Z7fNkVhOo3q8octqSrtR4wRMH1fHT8b5w8GSh4qxLOrFuAfFUgG6r92GUCSyDfSpEwTKA2GnVINy+dhoS+G3A59ydbHrpM5XOJCBYi09xEP9gYDQPc8WWlSTlcpKYtTmLaz42Jjx+DgMMIhXavUfTCQsKI7yd9Hy426COk+5tdy8gzgExyEbZvz42RKtwQ3aIHwhfv0oj406ZPM3AzSZdydbPe2O2tcFfEulYSh9ATmSwddg9795WUdfKg8saA9ezFJL5bNNkOfmdovPGGNH+otzNxWB7zdveehzYVBXK+baUWEP86tlZlnFsTuF+Th+FG5NjQUX5BFrxC5RHq83btgxc9QeoK0N3c0Ptg/6ehLkrRInmxyfTyEbr9q8UQrB3In4s7yVxPnCUze1nirtvupuTgNKlTynrxSWiOcqwDFNTS7K0DjAy5QV7jXrXjcFzYJQMVbuSrbfFcsceC5F6uLVEEtgGYH9pozKM7c5GL6RqV0W8rOmAu00MHyG09WpoFEpFOiAAABjg==',
        'x-s': 'XYS_2UQhPsHCH0c1+shlHjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIPAZlg94aGLTlGfrA2o8sJbphqfpb4emk8r+FafcEGg+awepncA4x2bSo8rDUy0rM+FDF8BYNJ0bca/YxJ9VALgSI+b8My0pi+9QYJAmnJ9pMzpq6aF4UqFpCq/P7GgHAcLhhLpzg+dSLLBRVanFFPLlNwrTnN9QmPrkHaMY/adYnz9S1Pbz+c9EIqMQCLDkcpnbLP9lsqDT/Jfznnfl0yLLIaSQQyAmOarEaLSz+q9ROLB4z2fTb8AS9qLktG/D6zr+lGjHVHdWFH0ijHjIj2eLjwjHFwecMPfHMPAW7GA+Swnbf+fz0G0D7PBrl+/pYP98fGjHVHdW9H0kvHdYiqUMIGUM78nHjwjQsnS892bZ9aDpzpLSIaSSF2oprzSQ68D8IpBuRHdFVHdW7H0kvHdYiqUMIGUM78nHjwjQe+pp6yFRCP/mgpoYDcfbVc0QEJd8Lcg4Sy/4G2LMUasQRKc==',
        'x-s-common': '2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1+shlHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjH9N0P7N0PjNsQh+aHCH0rEG0H7P/qA+eqIyfMM+BkD80Y0J7+1qnbEyBY1yePM8obfwepCqnMf+/ZIPeZlPAGFPecjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FDAaeFjNsQhwaHCN/rhwecAP/rA+AqVHdWlPsHCPsIj2erlH0ijJfRUJnbVHjIj2erUH0ijP/qh+0PFw/LF+eLhweVl+AW9PeWMw/HUP/rEHdF=',
        'x-t': '1786349547819',
        'x-xray-traceid': 'cff55d788abdf34f4d5c90bfead1373f',
        'cookie': 'abRequestId=35b100b5-d7f7-5fa6-af52-82151e849f72; a1=19b27173470jmu4jdf8cosnqayhhnh35dqf85zqmf50000136404; webId=a74a82425c063518a289a4f4b44203b0; gid=yjDJWyW4qyfJyjDJWyWq4AuAW8V674VfiYSli6iMIA0vxY28xIxq22888yqK4848DyY2iWdq; xsecappid=xhs-pc-web; ets=1785615270063; x-rednote-datactry=CN; x-rednote-holderctry=CN; web_session=040069b0de1d7812247fe26341384b7617a18c; id_token=VjEAAC+u1ng+Ml1q5hng+LWj4aHzDqa+2T6DvJmTMJ9FbdpX8yCF6PU8FhNTTW15s10WmKyO4spVXrHiU3DlFi9zEouVediqFhMq2gCZ9bKqd/jPhiwPCAKMM5EvxOK4yFRwItyq; webBuild=6.37.3; unread={%22ub%22:%226a69dadf000000000f00bfe6%22%2C%22ue%22:%226a7703fc000000002500cc3b%22%2C%22uc%22:13}; loadts=1786349544334; acw_tc=0a0bb41417863495448177491e41590baffbe24a8497c0d705c250b000f4ef; websectiga=cf46039d1971c7b9a650d87269f31ac8fe3bf71d61ebf9d9a0a87efb414b816c; sec_poison_id=c81e1257-23fa-4aca-b586-c33f71ec5bc7',
    }
    session.proxies = {}

    def __init__(self):
        pass
    
    def get_userspace_page(self, cursor: str, user_id: str, xsec_token: str):
        params = {
            'num': '30',
            'cursor': f'{cursor}',
            'user_id': f'{user_id}',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': f'{xsec_token}',
            'xsec_source': 'pc_like'
        }
        url_param = '/api/sns/web/v1/user_posted?' + urllib.parse.urlencode(params, safe=',')
        js_path = Path(__file__).parent.parent / "signature" / "main.js"
        js_code = Path(js_path).read_text(encoding='utf-8')
        ctx = execjs.compile(js_code)
        x_s = ctx.call('seccore_signv2', url_param)
        XhsSpider.session.headers['x-s'] = x_s
        response = XhsSpider.session.get("https://edith.xiaohongshu.com"+url_param)
        pprint(response.json())

    @classmethod
    def run(cls):
        obj = XhsSpider()
        obj.get_userspace_page()

XhsSpider.run()