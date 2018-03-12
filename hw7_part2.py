


count = 0
#### Your Part 2 solution goes here ####
import json

f = open('directory_dict.json', 'r')
dict = f.read()
f.close()

json_dict = json.loads(dict)
for k in json_dict:
    count +=1


#### Your answer output (change the value in the variable, count)####
print('The number of PhD students: ', count)
