# 保存Cookie脚本
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://qianwen.com/")
    input("登录后回车...")
    # 保存Cookie
    page.context.storage_state(path="qwen_cookie.json")
    browser.close()