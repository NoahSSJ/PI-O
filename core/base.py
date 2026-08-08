from abc import ABC, abstractmethod
import logging
import os
import sqlite3
from pathlib import Path
import redis
from dotenv import load_dotenv

# 在模块顶部加载环境变量
load_dotenv()


class BaseSpider(ABC):
    """爬虫基类，提供通用的初始化和资源管理"""
    
    def __init__(self):
        super().__init__()
        
        # 1. 从环境变量读取配置
        self.save_dir = os.getenv('DOWNLOAD_DIR', './downloads')  # 提供默认值
        # print(self.save_dir)
        self.p = Path(self.save_dir)
        self.p.mkdir(parents=True, exist_ok=True)

        self.auth_dir = os.getenv('AUTH_DIR', "./auth")
        self.auth = Path(self.auth_dir)
        self.auth.mkdir(parents=True, exist_ok=True)
        
        # 2. Redis 连接（从环境变量读取）
        try:
            self.r = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                password=os.getenv('REDIS_PASSWORD', 1234),
                decode_responses=True  # 自动解码返回的字节串
            )
            # 测试连接
            self.r.ping()
        except redis.ConnectionError as e:
            logging.error(f"Redis 连接失败: {e}")
            self.r = None  # 或 raise 中断程序
        
        # 3. 配置日志
        log_level = logging.DEBUG if os.getenv('DEBUG_MODE', 'false').lower() == 'true' else logging.WARNING
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # 4. SQLite 数据库连接（使用 Path 拼接）
        db_dir = Path("database")
        db_dir.mkdir(parents=True, exist_ok=True)
        db_path = db_dir / "example.db"
        
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_database()  # 可选的建表方法
    
    # @abstractmethod
    # def start(self):
    #     """启动爬虫（子类必须实现）"""
    #     pass
    
    # @abstractmethod
    # def parse(self, response):
    #     """解析响应（子类必须实现）"""
    #     pass
    
    def _init_database(self):
        """初始化数据库表（子类可重写）"""
        # 示例：
        # self.cursor.execute('''
        #     CREATE TABLE IF NOT EXISTS items (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         url TEXT UNIQUE,
        #         content TEXT
        #     )
        # ''')
        # self.conn.commit()
        pass
    
    def close(self):
        """释放资源"""
        if hasattr(self, 'conn'):
            self.conn.close()
        if hasattr(self, 'r') and self.r:
            self.r.close()
        self.logger.info("资源已释放")
    
    # def __del__(self):
    #     """析构时自动清理资源（但不保证一定会调用）"""
    #     try:
    #         self.close()
    #     except:
    #         pass