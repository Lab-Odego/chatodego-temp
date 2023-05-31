import jsonlines
import json
from  collections import OrderedDict

text_form = "### 질문: {instruction} ### 답변: {output}"

# dataset = list()
# with jsonlines.open(".\\KoAlpaca_v1.1.jsonl", 'r') as data:
#     for line in data.iter():
#         data_dict = OrderedDict()
#         data = text_form.format(instruction=line['instruction'], output=line['output'])
#         data_dict["text"] = data
#         dataset.append(data_dict)
#     print(dataset)
            
# with open(".\\odego_data.json", 'w', encoding="utf-8") as file:
#     json.dump(dataset, file, indent='\t', ensure_ascii=False)


dataset = list()
with jsonlines.open(".\\KoAlpaca_v1.1.jsonl", 'r') as data:
    for line in data.iter():
        data_dict = OrderedDict()
        data_dict["instruction"] = line['instruction']
        data_dict["input"] = ''
        data_dict["output"] = line['output']
        dataset.append(data_dict)

with open(".\\odego_data.json", 'w', encoding="utf-8") as file:
    json.dump(dataset, file, indent='\t', ensure_ascii=False)

