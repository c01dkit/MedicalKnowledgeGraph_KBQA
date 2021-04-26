import questionSearch
import questionSparql

if __name__ == '__main__':
    sparql = questionSearch.sparqlConnect()
    q2s = questionSparql.QuestionSparql([ # 加载自定义词典作为手动分词
        u'./data/illDepartment.txt',
        u'./data/illName.txt',
        u'./data/medicalName.txt',
        u'./data/illClass.txt',
        u'./data/drugs.txt',
        u'./data/extendWords.txt'
    ])

    while True:
        question = input("")
        if question == 'q':
            break

        query = q2s.get_sparql(question) # 语义解析 获取sparsql查询语句

        if query is not None:

            result = sparql.get_sparql_result(query) # 进行查询 以json格式返回结果

            values = sparql.get_sparql_result_value(result) # 解析json 以列表格式返回

            if len(values):
                print("、".join(values))
            else:
                print("数据库暂无此类问题答案")
        else:
            print("啊……这种问法还不清楚是什么意思呢……")