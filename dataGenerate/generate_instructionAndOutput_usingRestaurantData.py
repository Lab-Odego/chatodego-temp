import time
import json
import os
import random
import re
import string
from functools import partial
from multiprocessing import Pool
import numpy as np
import tqdm
from rouge_score import rouge_scorer
# import utils
import fire
import openai
import pandas as pd
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work

path = os.getcwd()
print(type(path))
print(f"path: {path}")
# print(f"path+folder: {path}+{folder}")
OPEN_API_KEY=open(path + "\\api_key.txt", "r").read()
# openai.api_key = os.getenv(OPEN_API_KEY)
openai.api_key = OPEN_API_KEY

'''
    {
        "instruction": "질문0: 비아조 카페의 대표메뉴는 무엇인가요?",
        "output": "답변0: 비아조 카페의 대표메뉴는 <DB>DAEPYO name</DB>입니다. 가격은 6,000원입니다."
    },   if "<DB>" == answer_tag : 
            split
'''


'''
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
'''
# def encode_prompt(prompt_instructions):
#     """Encode multiple prompt instructions into a single string."""
#     prompt = open("./prompt.txt").read() + "\n"

#     for idx, task_dict in enumerate(prompt_instructions):
#         (instruction, input, output) = task_dict["instruction"], task_dict["input"], task_dict["output"]
#         instruction = re.sub(r"\s+", " ", instruction).strip().rstrip(":")
#         input = "<noinput>" if input.lower() == "" else input
#         prompt += f"###\n"
#         prompt += f"{idx + 1}. Instruction: {instruction}\n"
#         prompt += f"{idx + 1}. Input:\n{input}\n"
#         prompt += f"{idx + 1}. Output:\n{output}\n"
#     prompt += f"###\n"
#     prompt += f"{idx + 2}. Instruction:"
#     return prompt
messages = []
prompt = open(file = path + "\\prompt.txt", mode="r", encoding="utf-8").read()
print(prompt)
csv_path = "C:\\Users\\Young\\Desktop\\Young\\10.sideproject\\odego\\dataGenerate\\test_data_for_generating.csv"
df = pd.read_csv(filepath_or_buffer=csv_path, encoding="utf-8")
for index, row in df.iterrows():
    if index >= 1:
        break
    print(f"row {index+1}")
    # user_content = str
    list1 = []
    for col_name, value in row.items():
        # print(f"\t{col_name}: {value}")
        feature = (f"{col_name}: {value}+\n")
        list1.append(feature)
        # user_content = []
        # user_content.append(feature)
        # user_content += feature
        # user_content.append(prompt + feature)
    
    user_content = prompt + ''.join(list1)
    messages = []
    messages.append({"role":"user", "content":f"{user_content}"})
    print(user_content)
#     completion = None
#     completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    
#     print("=====================completion=============================")
#     print(completion)
#     print("=====================completion.choices[0].message========================")
#     print(completion.choices[0].message)
#     print("=====================completion.choices[0].message['content'].strip()========================")
#     print(completion.choices[0].message["content"].strip())
#     output_data = completion.choices[0].message["content"].strip()
#     print(type(output_data))
    
    
#     qa_data = output_data.strip().split('\n\n')
#     print("=====================qa_data========================")
#     print(qa_data)
#     # QA 데이터를 dictionary 형태로 변환하여 리스트에 저장
#     qa_list = []
#     for i, data in enumerate(qa_data):
#         q, a = data.strip().split('\n')
#         # qa_dict = {
#         #     "질문{}".format(i): q,
#         #     "답변{}".format(i): a
#         # }
#         qa_dict = {
#             "instruction": q.replace("###", "").replace("+",""),
#             "output": a.replace("###", "").replace("+","")
#         }
#         qa_list.append(qa_dict)

#     print("=====================qa_list========================")
#     print(qa_list)
#     # 생성한 QA 리스트를 json 파일로 저장
#     with open("output.json", "w", encoding="utf-8") as f:
#         json.dump(qa_list, f, ensure_ascii=False, indent=4)
#     # with open("output_test_data", "w") as outfile:
#     #     json.dump(output_data, outfile)
# # 별점,주소,검색량,운영시간,대표메뉴

# # messages=[]
# # user_content = input("user: ")
# # user_content = ["가게이름: 비아조,\n가게카테고리: 카페,\n별점: 4.3,\n주소: 부산 강서구 식만로 164 (우)46707,\n검색량: 29534,\n운영시간: ['매일 10:00 ~ 22:00'],\n대표메뉴: {'아메리카노': '6,000'}\n인 곳이 있어. 위에서 준 데이터를 기반으로 비아조에 관련하여 사용자들이 물어볼법한 질문 답변 형식의 대화형 데이터셋으로 만들어줘"]
# # messages.append({"role":"user", "content":f"{user_content}"})
# # completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

# # print("=====================completion=============================")
# # print(completion)
# # print("=====================completion.choices[0].message========================")
# # print(completion.choices[0].message)
# # print("=====================completion.choices[0].message['content'].strip()========================")
# # print(completion.choices[0].message["content"].strip())
