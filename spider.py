import requests #用于发送请求获取网页
from bs4 import BeautifulSoup #用于解析HTML
import pdfkit #用于将HTML转换为PDF
import matplotlib.pyplot as plt #用于绘图

# 定义语言代码和日期范围
language_codes = ["en", "zh",""]
DATE = ["daily", "weekly", "monthly"]

def parse_url_to_html_and_collect_languages(url, language, date_range):

    #使用headers伪装为正常访问
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'}
    # 根据语言和日期范围构建URL
    url = f"{url}?since={date_range}&spoken_language_code={language}"
    print(url)
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find_all(class_="Box")[0]
    html = str(body)
    file_path = r"F:\python_result\a.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 收集编程语言的数量
    language_counts = {}
    programming_languages = soup.find_all('span', itemprop='programmingLanguage')
    for lang in programming_languages:
        language = lang.text.strip()
        if language in language_counts:
            language_counts[language] += 1
        else:
            language_counts[language] = 1
    
    return file_path, language_counts  # 返回文件名和语言计数

def save_pdf(htmls):
    options = {
        "page-size": "Letter",
        'encoding': "UTF-8",
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdfkit.from_file(htmls, 'F:\\python_result\\result.pdf', options=options)

def plot_language_counts(language_counts,date,spoken_language):
    plt.rcParams["font.size"] = 14  # 设置字体大小
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    # 绘制柱状图
    languages = list(language_counts.keys())
    counts = list(language_counts.values())
    
    plt.figure(figsize=(19, 8))
    plt.bar(languages, counts, color='skyblue')
    plt.xlabel('编程语言')
    plt.ylabel('数量')
    plt.title('当前排行榜中编程语言的占比' + "(" + date + " " + spoken_language + ")")
    plt.show()

if __name__ == "__main__":
    print("请输入语言和日期范围：")
    for index, language in enumerate(language_codes):
        if(index == 2):
            print(f"{index}: All languages")
        else:
            print(f"{index}: {language}")
    language_choice = int(input("选择语言（输入数字）："))
    for index, date in enumerate(DATE):
        print(f"{index}: {date}")
    date_choice = int(input("选择日期范围（输入数字）："))

    # 获取用户选择的语言和日期范围
    selected_language = language_codes[language_choice]
    selected_date = DATE[date_choice]

    # 构建URL并解析HTML，同时收集编程语言的数量
    url = 'https://github.com/trending'
    html_file, language_counts = parse_url_to_html_and_collect_languages(url, selected_language, selected_date)
    
    # 将HTML文件转换为PDF
    save_pdf([html_file])

    # 绘制柱状图
    plot_language_counts(language_counts,selected_date,selected_language)