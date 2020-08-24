import re
import sys
import jieba
import jieba.analyse as anal
import pymssql

# 获取停词表
def get_stopword_list():
    # 停用词表存储路径，每一行为一个词，按行读取进行加载
    # 进行编码转换确保匹配准确率
    # stop_word_path = 'C:/Users/ZYS05/PycharmProjects/pythonProject/stopwords.txt'
    stop_word_path = 'C:/Users/ZYS05/Desktop/IOT/stopwords.txt'
    stopword_list = [sw.replace('\n', '') for sw in open(stop_word_path,encoding='utf-8').readlines()]
    return stopword_list


def keyExtractor(filename, k=20, thresh=0.2):
    f = open(filename, encoding='utf-8')
    docs = f.read()
    # 分词
    seg_list = jieba.cut(docs, cut_all=False)
    stopwords = get_stopword_list()
    word_list = []
    for word in seg_list:
        if word != " " and word != "\n":
            # 剔除单字
            if len(word) > 1:
                # 剔除停词
                if word not in stopwords:
                    word_list.append(word)
    # 重新组合成句
    sentence = "".join(word_list)
    # 调用TextRank算法提取关键字
    keywords_map = anal.textrank(sentence, topK=k, withWeight=True, allowPOS=('n', 'nr', 'ns'))
    keywords_list = []
    # 显示关键字及对应权重
    for item in keywords_map:
        # 分别为关键词和相应的权重
        if item[1] >= thresh:
            keywords_list.append(item[0])

    return keywords_list

# def output(keywords):
#     file = open("C:/Users/ZYS05/PycharmProjects/pythonProject/keywords.txt", "w")
#     for line in keywords:
#         file.write(line + '\n')
#     file.close()
#     return "success"

def DBupdate(keywords, id):
    try:
        conn = pymssql.connect(
            host="localhost",
            user="sa",
            password="123456",
            database="NBA",
            port="63312")

        # if conn:
        #     print("连接成功!")
        # 获取连接下的游标
        cursor_test = conn.cursor()

        sql = "SELECT t_knowledgepage.PageContent  FROM  t_knowledgepage  WHERE  t_knowledgepage.KnowledgePageID=" + str(
            id)

        # 执行 sql 语句
        cursor_test.execute(sql)
        # 显示出所有数据
        content = ""
        for word in keywords:
            content += word + ","
        updatestr = "UPDATE t_knowledgepage set PageContent='{0}' WHERE  t_knowledgepage.KnowledgePageID={1}".format(
            content.replace('\n', '').replace('\r', '').replace(',', ' '), str(id));
        cursor_test.execute(updatestr)
        conn.commit()
        conn.close()
        print(0)
        return content
    except  Exception:
        # print("发生异常", Exception)
        print(1)
        conn.rollback()
        conn.close()


if __name__ == '__main__':
    try:
        keywords = keyExtractor('C:/Users/ZYS05/Desktop/IOT/document.txt')
        pageID = int(sys.argv[1])
        DBupdate(keywords,pageID)
        #print(output(keywords))
    except Exception as e:
        print(2)
