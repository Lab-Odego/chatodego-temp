
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

tokenizer = LlamaTokenizer.from_pretrained("../KoAlpaca/")
model = LlamaForCausalLM.from_pretrained("../KoAlpaca/")

model.generate(**tokenizer('안녕하세요?', return_tensors='pt'))