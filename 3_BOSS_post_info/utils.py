# -*- coding = utf-8 -*-
# @Time : 2025/4/30 14:26
# @Author : 鬼鬼
# @File : utils.py
# @Software: PyCharm

import pandas as pd
import re


def get_base_data(excel_path):
    df = pd.read_excel(excel_path)
    urls_tuple = []
    for index, (_, row) in enumerate(df.iterrows(), start=1):

        print(f"第{index}条岗位信息：", row["detail_url"])
        page, num = row["页码/序号"].split("/")

        urls_tuple.append((row["detail_url"], (int(page) - 1) * 15 + int(num)))

    return urls_tuple, df


def sanitize_filename(title):
    # 替换文件名中不能出现的字符
    return re.sub(r'[\\/*?:"<>|]', "_", title).replace("-BOSS直聘", "")


def process_html_info(urls_tuple, driver, i):

    url = driver.current_url
    num_t = None
    for u, n in urls_tuple:
        if u == url:
            num_t = n
            break

    title = driver.title or f"page_{i + 1}"
    clean_title = sanitize_filename(title)

    return num_t, clean_title


def main():
    pass


if __name__ == "__main__":
    main()
