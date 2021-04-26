import rdflib
import json

g = rdflib.Graph()
prefix = 'http://www.medicalQA.zju/'

def handle_ill_info(ill_dict:dict):
    """添加疾病实体及一系列关系

    :param ill_dict:
    :return:
    """
    # 共用变量
    name_relation = rdflib.URIRef(prefix + 'name')
    ill_name = ill_dict['gaishu']['ill_name']
    ill_entity = rdflib.URIRef(prefix + f'illness/{ill_name}')

    # 概述里的字面量部分
    category = ['ill_name','insurance','mobidity','susceptible',
                'spread','period','cure_ratio','cost','suggestion','desc']
    for literal_name in category:
        literal_text = rdflib.Literal(ill_dict['gaishu'][literal_name])
        literal_relation = rdflib.URIRef(prefix+literal_name)
        g.add((ill_entity,literal_relation,literal_text))

    # 一般的字面量部分
    category = ['cause', 'prevent', 'symptom', 'inspect',
                'diagnosis', 'treat', 'nursing']
    for literal_name in category:
        literal_text = rdflib.Literal(ill_dict[literal_name])
        literal_relation = rdflib.URIRef(prefix + literal_name)
        g.add((ill_entity, literal_relation, literal_text))


    # 实体部分
    category = ['department','treatment','drugs']
    for entity_name in category:
        entity_relation = rdflib.URIRef(prefix+entity_name)
        entity_list = ill_dict['gaishu'][entity_name]
        for item in entity_list:
            entity = rdflib.URIRef(prefix+entity_name+'/'+item)
            name_literal = rdflib.Literal(item)
            g.add((ill_entity,entity_relation,entity))
            g.add((entity,name_relation,name_literal))

    # 并发症
    neopathy_literal = rdflib.Literal('、'.join(ill_dict['gaishu']['neopathy']))
    neopathy_relation = rdflib.URIRef(prefix+'neopathy')
    g.add((ill_entity,neopathy_relation,neopathy_literal))

    # 食物
    good_food_literal = rdflib.Literal(ill_dict['food']['宜食'])
    good_food_relation = rdflib.URIRef(prefix+'goodfood')
    g.add((ill_entity,good_food_relation,good_food_literal))
    bad_food_literal = rdflib.Literal(ill_dict['food']['忌食'])
    bad_food_relation = rdflib.URIRef(prefix+'badfood')
    g.add((ill_entity,bad_food_relation,bad_food_literal))




def generateRDF():
    """用于生成知识图谱所需RDF文件

    :return:
    """
    with open("../data/data.json",encoding='utf-8') as f:
        while True:
            try:
                line = f.readline()
                ill_dict = json.loads(line)
                handle_ill_info(ill_dict)
            except:
                break
    g.serialize('illness-info.rdf')
if __name__ == "__main__":
    generateRDF()
