"""
用于编写匹配规则
1. 首先定义关键词：既可以使用自定义词典的pos分词，也可以手动定义token分词
2. 然后在Question类内定义触发时所用的函数，拼接Sparql查询语句
3. 最后在rules列表内添加新的匹配规则，需要定义好权重、说明、匹配规则、调用函数等信息
"""
from refo import finditer, Predicate, Star, Any   # 正则表达式库
import re

SPARQL_PREFIX = u"""
    PREFIX : <http://www.medicalQA.zju/>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
             u"SELECT DISTINCT {select} WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
             u"SELECT COUNT({select}) WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
             u"ASK {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_weight, description=None,
                 condition=None, action=None):
        assert condition and action
        self.condition_weight = condition_weight
        self.description = description
        self.condition = condition
        self.action = action

    def apply(self, word_objects):
        matches = []
        for m in finditer(self.condition, word_objects):
            i, j = m.span()
            matches.extend(word_objects[i:j])
        return self.action(matches), self.condition_weight, self.description



illName = 'nhd'         # 具体的疾病名
medicalName = 'nhn'     # 医学相关的名词
illDepartment = 'nhc'   # 疾病所属科目
illClass = 'nhl'        # 疾病类别
drug = 'nhm'            # 药品名称
illSymptom = 'nhs'         # 疾病症状

illName_entity = (W(pos=illName))
illDepartment_entity = (W(pos=illDepartment))
illClass_entity = (W(pos=illClass))
medical_entity = (W(pos=medicalName))
drug_entity = (W(pos=drug))
illSymptom_pos = (W(pos=illSymptom))

is_ = (W('是'))
dis = (W('不')|W('不能'))
contains = (W('包括') | W('有') | W('涵盖') | W('包含'))
what = (W('什么') | W('哪些') | W('多少')|W('咋'))
should = (W('适合')| W('宜') |W('应该') |W('需要') |W('应当')|W('可以')|W('能')|W('了能'))
whether = (W('有没有')|W('是否')|W('是不是')|W('有无'))
why = (W('为什么')|W('为啥'))

cause = (W('导致') | W('诱因') | W('引起') |W('起因') |W('病因') |W('原因') |W('成因'))
clinic = (W('临床')|W('医学'))
cost = (W('收费')|W('花销')|W('开销')|W('钱'))
cure_ratio = (W('治愈率')| W('康复率') |W('成功率'))
department_of = (W('科室') | W('科'))
desc = (W('介绍')|W('描述'))
diagnosis = (W('诊断')| W('确诊') | W('判断'))
disease = (W('疾病')|W('病'))
drug = (W('药') | W('药物') |W('药品'))
food = (W('食物')|W('吃')|W('摄入'))
inspect = (W('检查')|W('诊断'))
insurance = (W('医保') | W('医疗保险'))
mobidity = (W('患病率') | W('发病率') | W('患病比例') |W('得病率'))
neopathy = (W('并发症'))
nursing = (W('护理'))
period = (W('治疗周期')| W('治疗时间') |W('时间')|W('多久'))
prevent = (W('预防')|W('避免'))
spread = (W('传染') | W('传染性') |W('传播') |W('传播性'))
suggestion = (W('建议')|W('怎么办'))
susceptible = (W('易感人群')|W('人群'))
symptom = (W('症状') | W('表现') |W('状况'))
treat = (W('治疗方式'))
treatment = (W('治')|W('治疗')|W('治愈'))

class Question:
    def __init__(self):
        pass

    @staticmethod
    def find_illness_treat(word_objects):  # 查询疾病治疗方式
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :treat ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_suggestion(word_objects):  # 查询疾病建议
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"{" + u"?a :ill_name '{illName}'." \
                    u"?a :suggestion ?x.".format(illName=w.token) + u"} UNION "\
                    u"{" + u"?a :ill_name '{illName}'." \
                    u"?a :nursing ?x.".format(illName=w.token) + u"}"


                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_inspect(word_objects):  # 查询疾病临床检查手段
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :inspect ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_cure_ratio(word_objects):  # 查询疾病治愈率
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :cure_ratio ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_prevent(word_objects):  # 查询疾病预防手段
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :prevent ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_nursing(word_objects):  # 查询疾病护理方式
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :nursing ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_desc(word_objects):  # 查询疾病简介
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :desc ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_badfood(word_objects):  # 查询疾病忌食
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :badfood ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_goodfood(word_objects):  # 查询疾病宜食
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :goodfood ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_diagnosis(word_objects):  # 查询疾病诊断方式
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :diagnosis ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_susceptible(word_objects):  # 查询疾病易感人群
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :susceptible ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_mobidity(word_objects):  # 查询疾病发病率
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :mobidity ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_cost(word_objects):  # 查询疾病开销
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :cost ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_cause(word_objects):  # 查询疾病起因
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :cause ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_symptom(word_objects):  # 查询疾病症状
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :symptom ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def judge_illness(word_objects):  # 根据症状查询疾病
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illSymptom:
                e = u"?a :ill_name ?x." \
                    u"?a :symptom ?b."\
                    u"FILTER regex(?b, '{illsymtom}')".format(illsymtom=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_neopathy(word_objects):  # 查询疾病并发症
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :neopathy ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_cure_period(word_objects):  # 查询疾病治疗周期
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :period ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_spread(word_objects):  # 查询疾病传染性
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :spread ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_insurance(word_objects):  # 查询疾病是否纳入医疗保险
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :insurance ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_department(word_objects):  # 查询疾病所属科室
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :department ?b." \
                    u"?b :name ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_drugs(word_objects):  # 查询疾病所用药品
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :drugs ?b." \
                    u"?b :name ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_illness_treatment(word_objects):  # 查询疾病治疗手段
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == illName:
                e = u"?a :ill_name '{illName}'." \
                    u"?a :treatment ?b." \
                    u"?b :name ?x".format(illName=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

    @staticmethod
    def find_department_illnesses(word_objects):  # 查询某个科室下的疾病
        select = u"?x"

        sparql = None
        for w in word_objects:
            if w.pos == illDepartment:
                e = u"?a :department ?b." \
                    u"?b :name '{illDepartment}'." \
                    u"?a :ill_name ?x".format(illDepartment=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
            elif w.pos == illClass:
                e = u"?a :ill_name '{illClass}'." \
                    u"?a :department ?b." \
                    u"?c :department ?b." \
                    u"?c :ill_name ?x".format(illClass=w.token)

                sparql = SPARQL_SELECT_TEM.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression=e)
                break
        return sparql

rules = [
    Rule(condition_weight=2, description='查询疾病所属科室',
         condition=(illName_entity + Star(Any(), greedy=False)+ department_of + Star(Any(), greedy=False)),
         action=Question.find_illness_department),

    Rule(condition_weight=4, description='查询科室下属疾病',
         condition=((illDepartment_entity + contains + what + Star(disease,greedy=False)) |
                    (illClass_entity + Star(Any(), greedy=False) + contains + what + Star(disease,greedy=False))),
         action=Question.find_department_illnesses),

    Rule(condition_weight=2, description='查询疾病是否医保',
         condition=(illName_entity + Star(Any(),greedy=False) + insurance),
         action=Question.find_illness_insurance),

    Rule(condition_weight=2, description='查询疾病传染性',
         condition=(illName_entity + Star(Any(), greedy=False) + spread),
         action=Question.find_illness_spread),

    Rule(condition_weight=2, description='查询疾病并发症',
         condition=(illName_entity + Star(Any(), greedy=False) + neopathy),
         action=Question.find_illness_neopathy),

    Rule(condition_weight=2, description='查询疾病治疗周期',
         condition=(illName_entity + Star(Any(), greedy=False) + period),
         action=Question.find_illness_cure_period),

    Rule(condition_weight=2, description='查询疾病临床检查手段',
         condition=((illName_entity + Star(Any() | clinic, greedy=False) + inspect)|
                    (whether+Star(Any(),greedy=False)+illName_entity)),
         action=Question.find_illness_inspect),

    Rule(condition_weight=2, description='查询疾病诊断方式',
         condition=(illName_entity + Star(Any() | clinic, greedy=False) + diagnosis),
         action=Question.find_illness_diagnosis),

    Rule(condition_weight=3, description='查询疾病治疗费用',
         condition=(illName_entity + Star(Any(), greedy=False) + cost),
         action=Question.find_illness_cost),

    Rule(condition_weight=2, description='查询疾病治愈率',
         condition=(illName_entity + Star(Any(), greedy=False) + cure_ratio),
         action=Question.find_illness_cure_ratio),

    Rule(condition_weight=2, description='查询疾病预防手段',
         condition=((illName_entity + Star(Any(), greedy=False) + prevent)|
                    (prevent + Star(Any(),greedy=False)+illName_entity)),
         action=Question.find_illness_prevent),

    Rule(condition_weight=2, description='查询疾病护理方式',
         condition=(illName_entity + Star(Any(), greedy=False) + nursing),
         action=Question.find_illness_nursing),

    Rule(condition_weight=3, description='查询疾病建议',
         condition=(illName_entity + Star(Any(), greedy=False) + suggestion),
         action=Question.find_illness_suggestion),

    Rule(condition_weight=3, description='查询疾病宜食',
         condition=(illName_entity + Star(Any(), greedy=False) + Star(should,greedy=False) + food),
         action=Question.find_illness_goodfood),

    Rule(condition_weight=4, description='查询疾病忌食',
         condition=(illName_entity + Star(Any(), greedy=False) + dis + Star(should,greedy=False) + food),
         action=Question.find_illness_badfood),

    Rule(condition_weight=1, description='查询疾病简介',
         condition=((illName_entity + Star(Any(), greedy=False) + desc)|
                    (what+Star(Any(),greedy=False)+illName_entity)|
                    (illName_entity+Star(Any(),greedy=False)+what)|
                    (desc+Star(Any(),greedy=False)+illName_entity)),
         action=Question.find_illness_desc),

    Rule(condition_weight=2, description='查询疾病发病率',
         condition=(illName_entity + Star(Any(), greedy=False) + mobidity),
         action=Question.find_illness_mobidity),

    Rule(condition_weight=2, description='查询疾病治疗手段',
         condition=(illName_entity + Star(Any(), greedy=False) + treatment),
         action=Question.find_illness_treatment),

    Rule(condition_weight=2, description='查询疾病易感人群',
         condition=(illName_entity + Star(Any(), greedy=False) + susceptible),
         action=Question.find_illness_susceptible),

    Rule(condition_weight=2, description='查询疾病起因',
         condition=(illName_entity + Star(Any(), greedy=False) + cause),
         action=Question.find_illness_cause),

    Rule(condition_weight=2, description='查询疾病症状',
         condition=(illName_entity + Star(Any(), greedy=False) + symptom),
         action=Question.find_illness_symptom),

    Rule(condition_weight=2, description='查询疾病治疗方式',
         condition=(illName_entity + Star(Any(), greedy=False) + treat),
         action=Question.find_illness_treat),

    Rule(condition_weight=4, description='查询疾病所用药物',
         condition=(illName_entity + Star(Any(),greedy=False) + drug),
         action=Question.find_illness_drugs),

    Rule(condition_weight=5, description='根据症状查询疾病',
         condition=((illSymptom_pos + Star(Any(),greedy=False) + disease)|
                    (why + Star(Any(),greedy=False) + illSymptom_pos)|
                    (illSymptom_pos + Star(Any(),greedy=False) + what)),
         action=Question.judge_illness)
   ]
