# -*- coding = utf-8 -*-
# @Time : 2025/4/30 14:27
# @Author : 鬼鬼
# @File : start.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

from utils import get_base_data, process_html_info


def open_urls_and_save_html(chrome_driver, url_tuple):

    options = Options()
    # 可选：是否无头模式
    # options.add_argument('--headless')
    service = Service(chrome_driver)
    driver = webdriver.Chrome(service=service, options=options)

    # 打开第一个页面
    first_item = url_tuple[0]
    driver.get(first_item[0])
    time.sleep(2)

    # 依次打开新标签页并访问其他URL
    for tup in url_tuple[1:]:
        url = tup[0]
        driver.execute_script(f"window.open('{url}', '_blank');")
        time.sleep(2)

    print(f"已打开 {len(url_tuple)} 个标签页")
    return driver


def main():
    # !!!先运行 get_base_info_excel.py，得到xxx_jobs_base_info.xlsx
    post = "python开发"
    data_p = f"./data/{post}"
    excel_path = f"{data_p}/{post}_jobs_base_info.xlsx"
    chrome_driver = './chromedriver.exe'
    output_path = f"./output/{post}"

    urls_tuple, df = get_base_data(excel_path)
    start, end = 50, 60
    driver = open_urls_and_save_html(chrome_driver, urls_tuple[start:end])

    handles = driver.window_handles  # 获取所有标签页句柄
    for i, handle in enumerate(handles):
        driver.switch_to.window(handle)
        print(f"第{i+1}个页面标题：{driver.title}")

        num_t, clean_title = process_html_info(urls_tuple, driver, i)
        filename = os.path.join(output_path, f"{num_t}_{clean_title}.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"✅ 第{num_t}个【{clean_title}】已保存为 {filename}")
        time.sleep(3)

    driver.quit()


if __name__ == "__main__":
    main()
