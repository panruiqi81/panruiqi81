import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, folder_name="downloaded_images"):
    # 1. 创建保存图片的文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"创建文件夹: {folder_name}")

    # 2. 模拟浏览器，防止被网站屏蔽 (User-Agent)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 3. 发送请求获取网页内容
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 如果请求失败会报错
        
        # 4. 解析网页，寻找所有 <img> 标签
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        print(f"发现 {len(img_tags)} 张潜在图片")

        # 5. 循环下载
        for i, img in enumerate(img_tags):
            img_url = img.get('src')
            if not img_url:
                continue
            
            # 处理相对路径，转换为绝对路径
            img_url = urljoin(url, img_url)
            
            try:
                img_data = requests.get(img_url, headers=headers).content
                # 提取文件名或用数字命名
                filename = f"image_{i+1}.jpg"
                with open(os.path.join(folder_name, filename), 'wb') as f:
                    f.write(img_data)
                print(f"已下载: {filename}")
            except Exception as e:
                print(f"下载失败 {img_url}: {e}")

    except Exception as e:
        print(f"错误: {e}")

# --- 测试运行 ---
if __name__ == "__main__":
    target_url = "https://www.baidu.com" # 你可以换成任何你想抓图片的网站
    download_images(target_url)