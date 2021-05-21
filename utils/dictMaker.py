import json

def generateDICT():
    """用于生成专有名词字典文件

    :return:
    """
    # output = open("../data/illName.txt",'w+',encoding='utf-8')
    # output = open("../data/illDepartment.txt",'w+',encoding='utf-8')
    # output = open("../data/drugs.txt", 'w+', encoding='utf-8')
    output = open("../data/rawSymptom.txt", 'w+', encoding='utf-8')
    s = []
    with open("../data/data.json",encoding='utf-8') as f:
        while True:
            try:
                line = f.readline()
                data_dict = json.loads(line)
                s.append((data_dict['gaishu']['ill_name'],data_dict['symptom'].replace('，','\n')))
            except:
                break
    li = list(s)
    for i in li:
        print(i[0],i[1], file=output,sep='@@@@')
    output.flush()
    output.close()

if __name__ == "__main__":
    generateDICT()

# https://wenku.baidu.com/view/3c77749c31b765ce0408144e.html 常用分词词性对照表