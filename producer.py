"""
独立生产者入口 — 通过命令行参数指定配置文件和用户索引

用法：
    python producer.py <config_file> <user_index>

示例：
    python producer.py spider_demo.yaml 0   # 运行第 1 个用户（任务1）
    python producer.py spider_demo.yaml 1   # 运行第 2 个用户（任务2）
    python producer.py spider.yaml          # 运行全部用户
"""
import sys
import time
from pathlib import Path
from config.loader import ConfigLoader


def main():
    config_file = sys.argv[1] if len(sys.argv) >= 2 else "spider.yaml"
    user_index = int(sys.argv[2]) if len(sys.argv) >= 3 else None

    print(f"🚀 生产者启动 — 配置: {config_file}, 用户索引: {user_index if user_index is not None else '全部'}")
    loader = ConfigLoader()
    loader.load_config(config_file=config_file, user_index=user_index)
    print("✅ 生产者运行完成")

    # 保持容器运行（生产者一般需要持续运行/循环）
    print("⏳ 生产者保持运行中...")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n👋 生产者已退出")


if __name__ == "__main__":
    main()
