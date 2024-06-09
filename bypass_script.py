import cloudscraper
from DrissionPage import ChromiumPage, ChromiumOptions
import time

class Bypasser:
    def __init__(self, driver):
        self.driver = driver

    def clickCycle(self):
        if self.driver.wait.ele_displayed('xpath://div/iframe', timeout=1.5):
            iframe = self.driver.ele('xpath://div/iframe')
            if iframe and self.driver.wait.ele_displayed('//*[text()="确认您是真人"]', timeout=2.5):
                iframe.ele('//*[text()="确认您是真人"]', timeout=25).click()
                time.sleep(2)

    def isBypassed(self):
        title = self.driver.title.lower()
        return not(("chatgpt.com" in title) or ("just a moment" in title) or ("请稍候" in title) or ("authz" in title))

    def bypass(self):
        while not self.isBypassed():
            self.clickCycle()

class CustomSession:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.driver = None
        self.bypasser = None

    def get(self, url, **kwargs):
        try:
            response = self.scraper.get(url, **kwargs)
            if self._needs_bypass(response):
                self._initialize_driver(url)
                response = self.scraper.get(url, **kwargs)
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def post(self, url, data=None, json=None, **kwargs):
        try:
            response = self.scraper.post(url, data=data, json=json, **kwargs)
            if self._needs_bypass(response):
                self._initialize_driver(url)
                response = self.scraper.post(url, data=data, json=json, **kwargs)
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def _needs_bypass(self, response):
        if response is None:
            return True
        text = response.text.lower()
        return 'just a moment' in text or '请稍候' in text or response.status_code in [403, 429]

    def _initialize_driver(self, url):
        if not self.driver:
            options = ChromiumOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--headless')  # 运行在无头模式下
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--remote-debugging-port=9222')  # 使用默认端口进行远程调试
            self.driver = ChromiumPage(options)
            self.bypasser = Bypasser(self.driver)
        self.driver.get(url)
        self.bypasser.bypass()

    def quit(self):
        if self.driver:
            self.driver.quit()

def main():
    session = CustomSession()
    url = 'https://chatgpt.com'
    
    # 执行GET请求
    response = session.get(url)
    if response:
        print(response.text)
    else:
        print("Failed to fetch the URL.")

    # 执行POST请求（示例）
    # response = session.post(url, data={"key": "value"})
    # if response:
    #     print(response.text)
    # else:
    #     print("Failed to post to the URL.")

    session.quit()

if __name__ == "__main__":
    main()
