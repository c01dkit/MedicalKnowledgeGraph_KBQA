#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys,codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

HTML1 = 'Content-type:text/html\n\n'\
'<html>\n'\
'    <head>\n'\
'        <meta charset="utf-8">\n'\
'        <title>疾病问答</title>\n'\
'    </head>\n'\
'    <body>\n'\
'        <form method="post">\n'\
'        请输入问题<input type="text" name="query"/>\n'\
'        <input type="submit" value="提交"/>\n'\
'        </form>\n'\
'        <p>{answer}</p>\n'\
'    </body>\n'\
'</html>\n'
HTML = 'Content-type:text/html\n\n'\
'<meta http-equiv="refresh" content="1; url=http://www.c01dkit.com:3000">'\
'<h1>正在跳转至<a href="http://www.c01dkit.com:3000">http://www.c01dkit.com:3000</a></h1>{answer}'
import questionSearch,questionSparql
sparql = questionSearch.sparqlConnect()
q2s = questionSparql.QuestionSparql([  # 加载自定义词典作为手动分词
    u'./data/illDepartment.txt',  # 疾病科室
    u'./data/illName.txt',  # 疾病名称
    u'./data/medicalName.txt',  # 医学名词
    u'./data/illClass.txt',  # 疾病分类
    u'./data/drugs.txt',  # 药品名称
    u'./data/symptom.txt',  # 疾病症状
    u'./data/extendWords.txt'  # 拓展词典
    ])

def medical_query(question):
    query = q2s.get_sparql(question)  # 语义解析 获取sparsql查询语句
    if query is not None:
        result = sparql.get_sparql_result(query)  # 进行查询 以json格式返回
        values = sparql.get_sparql_result_value(result)  # 解析json 以列表格式返回
        for index, content in enumerate(values):
            values[index] = content.replace('。', '。\n')
        if len(values):
            return "\n".join(values)
        else:
            return "暂时没有相关信息"
    else:
        return "啊……这种问法还不清楚是什么意思呢……"

import cgi,cgitb

form = cgi.FieldStorage()
q = form.getvalue('query')
answer = ''
if q is not None and q != '':
    answer = medical_query(q)
print(HTML.format(answer=answer))
