import jsonlines
import json
from  collections import OrderedDict

text_form = "### 질문: {instruction} ### 답변: {output}"


# with jsonlines.open('.\\KoAlpaca_v1.1.jsonl', 'r') as jsonl:
#     json_list = list(jsonl)

# for json_str in json_list:
#     result = json.loads(json_str)
#     print(f"result: {result}")
#     print(isinstance(result, dict))

# with open(".\\odego_data.json", 'w') as file:
#     json.dump(result, file, indent='\t', ensure_ascii=False)

dataset = list()
with jsonlines.open(".\\KoAlpaca_v1.1.jsonl", 'r') as data:
    for line in data.iter():
        data_dict = OrderedDict()
        data = text_form.format(instruction=line['instruction'], output=line['output'])
        data_dict["text"] = data
        dataset.append(data_dict)
            
with open(".\\odego_data.json", 'w') as file:
    json.dump(data_dict, file, indent='\t', ensure_ascii=False)

    

