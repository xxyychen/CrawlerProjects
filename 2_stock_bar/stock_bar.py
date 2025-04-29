# -*- coding = utf-8 -*-
# @Time : 2024/12/13 21:09


import requests
import json
from openpyxl import Workbook
from utils import format_title, format_number, extract_item_data


def get_cfgs():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://gubatopic.eastmoney.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    return headers


def send_request_post(headers, data):
    response = requests.post(
        'https://gubatopic.eastmoney.com/interface/GetData.aspx?path=newtopic/api/Topic/HomePageListRead',
        headers=headers, data=data,
    )
    res_content = response.content.decode('utf-8')
    return res_content


def main():

    # 上证股吧网站 https://gubatopic.eastmoney.com/index.html
    headers = get_cfgs()
    data = {
        'param': 'ps=50&p=1&type=0&htid=0&code=&sort=0',
        'path': 'newtopic/api/Topic/HomePageListRead',
        'env': '2',
    }

    res_content = send_request_post(headers, data)
    content = json.loads(res_content)["re"]


    wb = Workbook()
    ws = wb.active
    #ws.title = "数据"
    ws.append(["标题", "内容简介", "讨论数", "浏览量", "链接"])

    for ind, each in enumerate(content, 1):

        title, each_url, each_content, discuss_num, browse_num = extract_item_data(ind, each)
        ws.append([
                format_title(title),
                each_content,
                discuss_num,
                format_number(browse_num),
                each_url
            ])

    # 保存到 Excel 文件
    output_file = "output.xlsx"
    wb.save(output_file)




if __name__ == "__main__":
    main()
