import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def dynamic_download():
    # 1. 这里的设置是关键，专门针对 Codespaces 这种云端环境
    chrome_options = Options()
    chrome_options.add_argument("--headless")        # 无头模式（必选）
    chrome_options.add_argument("--no-sandbox")       # 绕过沙盒（必选）
    chrome_options.add_argument("--disable-dev-shm-usage") # 解决内存不足（必选）
    
    # 自动下载匹配的驱动并启动
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 2. 目标网址（这里以一个图片很多的示例站为例）
    target_url = "https://pypi.org/" # 这是一个示例，你可以换成任何动态加载的站
    driver.get(target_url)
    
    # 3. 核心：模拟人手向下滚动 3 次，每次停 2 秒等图片出来
    print("正在模拟滚动加载更多图片...")
    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
    
    # 4. 提取图片链接
    img_tags = driver.find_elements(By.TAG_NAME, "img")
    print(f"动态加载后，共发现 {len(img_tags)} 张图片")
    
    # 创建文件夹
    if not os.path.exists("dynamic_images"):
        os.makedirs("dynamic_images")

    # 5. 循环下载
    for i, img in enumerate(img_tags[:10]): # 先试着下 10 张
        try:
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                res = requests.get(src, timeout=10)
                with open(f"dynamic_images/dynamic_{i}.png", "wb") as f:
                    f.write(res.content)
                print(f"成功抓取动态图片: {i}")
        except Exception as e:
            print(f"下载失败一张: {e}")

    driver.quit()
    print("任务完成！")

if __name__ == "__main__":
    dynamic_download()