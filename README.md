# 拼写纠错
> 利用贝叶斯和编辑距离进行中文、英文拼写纠错

## 目录
- spell_correct_cn.py 中文纠错
- spell_correct_en.py 英文纠错

## 原理
- 参考[How to Write a Spelling Corrector](https://norvig.com/spell-correct.html)
- 中文纠错将中文转换成拼音，再利用英文原理进行纠错

## 示例
```python

    spell_correct = SpellCorrect(train=False)
    print(spell_correct.correct('宋江'))
    print(spell_correct.correct('松江'))
    print(spell_correct.correct('李奎'))
    print(spell_correct.correct('吴宋'))
    print(spell_correct.correct('送三连'))

output:
['宋江', '松江', '宋将']
['宋江', '松江', '宋将']
['李逵']
['武松']
['宋三郎', '宋万先']
```

