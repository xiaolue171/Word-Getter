import re
import nltk
import random
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('wordnet')

def extract_words(novel_file):
    """从文件中提取单词 """
    words = []
    with open(novel_file, 'r', encoding='utf-8') as novel:
        for line in novel:
            tokens = word_tokenize(line)
            for token in tokens:
                if is_valid_word(token):
                    words.append(token)
    return words

def is_valid_word(word):
    """使用正则表达式检查单词是否仅由字母或连字符构成"""
    pattern = r'^[a-zA-Z-]+$'
    return bool(re.match(pattern, word))

def get_novel_words(novel_file):
    """将文本转化为基础单词表"""
    words = extract_words(novel_file) # 提取文本中的单词

    # 词干化单词
    stemmer = PorterStemmer()
    for word in words:
        word = stemmer.stem(word)

    # 检查是否在WordNet中
    for word in words:
        if not is_in_wordnet(word):
            words.remove(word)

    return list(set(words))

def is_in_wordnet(word):
    """检查单词是否在WordNet中"""
    return wordnet.synsets(word) != []

def write_words_to_file(words, output_file):
    """将单词列表写入文件"""
    with open(output_file, 'w', encoding='utf-8') as output:
        for word in words:
            output.write(f"{word.lower()}\n")

"""可选功能"""

def delete_short(words):
    """过滤掉长度小于等于2的单词"""
    for word in words:
        if len(word) <= 2:
            words.remove(word)

def filter_words(words, filter_file):
    """过滤掉在 words 中与 filter_file 重复的单词"""
    with open(filter_file, 'r', encoding='utf-8') as file:
        filter_words = set(file.read().splitlines())
    words = words - filter_words

def shuffle_words(words):
    random.shuffle(words)

if __name__ == "__main__":
    print("欢迎使用本程序！github仓库https://github.com/xiaolue171/Word-Getter")
    # 读取 info.txt 文件中的内容
    info_file = "info.txt"
    english_text_file = ""
    word_list_file = ""
    filter_file = ""

    with open(info_file, 'r', encoding='utf-8') as info:
        for line in info:
            line = line.strip()
            if line.startswith("English text:"):
                english_text_file = line.split(":", 1)[1].strip()
            elif line.startswith("Word list text:"):
                word_list_file = line.split(":", 1)[1].strip()
            elif line.startswith("Filter text:"):
                filter_file = line.split(":", 1)[1].strip()

    want_shuffle_words = input("是否需要打乱单词顺序？(y/n): ")
    want_delete_short = input("是否需要删除长度小于等于2的单词？(y/n): ")
    if not filter_file.strip():
        want_filter_words = 'n'
    else:
        want_filter_words = input("是否需要过滤掉指定的单词？(y/n): ")

    print("正在处理...")
    words = get_novel_words(english_text_file)
    print("本文档共含有"+str(len(words))+"个单词")

    if want_shuffle_words.lower() == 'y':
        shuffle_words(words)
    if want_delete_short.lower() == 'y':
        delete_short(words)
    if want_filter_words.lower() == 'y':
        filter_words(words, filter_file)
    
    write_words_to_file(words, word_list_file)
    print("生成单词表共含有"+str(len(words))+"个单词")
    print(f"已保存单词列表到 {word_list_file} 文件中")
    input("按 Enter 键退出...")