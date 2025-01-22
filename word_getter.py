import re
import nltk
import random
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk import pos_tag

nltk.download('wordnet')

def extract_words(novel_file):
    """从文件中提取单词 """
    words = []
    with open(novel_file, 'r', encoding='utf-8') as novel:
        for line in novel:
            tokens = word_tokenize(line)
            for token in tokens:
                if is_valid_word(token):
                    words.append(token.lower())
    return words

def is_valid_word(word):
    """使用正则表达式检查单词是否仅由字母或连字符构成"""
    pattern = r'^[a-zA-Z-]+$'
    return bool(re.match(pattern, word))

def get_novel_words(novel_file):
    """将文本转化为基础单词表，移除复数形式和动词三单形式"""
    words = extract_words(novel_file)  # 提取文本中的单词

    tagged_words = pos_tag(words)
    lemmatizer = WordNetLemmatizer()
    # 还原单词
    lemmatized_words = []
    for word, tag in tagged_words:
        wn_tag = get_wordnet_pos(tag)
        if wn_tag == wordnet.NOUN:
            # 将名词的复数形式还原为单数
            lemmatized_word = lemmatizer.lemmatize(word, wordnet.NOUN)
        elif wn_tag == wordnet.VERB:
            # 将动词的第三人称单数形式还原为基本形式
            lemmatized_word = lemmatizer.lemmatize(word, wordnet.VERB)
        else:
            # 对其他情况进行默认处理
            lemmatized_word = lemmatizer.lemmatize(word)
        
        lemmatized_words.append(lemmatized_word)

    # 检查是否在 WordNet 中
    lemmatized_words = [word for word in lemmatized_words if is_in_wordnet(word)]

    return sorted(list(set(lemmatized_words)))

def get_wordnet_pos(treebank_tag):
    """将 Treebank 标签转换为 WordNet 标签"""
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    elif treebank_tag.startswith('S'):
        return wordnet.ADJ_SAT
    else:
        return None

def is_in_wordnet(word):
    """检查单词是否在WordNet中"""
    return bool(wordnet.synsets(word))

def write_words_to_file(words, output_file):
    """将单词列表写入文件"""
    with open(output_file, 'w', encoding='utf-8') as output:
        for word in words:
            output.write(f"{word}\n")

"""可选功能"""

def delete_short(words):
    """过滤掉长度小于等于2的单词"""
    return [word for word in words if len(word) > 2]

def filter_words(words, filter_file):
    """过滤掉在 words 中与 filter_file 重复的单词"""
    with open(filter_file, 'r', encoding='utf-8') as file:
        filter_words = set(file.read().splitlines())
    words = list(set(words) - filter_words)
    return words

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
        words = delete_short(words)
    if want_filter_words.lower() == 'y':
        words = filter_words(words, filter_file)
    
    write_words_to_file(words, word_list_file)
    print("生成单词表共含有"+str(len(words))+"个单词")
    print(f"已保存单词列表到 {word_list_file} 文件中")
    input("按 Enter 键退出...")