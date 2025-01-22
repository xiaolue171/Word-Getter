# Word-Getter
一个用于获取英文文本中单词并生成单词表的python小程序  
生成单词表可以用于不背单词制作词书，也可以用于其他单词软件导入单词本，或者其他用途
## 功能
使用nltk库进行分词、词干化、wordnet词汇过滤，可以选择删除短词汇、去除指定词汇、乱序输出单词表
## 使用方法
1. 在info.txt中填写相应文件路径：
  - English text是需要提取的英文文本
  - Word list text是输出的词汇表
  - Filter text是指定的用于过滤的词汇表，如果不填写将认为不进行过滤
2. dicts文件夹中有一些已经准备好的用于过滤的词汇表。比如可以选择过滤掉简单的中高考词汇，让单词表里剩下较难的词汇：
  - gaokao.txt是高考词汇
  - zhongkao.txt是中考词汇
  - toefl.txt是托福词汇
  - ielt.txt是雅思词汇
  - gre.txt是GRE词汇
3. 点击运行word_getter.py或word_getter.exe，按照提示选择即可
