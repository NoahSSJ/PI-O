import json
import os
from playwright.sync_api import sync_playwright

COOKIE_FILE = "xiaohongshu_cookies.json"
LOGIN_URL = "https://www.xiaohongshu.com/"

def save_cookies(context, path=COOKIE_FILE):
    cookies = context.cookies()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    print(f"✅ Cookie 已保存到 {path}")

def load_cookies(context, path=COOKIE_FILE):
    if not os.path.exists(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        context.add_cookies(cookies)
        print("✅ 已加载本地 Cookie")
        return True
    except Exception as e:
        print("❌ Cookie 加载失败", e)
        return False

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport=None
        )

        page = context.new_page()

        # 先加载 Cookie
        if load_cookies(context):
            page.goto(LOGIN_URL)
            print("🎉 已使用 Cookie 登录，直接进入小红书")
            page.wait_for_timeout(5000)  # 看一下效果
            # 这里写你后续业务逻辑
            return

        # 无 Cookie → 扫码登录
        print("🔑 请扫码登录，10秒后自动保存Cookie")
        page.goto(LOGIN_URL)
        page.wait_for_timeout(10000)  # 等10秒

        # 保存Cookie
        save_cookies(context)
        print("✅ Cookie保存完成，下次可直接登录")

        # 停留一会儿再关
        page.wait_for_timeout(3000)
        browser.close()

if __name__ == "__main__":
    run()
