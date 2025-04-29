# -*- coding = utf-8 -*-
# @Time : 2024/12/14 17:00
# @Author : 鬼鬼
# @File : start.py
# @Software: PyCharm


import requests
from utils.utils import get_cfgs, flag_file_exist
from utils.crawl_utils import MyMethod, extract_data


def send_request(url, headers):
    response = requests.get(url, headers=headers)
    return response



def main():

    # 博客园 Blog_Garden
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    cfgs_path = "cfgs.yaml"
    config = get_cfgs(cfgs_path)
    method = MyMethod()

    #
    spider_url = 'https://www.cnblogs.com/'
    html_path, pages = config["crawler"]["html_path"], config["crawler"]["pages"]


    url = spider_url
    for page in range(1, pages+1, 1):
        if page != 1:
            url = spider_url + f"#p{page}"
        print(url)
        html_file_path = html_path.replace('***page***', f"_{page}")

        flag_html_file = flag_file_exist(html_file_path)
        if flag_html_file:
            html_content = method.get_html_file_content(html_file_path)
        else:
            response = send_request(url, headers)
            method.save_html_content(response, html_file_path)
            html_content = response.content.decode('utf-8')

        extract_data(html_content)



if __name__ == "__main__":
    main()
