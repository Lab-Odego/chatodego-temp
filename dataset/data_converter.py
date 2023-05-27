import jsonlines
import json
from  collections import OrderedDict

text_form = "### 질문: {instruction} ### 답변: {output}"

dataset = list()
with jsonlines.open(".\\KoAlpaca_v1.1.jsonl") as data:
    for line in data.iter():
        data_dict = OrderedDict()
        data = text_form.format(instruction=line['instruction'], output=line['output'])
        data_dict["text"] = data
        dataset.append(data_dict)
            
print(dataset[:10])

with jsonlines.open(".\\odego_data.json", 'w') as file:
    json.dump(data_dict, file, indent='\t', ensure_ascii=False)

    

