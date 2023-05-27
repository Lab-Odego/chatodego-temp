# Reference https://github.com/Beomi/KoAlpaca

import json

ko = json.load(open('.\\KoAlpaca_v1.1.json', 'rt', encoding='UTF8'))
en = json.load(open('.\\en_alpaca_data.json', 'rt', encoding='UTF8'))
total = ko + en

# with open('alpaca_data.json', 'w', encoding='UTF8') as file:
#     json.dump(total, file, indent="\t", ensure_ascii=False)

with open('.\\alpaca_data.json', 'r', encoding='UTF8') as file:
    data = json.load(file)

print(len(data))