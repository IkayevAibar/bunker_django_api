from sys import getdefaultencoding
import codecs
import json
import io
# f = 

character = {}

test_list = ["addinfos.txt","jobs.txt","phobias.txt","hobbies.txt","healthes.txt","characters.txt","biodates.txt","baggages.txt"]
c_list = ["catastrophes_area.txt","catastrophes_days.txt","catastrophes_desc.txt","catastrophes_items.txt","catastrophes_population.txt","catastrophes_type.txt"]

def read_file(txt ,with_points=False):
    variants = {}
    id = 0
    with codecs.open(txt, "rU", "utf-8") as f:
        for line in f:
            if(with_points==False):
                variants[id]=line.strip()
            else:
                obj={}
                obj['name'] = line.strip().split("\t\t")[0]
                obj['cost'] = line.strip().split("\t\t")[1]
                variants[id]=obj
            id+=1
    id=0
    
    character[txt.split('.')[0]]=[variants]
    



read_file("spells.txt")
for i in test_list:
    read_file(i,with_points=True)


with io.open("character.json", "w", encoding="utf-8") as fp:
    s = json.dumps(character, ensure_ascii=False)
    fp.write(s)

character={}
for d in c_list:
    read_file(d)

with io.open("catastrophes.json", "w", encoding="utf-8") as fp:
    s = json.dumps(character, ensure_ascii=False)
    fp.write(s)

# print(variants)


