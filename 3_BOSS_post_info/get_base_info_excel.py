# -*- coding = utf-8 -*-
# @Time : 2025/4/30 11:05
# @Author : 鬼鬼
# @File : get_base_info_excel.py
# @Software: PyCharm

import json
import pandas as pd
import os
from openpyxl import load_workbook
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = ['Microsoft YaHei']


def get_cfgs():
    page_num = 7
    # post = "python开发"
    # # # 假设你不想要这些词出现在词云中
    # stop_skill_keywords = {'python', 'flask', 'django', 'mysql'}

    # post = "测试开发"
    # stop_skill_keywords = {'计算机相关专业', '通信相关专业',
    #                        '自动化测试', '自动化测试经验',
    #                        'java', 'python', 'mysql'}

    # post = "产品经理"
    # stop_skill_keywords = {'B端产品', 'C端产品',
    #                        'java', 'python', 'mysql'}

    # #####################################################################
    # post = "爬虫"
    # stop_skill_keywords = {'爬虫', '采集', '爬虫经验', '爬虫工程师',
    #                        '数据抓取', '网络爬虫技术', '数据抓取', 'spring',
    #                        'scrapy', 'go', '数据抓取', 'spring',
    #                        'java', 'python', 'mysql'}

    # post = "AI"
    # stop_skill_keywords = {'深度学习', '人工智能', '机器学习', '爬虫工程师',
    #                        'java', 'python', 'mysql'}

    # post = "数据开发"
    # stop_skill_keywords = {'数据平台开发经验', '数据仓库开发经验',
    #                        '要求数据开发经验',
    #                        'java', 'python', 'mysql'}

    # post = "自动驾驶"
    # stop_skill_keywords = {'深度学习', '自动驾驶', '机器学习', #'爬虫工程师',
    #                        'java', 'python', 'mysql'}

    post = "AI应用开发"
    stop_skill_keywords = {'ai', 'spring',  'c', 'pytorch',
                           '接受实习', '在校生投递', 'golang', '爬虫经验',
                           'java', 'python', 'mysql'}


    data_p = f"./data/{post}"

    excel_path = f"{data_p}/{post}_jobs_base_info.xlsx"
    word_cloud_path = f"{data_p}/{post}_技能词云图.png"
    return page_num, post, stop_skill_keywords, data_p, excel_path, word_cloud_path


def read_json(data_path):
    # 打开并读取 JSON 文件
    with open(data_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    return json_data


def extract_data(item, page, ind):

    uu = f'https://www.zhipin.com/job_detail/{item["encryptJobId"]}.html'
    res_dict = {
        '岗位名称': item["jobName"],
        '薪资待遇': item["salaryDesc"],
        '经验要求': item["jobLabels"],  # item["jobDegree"] + item["jobExperience"]
        '公司名称/类型': item["brandName"] + "/" + item["brandIndustry"],
        '公司规模': item["brandScaleName"] + "-" + item["brandStageName"],
        '公司地点': item["cityName"] + "-" + item["areaDistrict"],
        '技能标签': item["skills"],
        'HR信息': item["bossName"] + "-" + item["bossTitle"],
        '页码/序号': str(page) + "/" + str(ind),
        'detail_url': uu,
        '相关福利': item["welfareList"],
        # '岗位名称': item["jobName"],
    }
    return res_dict


def optimize_excel(excel_path):
    # 调整列宽
    wb = load_workbook(excel_path)
    ws = wb.active

    # 设置列宽：第1、3、6列宽一些，最小宽度为 15
    wider_cols = [1, 3, 5]  # Excel 列是从 1 开始计数
    min_width = 12
    for col in ws.columns:
        col_index = col[0].column  # 获取列号
        max_len = max((len(str(cell.value)) for cell in col if cell.value), default=0)
        adjusted_width = max(min_width, max_len + 2)
        if col_index in wider_cols:
            adjusted_width += 13  # 宽一点
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = adjusted_width

    wb.save(excel_path)
    #print("列宽设置完成！")


def get_word_cloud_pic(jobs_base_info, stopwords, word_cloud_path):

    all_skills = []
    for item in jobs_base_info:
        skills = item.get('技能标签', [])
        if isinstance(skills, list):
            all_skills.extend(skills)

    # 统一转小写并 strip 掉空格后再过滤
    all_skills = [
        word for word in all_skills
        if word.strip().lower() not in stopwords
    ]

    # 2. 拼接成一个字符串（用空格分隔）
    text = ' '.join(all_skills)
    # 3. 创建词云
    wc = WordCloud(
        font_path='msyh.ttc',  # 中文字体路径，Windows 下一般是微软雅黑
        width=800,
        height=600,
        background_color='white'
    ).generate(text)

    # 保存词云图
    wc.to_file(word_cloud_path)

    # 4. 显示词云
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('技能标签词云图')
    plt.show()


def main():
    ########################################################
    # 1.
    # 打开boss直聘，搜索python开发
    # 即url = https://www.zhipin.com/web/geek/jobs?query=python%E5%BC%80%E5%8F%91&city=101010100
    # 得到接口数据：https://www.zhipin.com/wapi/zpgeek/search/joblist.json?page=1&pageSize=15&city=101010100&query=python%E5%BC%80%E5%8F%91&expectInfo=&multiSubway=&multiBusinessDistrict=&position=&jobType=&salary=&experience=&degree=&industry=&scale=&stage=&scene=1&_=1745982476107
    # 手动保存为 jobs_1.json
    ########################################################
    # 2.得到 jobs_base_info.xlsx

    # get_cfgs()
    page_num, post, stop_skill_keywords, data_p, excel_path, word_cloud_path = get_cfgs()

    jobs_base_info = []
    for page in range(1, page_num+1):
        data_path = f"{data_p}/jobs_{page}.json"
        json_data = read_json(data_path)

        for ind, item in enumerate(json_data["zpData"]["jobList"], 1):
            res_dict = extract_data(item, page, ind)
            print(page, ind)
            jobs_base_info.append(res_dict)

    # 去重 #####################
    seen_urls = set()
    unique_dicts = []
    for d in jobs_base_info:
        url = d.get('detail_url')
        if url not in seen_urls:
            seen_urls.add(url)
            unique_dicts.append(d)

    jobs_base_info = unique_dicts
    print(f"获得{len(jobs_base_info)}条招聘信息(已去重)！")

    # 工作岗位的基本信息 xlsx #################################
    if not os.path.exists(excel_path):
        df = pd.DataFrame(jobs_base_info)
        df.to_excel(excel_path, index=False)

    optimize_excel(excel_path)  # 优化excel
    print("工作岗位的基本信息 保存成功！")

    # 3. 得到 词云图 #########################################
    get_word_cloud_pic(jobs_base_info, stop_skill_keywords, word_cloud_path)
    print("技能标签 词云图 保存成功！")


if __name__ == "__main__":
    main()
