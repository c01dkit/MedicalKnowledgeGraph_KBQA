import questionSearch
import questionSparql

if __name__ == '__main__':
    sparql = questionSearch.sparqlConnect()
    q2s = questionSparql.QuestionSparql([   # 加载自定义词典作为手动分词
        u'./data/illDepartment.txt',        # 疾病科室
        u'./data/illName.txt',              # 疾病名称
        u'./data/medicalName.txt',          # 医学名词
        u'./data/illClass.txt',             # 疾病分类
        u'./data/drugs.txt',                # 药品名称
        u'./data/symptom.txt',              # 疾病症状
        u'./data/extendWords.txt'           # 拓展词典
    ])
    while True:
        question = input("")
        if question == 'q':
            break

        query = q2s.get_sparql(question) # 语义解析 获取sparsql查询语句

        if query is not None:

            result = sparql.get_sparql_result(query) # 进行查询 以json格式返回结果

            values = sparql.get_sparql_result_value(result) # 解析json 以列表格式返回

            for index, content in enumerate(values):
                values[index] = content.replace('。','。\n')
            if len(values):
                print("\n".join(values))
            else:
                print("数据库暂无此类问题答案")
        else:
            print("啊……这种问法还不清楚是什么意思呢……")