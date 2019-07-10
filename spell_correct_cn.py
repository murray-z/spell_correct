# -*- coding: utf-8 -*-

import re
import jieba
import json
from xpinyin import Pinyin
from collections import Counter

p = Pinyin()


### 纠错词库准备，将文本转换成拼音，保存成json格式,（这里选用的是《水浒传》）###

def load_stopwords(stopwords_path='./data/stopwords.txt'):
    with open(stopwords_path, encoding='utf-8') as f:
        return [line.strip() for line in f]

def split_text(file_path='./data/水浒传.txt'):
    pinyin_word = {}  # 存放拼音对应词
    stopwords = load_stopwords()
    with open(file_path, encoding='utf-8') as f:
        words = jieba.lcut(re.sub("[\sa-z0-9\r\n]+", "", f.read()))
        word_count = dict(Counter(words))  # 词对应词频
        for key in word_count:
            if key not in stopwords:
                pinyin = p.get_pinyin(key).replace('-', '')
                if pinyin not in pinyin_word:
                    pinyin_word[pinyin] = [key]
                else:
                    pinyin_word[pinyin].append(key)

    with open('./data/word_count.json', 'w', encoding='utf-8') as f:
        json.dump(word_count, f, ensure_ascii=False, indent=4)

    with open('./data/pinyin_word.json', 'w', encoding='utf-8') as f:
        json.dump(pinyin_word, f, ensure_ascii=False, indent=4)


##### copy from spell_correct_en.py ######
def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

#### 利用拼音进行纠错  #####

def load_json(json_file_path):
    with open(json_file_path, encoding='utf-8') as f:
        return json.loads(f.read(), encoding='utf-8')

pinyin_word = load_json('./data/pinyin_word.json')
word_count = load_json('./data/word_count.json')
WORDS = pinyin_word.keys()


def correct(word):
    word_pinyin = p.get_pinyin(word).replace('-', '')
    candidate_pinyin = candidates(word_pinyin)
    ret_dic = {}
    words = []
    for pinyin in candidate_pinyin:
        words.extend(pinyin_word[pinyin])
    for word in words:
        ret_dic[word] = word_count.get(word, 0)
    sort_word = sorted(ret_dic.items(), key=lambda x: x[1], reverse=True)
    return sort_word[0][0]


if __name__ == '__main__':
    print(correct('松江'))
    print(correct('李奎'))
    print(correct('吴宋'))

