# coding=utf-8


import wordHandle
import questionMapping

class QuestionSparql:
    def __init__(self, dict_paths):
        self.tw = wordHandle.Tagger(dict_paths)  # 自定义分词
        self.rules = questionMapping.rules  # 定义搜索规则
    def get_sparql(self, question):  # 语义解析
        word_objects = self.tw.get_word_objects(question)
        queries_dict = dict()
        for i in word_objects:
            print(i.__dict__)
        for rule in self.rules:
            query, num, desc= rule.apply(word_objects)
            if query is not None:
                queries_dict[num] = query
                print(f'匹配问题: {desc} 其使用关键字个数为{num}')
        if len(queries_dict) == 0:
            return None
        elif len(queries_dict) == 1:
            for key, value in queries_dict.items():
                return value
        else:
            # 产生多个匹配时，选择权重最高的匹配结果返回
            sorted_dict = sorted(queries_dict.items(), key=lambda item: item[0], reverse=True)
            return sorted_dict[0][1]
