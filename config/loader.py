import sys
from pprint import pprint
import yaml
import importlib
from pathlib import Path


class ConfigLoader:
    @staticmethod
    def load_config(config_file: str = "spider.yaml", user_index: int = None):
        """
        加载爬虫配置并执行
        
        :param config_file: 配置文件名（默认 spider.yaml），相对于 config/ 目录
        :param user_index: 可选，仅运行指定索引的用户（0-based）；None 表示运行全部
        """
        config_path=Path(__file__).parent / config_file
        with open(config_path, 'r', encoding='utf-8') as f:
            config =  yaml.safe_load(f)
        sites = [site for site in config['sites'] if site['enabled'] == True]
        for site in sites:
            pprint(site)
            module_path, class_name = site['spider_class'].rsplit('.', 1)
            print(module_path, class_name)
            module = importlib.import_module(module_path)
            spider_class = getattr(module, class_name)
            print(spider_class)
            
            users = site['users']
            # 如果指定了 user_index，只运行该用户
            if user_index is not None:
                users = [users[user_index]]
            
            for user in users:
                spider_instance = spider_class.run(user['url'], user['flag'], user['page'])
            print('ok')




