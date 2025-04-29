# -*- coding = utf-8 -*-
# @Time : 2025/4/29 23:16
# @Author : 鬼鬼
# @File : utils.py
# @Software: PyCharm

def extract_item_data(ind, each):
    title = each["nickname"]
    each_url = 'https://gubatopic.eastmoney.com/topic_v3.html?htid=' + str(each["htid"])
    each_content = each["desc"]
    discuss_num = each["postNumber"]
    browse_num = each["clickNumber"]

    #print(ind, format_title(title), each_url, each_content, discuss_num, format_number(browse_num))
    print(ind, format_title(title), each_url, discuss_num, format_number(browse_num))
    return title, each_url, each_content, discuss_num, browse_num


def format_number(num):
    if num >= 10000:
        return f"{num / 10000:.2f}万"
    else:
        return str(num)


def format_title(title):
    return "#" + title + "#"


def main():
    pass


if __name__ == "__main__":
    main()
