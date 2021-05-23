import questionSearch
import questionSparql

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

    query = q2s.get_sparql(question)  # 语义解析 获取sparsq查询语句
    with open('log.txt','a+',encoding='utf-8') as f:
        f.write(question)
        f.write(query)
    if query is not None:

        result = sparql.get_sparql_result(query)  # 进行查询 以json格式返回结果

        values = sparql.get_sparql_result_value(result)  # 解析json 以列表格式返回

        # for index, content in enumerate(values):
        #     values[index] = content.replace('。', '。\n')
        if len(values):
            return "\n".join(values)
        else:
            return "数据库暂无此类问题答案"
    else:
        return "啊……这种问法还不清楚是什么意思呢……"

def prepare(line):
    try:
        return line.split()[0]
    except:
        return 'X'
preparse_dic = open('./data/illName.txt','r',encoding='utf-8')
preparse_dic = list(map(prepare,preparse_dic.readlines()))

def preparse(item,num=6,startwith=True,state=True):
    if not state:
        return []
    ans = []
    bak = []
    for name in preparse_dic:
        if startwith:
            if name.startswith(item):
                ans.append(name)
        elif item in name:
            bak.append(name)
        if len(ans) >= num:
            break

    ans.extend(bak)
    if len(ans) >= num:
        ans = ans[:num]
    return ans