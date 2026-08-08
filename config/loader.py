import sys
from pprint import pprint
import yaml
import importlib
from pathlib import Path


class ConfigLoader:
    @staticmethod
    def load_config():
        config_path=Path(__file__).parent / "spider.yaml"
        with open(config_path, 'r', encoding='utf-8') as f:
            config =  yaml.safe_load(f)
        sites = [site for site in config['sites'] if site['enabled'] == True]
        for i in sites:
            pprint(i)
            module_path, class_name = i['spider_class'].rsplit('.', 1)
            print(module_path, class_name)
            module = importlib.import_module(module_path)
            spider_class = getattr(module, class_name)
            print(spider_class)
            spider_instance = spider_class.run(i['url'], i['flag'])




