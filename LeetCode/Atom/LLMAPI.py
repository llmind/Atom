from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import threading
import time

app = FastAPI(title="通义千问 Playwright API")

# 全局浏览器单例（避免重复启动）
class QwenBrowser:
    def __init__(self):
        self.browser = None
        self.page = None
        self.lock = threading.Lock()
        self.init_browser()

    def init_browser(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(
                headless=True,  # 无头模式
                args=["--no-sandbox"]
            )
            # 加载你导出的 Cookie（提前登录后导出）
            context = self.browser.new_context(storage_state="qwen_cookie.json")
            self.page = context.new_page()
            self.page.goto("https://qianwen.com/chat")
            time.sleep(3)

    def chat(self, prompt: str) -> str:
        with self.lock:
            try:
                # 清空输入框
                self.page.locator(".editor-content").clear()
                # 输入问题
                self.page.locator(".editor-content").fill(prompt)
                # 点击发送
                self.page.locator(".send-btn").click()
                # 等待回复（流式）
                self.page.wait_for_selector(".message-item.assistant .content", timeout=60000)
                # 提取结果
                text = self.page.locator(".message-item.assistant:last-child .content").text_content()
                return text.strip()
            except Exception as e:
                return f"错误：{str(e)}"

qwen = QwenBrowser()

@app.post("/chat")
def api_chat(prompt: str):
    result = qwen.chat(prompt)
    print(f"通义千问回复: {result}")
    return {"prompt": prompt, "response": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8311)
    api_chat("你好千问，告诉我一些你的功能和特点。")