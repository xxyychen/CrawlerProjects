# -*- coding = utf-8 -*-
# @Time : 2025/4/30 14:46
# @Author : 鬼鬼
# @File : extract.py
# @Software: PyCharm


from bs4 import BeautifulSoup


def main():
    file_path = "A.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # 提取岗位描述 div
    desc_div_t = soup.find('div', class_='job-sec-text')

    def a(desc_div):
        if desc_div:
            # 使用换行符替换 <br> 标签，然后获取纯文本
            for br in desc_div.find_all('br'):
                br.replace_with('\n')
            text = desc_div.get_text(strip=True, separator='\n')
            return text
        else:
            return "未找到岗位描述信息"

    job_text = a(desc_div_t)
    aa = job_text.index("职位要求")

    print()
    print(job_text)
    print()
    if job_text[aa:aa+5] != "职位要求：":
        job_text = job_text.replace("职位要求", "职位要求：")

    #print(job_text[aa:aa+5])
    print(job_text)


if __name__ == "__main__":
    main()
