import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.font_manager as fm
import numpy as np
import seaborn as sns

# 页面标题
st.title("文本分析与词云生成")

# 停用词加载
def load_stopwords(file):
    stopwords = set()
    for line in file:
        stopwords.add(line.strip())
    return stopwords

# 输入框，用户输入文章URL
url = st.text_input("请输入文章的URL:")

# 停用词文件上传
stopwords_file = st.file_uploader("上传停用词文件 (可选):", type=['txt'])

if url:
    # 请求URL抓取文本内容
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        response.encoding = response.apparent_encoding  # 设置正确的编码
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取文本内容
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        text = ' '.join(paragraphs)

        # 显示提取的文本内容供选择
        st.subheader("提取的文本内容:")
        selected_paragraphs = st.multiselect("选择要显示的段落:", paragraphs)

        if selected_paragraphs:
            st.write("你选择的段落:")
            for paragraph in selected_paragraphs:
                st.write(paragraph)

        # 加载停用词
        stopwords = set()
        if stopwords_file is not None:
            stopwords = load_stopwords(stopwords_file)

        # 对文本分词
        words = jieba.cut(text)
        word_list = [word for word in words if len(word) > 1 and word not in stopwords]  # 过滤掉单个字符和停用词
        word_counts = Counter(word_list)

        # 统计词频并展示前20个词汇
        most_common_words = word_counts.most_common(20)
        st.write("词频排名前20的词汇:")
        st.write(most_common_words)

        # 设置字体
        font_path = 'SimHei.ttf'
        my_font = fm.FontProperties(fname=font_path)

        # 词云绘制
        wordcloud = WordCloud(font_path=font_path, width=800, height=400).generate_from_frequencies(word_counts)

        # 图形筛选
        chart_type = st.sidebar.selectbox("选择图形类型:", ["词云", "柱状图", "饼图", "折线图", "散点图", "热力图", "面积图"])

        # 根据选择的图形类型绘制
        if chart_type == "词云":
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
        elif chart_type == "柱状图":
            plt.bar(*zip(*most_common_words))
            plt.xticks(rotation=45, fontproperties=my_font)
            plt.ylabel('频率', fontproperties=my_font)
            plt.title('高频词柱状图', fontproperties=my_font)
            st.pyplot(plt)
        elif chart_type == "饼图":
            counts = [count for word, count in most_common_words]
            labels = [word for word, count in most_common_words]
            plt.pie(counts, labels=labels, autopct='%1.1f%%')
            for label in plt.gca().texts:
                label.set_fontproperties(my_font)
            st.pyplot(plt)
        elif chart_type == "折线图":
            words, counts = zip(*most_common_words)
            plt.plot(words, counts)
            plt.xticks(rotation=45, fontproperties=my_font)
            st.pyplot(plt)
        elif chart_type == "散点图":
            words, counts = zip(*most_common_words)
            plt.scatter(words, counts)
            plt.xticks(rotation=45, fontproperties=my_font)
            st.pyplot(plt)
        elif chart_type == "面积图":
            words, counts = zip(*most_common_words)
            plt.fill_between(words, counts)
            plt.xticks(rotation=45, fontproperties=my_font)
            st.pyplot(plt)
        elif chart_type == "热力图":
            heatmap_data = np.array([[count for _, count in most_common_words]])
            plt.figure(figsize=(10, 5))
            sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu', xticklabels=[word for word, _ in most_common_words], yticklabels=['频率'])
            plt.title('词频热力图', fontproperties=my_font)
            plt.xticks(rotation=45, fontproperties=my_font)
            st.pyplot(plt)

    except requests.exceptions.RequestException as e:
        st.error(f"网络请求错误: {e}")
    except Exception as e:
        st.error(f"抓取内容时出错: {e}")





# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# from collections import Counter
# import jieba
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import matplotlib.font_manager as fm
# import numpy as np
# import seaborn as sns
#
# # 页面标题
# st.title("文本分析与词云生成")
#
# # 输入框，用户输入文章URL
# url = st.text_input("请输入文章的URL:")
#
# if url:
#     # 请求URL抓取文本内容
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # 检查请求是否成功
#         response.encoding = response.apparent_encoding  # 设置正确的编码
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # 提取文本内容
#         paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
#         text = ' '.join(paragraphs)
#
#         # 显示提取的文本内容供选择
#         st.subheader("提取的文本内容:")
#         selected_paragraphs = st.multiselect("选择要显示的段落:", paragraphs)
#
#         if selected_paragraphs:
#             st.write("你选择的段落:")
#             for paragraph in selected_paragraphs:
#                 st.write(paragraph)
#
#         # 对文本分词
#         words = jieba.cut(text)
#         word_list = [word for word in words if len(word) > 1]  # 过滤掉单个字符
#         word_counts = Counter(word_list)
#
#         # 统计词频并展示前20个词汇
#         most_common_words = word_counts.most_common(20)
#         st.write("词频排名前20的词汇:")
#         st.write(most_common_words)
#
#         # 设置字体
#         font_path = 'SimHei.ttf'
#         my_font = fm.FontProperties(fname=font_path)
#
#         # 词云绘制
#         wordcloud = WordCloud(font_path=font_path, width=800, height=400).generate_from_frequencies(word_counts)
#
#         # 图形筛选
#         chart_type = st.sidebar.selectbox("选择图形类型:", ["词云", "柱状图", "饼图", "折线图", "散点图", "热力图", "面积图"])
#
#         # 根据选择的图形类型绘制
#         if chart_type == "词云":
#             plt.imshow(wordcloud, interpolation='bilinear')
#             plt.axis('off')
#             st.pyplot(plt)
#         elif chart_type == "柱状图":
#             plt.bar(*zip(*most_common_words))
#             plt.xticks(rotation=45, fontproperties=my_font)
#             plt.ylabel('频率', fontproperties=my_font)
#             plt.title('高频词柱状图', fontproperties=my_font)
#             st.pyplot(plt)
#         elif chart_type == "饼图":
#             counts = [count for word, count in most_common_words]
#             labels = [word for word, count in most_common_words]
#             plt.pie(counts, labels=labels, autopct='%1.1f%%')
#             for label in plt.gca().texts:
#                 label.set_fontproperties(my_font)
#             st.pyplot(plt)
#         elif chart_type == "折线图":
#             words, counts = zip(*most_common_words)
#             plt.plot(words, counts)
#             plt.xticks(rotation=45, fontproperties=my_font)
#             st.pyplot(plt)
#         elif chart_type == "散点图":
#             words, counts = zip(*most_common_words)
#             plt.scatter(words, counts)
#             plt.xticks(rotation=45, fontproperties=my_font)
#             st.pyplot(plt)
#         elif chart_type == "面积图":
#             words, counts = zip(*most_common_words)
#             plt.fill_between(words, counts)
#             plt.xticks(rotation=45, fontproperties=my_font)
#             st.pyplot(plt)
#         elif chart_type == "热力图":
#             heatmap_data = np.array([[count for _, count in most_common_words]])
#             plt.figure(figsize=(10, 5))
#             sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu', xticklabels=[word for word, _ in most_common_words], yticklabels=['频率'])
#             plt.title('词频热力图', fontproperties=my_font)
#             plt.xticks(rotation=45, fontproperties=my_font)
#             st.pyplot(plt)
#
#     except requests.exceptions.RequestException as e:
#         st.error(f"网络请求错误: {e}")
#     except Exception as e:
#         st.error(f"抓取内容时出错: {e}")
#
#













# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
# from collections import Counter
# import jieba
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import matplotlib.font_manager as fm
# import numpy as np
# import seaborn as sns
#
# # 页面标题
# st.title("文本分析与词云生成")
#
# # 输入框，用户输入文章URL
# url = st.text_input("请输入文章的URL:")
#
# if url:
#     # 请求URL抓取文本内容
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # 检查请求是否成功
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # 提取文本内容
#         paragraphs = [p.get_text() for p in soup.find_all('p')]
#         text = ' '.join(paragraphs)
#
#         # 显示提取的文本内容供选择
#         st.subheader("提取的文本内容:")
#         selected_paragraphs = st.multiselect("选择要显示的段落:", paragraphs)
#
#         if selected_paragraphs:
#             st.write("你选择的段落:")
#             for paragraph in selected_paragraphs:
#                 st.write(paragraph)
#
#         # 对文本分词
#         words = jieba.cut(text)
#         word_list = [word for word in words if len(word) > 1]  # 过滤掉单个字符
#         word_counts = Counter(word_list)
#
#         # 统计词频并展示前20个词汇
#         most_common_words = word_counts.most_common(20)
#         st.write("词频排名前20的词汇:")
#         st.write(most_common_words)
#
#         # 设置字体
#
#         font_path = 'SimHei.ttf'
#
#
#         # font_path = 'D:\\HuaweiMoveData\\Users\\MZY\\Desktop\\爬虫\\SimHei.ttf'  # 请确保路径正确
#
#
#
#         my_font = fm.FontProperties(fname=font_path)
#
#         # 词云绘制
#         wordcloud = WordCloud(font_path=font_path, width=800, height=400).generate_from_frequencies(word_counts)
#
#         # 图形筛选
#         chart_type = st.sidebar.selectbox("选择图形类型:", ["词云", "柱状图", "饼图", "折线图", "散点图", "热力图", "面积图"])
#
#         # 根据选择的图形类型绘制
#         if chart_type == "词云":
#             plt.imshow(wordcloud, interpolation='bilinear')
#             plt.axis('off')
#             st.pyplot(plt)
#         elif chart_type == "柱状图":
#             plt.bar(*zip(*most_common_words))
#             plt.xticks(rotation=45, fontproperties=my_font)  # 设置x轴标签字体
#             plt.ylabel('频率', fontproperties=my_font)  # 设置y轴标签字体
#             plt.title('高频词柱状图', fontproperties=my_font)  # 设置标题字体
#             st.pyplot(plt)
#         elif chart_type == "饼图":
#             counts = [count for word, count in most_common_words]
#             labels = [word for word, count in most_common_words]
#             plt.pie(counts, labels=labels, autopct='%1.1f%%')
#             for label in plt.gca().texts:
#                 label.set_fontproperties(my_font)
#             st.pyplot(plt)
#         elif chart_type == "折线图":
#             words, counts = zip(*most_common_words)
#             plt.plot(words, counts)
#             plt.xticks(rotation=45, fontproperties=my_font)
#             st.pyplot(plt)
#         elif chart_type == "散点图":
#             words, counts = zip(*most_common_words)
#             plt.scatter(words, counts)
#             plt.xticks(rotation=45, fontproperties=my_font)
#             st.pyplot(plt)
#         elif chart_type == "面积图":
#             words, counts = zip(*most_common_words)
#             plt.fill_between(words, counts)
#             plt.xticks(rotation=45, fontproperties=my_font)
#             st.pyplot(plt)
#         elif chart_type == "热力图":
#             # 准备热力图数据
#             heatmap_data = np.array([[count for _, count in most_common_words]])
#             plt.figure(figsize=(10, 5))
#             sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu', xticklabels=[word for word, _ in most_common_words], yticklabels=['频率'])
#             plt.title('词频热力图', fontproperties=my_font)
#             plt.xticks(rotation=45, fontproperties=my_font)
#             st.pyplot(plt)
#
#     except Exception as e:
#         st.error(f"抓取内容时出错: {e}")
#
#


