# -*- coding = utf-8 -*-
# @Time : 2024/12/15 0:17
# @Author : 鬼鬼
# @File : crawl_utils.py
# @Software: PyCharm

import os
from lxml import etree


class MyMethod:

    @staticmethod
    def save_html_content(res, html_file_path):

        html_content = res.content.decode('utf-8')
        if not os.path.exists(html_file_path):
            with open(html_file_path, "w", encoding='utf-8') as file:
                file.write(html_content)
        return html_file_path

    @staticmethod
    def get_html_file_content(html_file_path):

        if os.path.exists(html_file_path):
            with open(html_file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            return html_content

        return ""

    @staticmethod
    def get_etree_content(one_etree):

        etree_content = etree.tostring(one_etree, encoding='unicode', method="html")
        return etree_content


def item_content_process(content):

    a_tag = content.xpath('.//a[@target="_blank"]')
    if a_tag:
        a_tag = a_tag[0]
        # 将 <a> 的尾部文本（tail）合并到父节点中
        if a_tag.tail:
            parent = a_tag.getparent()
            parent.text = (parent.text or '') + a_tag.tail
        a_tag.getparent().remove(a_tag)

    content = content.xpath('.//text()')[0].strip()
    return content


def extract_data(html_content):

    html_etree = etree.HTML(html_content)

    items_list = html_etree.xpath('//*[@class="post-item"]')

    for ind, item in enumerate(items_list, 1):

        title = item.xpath('.//*[@class="post-item-title"]/text()')[0]
        #print(title)
        content = item.xpath('.//p[@class="post-item-summary"]')[0]
        content = item_content_process(content)

        user_name = item.xpath('.//span/text()')[0]
        date = item.xpath('.//span[@class="post-meta-item"]/span/text()')[0]
        print(ind, title, user_name, date)
        #print()
        #print(content)




def main():
    pass


if __name__ == "__main__":
    main()
