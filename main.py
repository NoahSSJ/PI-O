import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import loader

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('spider.yaml'):
            print("🔄 配置变化，开始爬取...")
            try:
                main = loader.ConfigLoader()
                main.load_config()
                print("✅ 爬取完成")
            except Exception as e:
                print(f"❌ 爬取失败: {e}")

# 首次运行
print("🚀 首次启动...")
main = loader.ConfigLoader()
main.load_config()
print("✅ 完成")

# 启动监控
observer = Observer()
observer.schedule(Handler(), path='config/', recursive=False)
observer.start()
print("👀 监控中...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("\n👋 已退出")
observer.join()