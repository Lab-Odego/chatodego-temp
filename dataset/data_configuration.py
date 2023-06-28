# Reference https://github.com/Beomi/KoAlpaca

import json

ko1 = json.load(open('.\\odego_data.json', 'rt', encoding='UTF8'))
ko2 = json.load(open('.\\ko_alpaca_data.json', 'rt', encoding='UTF8'))
total = ko1 + ko2

with open('total_data.json', 'w', encoding='UTF8') as file:
    json.dump(total, file, indent="\t", ensure_ascii=False)

# with open('.\\alpaca_data.json', 'r', encoding='UTF8') as file:
#     data = json.load(file)

# print(len(data))