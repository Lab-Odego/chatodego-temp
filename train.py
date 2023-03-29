# Local Directory that downloaded pre-trained models - C:\Users\...\.cache\huggingface\hub

import copy
import logging
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Sequence

import torch
import transformers
from torch.utils.data import Dataset
from transformers import Trainer

import utils

ROOT_PATH = "C:\\Users\\82109\\Desktop\\code_repos\\odego"

MODEL_PATH = "decapoda-research/llama-7b-hf"
DATA_PATH = os.path.join(ROOT_PATH, '\\dataset\\ko_alpaca_data.json')
OUTPUT_DIR = ROOT_PATH

IGNORE_INDEX = -100
DEFAULT_PAD_TOKEN = "[PAD]"
DEFAULT_EOS_TOKEN = "</s>"
DEFAULT_BOS_TOKEN = "</s>"
DEFAULT_UNK_TOKEN = "</s>"

PROMPT_DICT = {
    # 추가적인 input data가 있는 경우,
    "prompt_input": (
        "Below is an instruction that describes a task, paired with an input that provides further context. "
        "Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:"
    ),
    # 추가적인 input data가 없는 경우,
    "prompt_no_input": (
        "Below is an instruction that describes a task. "
        "Write a response that appropriately completes the request.\n\n"
        "### Instruction:\n{instruction}\n\n### Response:"
    ),
}

# Parser Arguments - Path of model
@dataclass
class ModelArguments:
    model_name_or_path: Optional[str] = field(default="facebook/opt-125m")

# Parser Arguments - Path of dataset
@dataclass
class DataArguments:
    data_path: str = field(default=None, metadata={"help": "Path to the training data."})

# Parser Arguments - Using args for training
@dataclass
class TrainingArguments(transformers.TrainingArguments):
    cache_dir: Optional[str] = field(default=None)
    optim: str = field(default="adamw_torch")
    model_max_length: int = field(
        default=512,
        metadata={"help": "Maximum sequence length. Sequences will be right padded (and possibly truncated)."},
    )

# Save model's states
def safe_save_model_for_hf_trainer(trainer: transformers.Trainer, output_dir: str):
    """Collects the state dict and dump to disk."""
    # 모델의 weight를 dictionary 형태로 저장
    state_dict = trainer.model.state_dict()
    if trainer.args.should_save:
        # weight들이 cuda에 있으므로, cpu에 위치하게 바꿈.
        cpu_state_dict = {key: value.cpu() for key, value in state_dict.items()}
        del state_dict
        # 가중치를 저장함.
        trainer._save(output_dir, state_dict=cpu_state_dict)  # noqa

def smart_tokenizer_and_embedding_resize(
    special_tokens_dict: Dict,
    tokenizer: transformers.PreTrainedTokenizer,
    model: transformers.PreTrainedModel,
):
    """Resize tokenizer and embedding.

    Note: This is the unoptimized version that may make your embedding size not be divisible by 64.
    """
    num_new_tokens = tokenizer.add_special_tokens(special_tokens_dict)
    model.resize_token_embeddings(len(tokenizer))

    if num_new_tokens > 0:
        input_embeddings = model.get_input_embeddings().weight.data
        output_embeddings = model.get_output_embeddings().weight.data

        input_embeddings_avg = input_embeddings[:-num_new_tokens].mean(dim=0, keepdim=True)
        output_embeddings_avg = output_embeddings[:-num_new_tokens].mean(dim=0, keepdim=True)

        input_embeddings[-num_new_tokens:] = input_embeddings_avg
        output_embeddings[-num_new_tokens:] = output_embeddings_avg

def _tokenize_fn(strings: Sequence[str], tokenizer: transformers.PreTrainedTokenizer) -> Dict:
    """Tokenize a list of strings."""
    tokenized_list = [
        tokenizer(
            text,
            return_tensors="pt",
            padding="longest",
            max_length=tokenizer.model_max_length,
            truncation=True,
        )
        for text in strings
    ]
    input_ids = labels = [tokenized.input_ids[0] for tokenized in tokenized_list]
    input_ids_lens = labels_lens = [
        tokenized.input_ids.ne(tokenizer.pad_token_id).sum().item() for tokenized in tokenized_list
    ]
    return dict(
        input_ids=input_ids,
        labels=labels,
        input_ids_lens=input_ids_lens,
        labels_lens=labels_lens,
    )

def preprocess(
    sources: Sequence[str],
    targets: Sequence[str],
    tokenizer: transformers.PreTrainedTokenizer,
) -> Dict:
    """Preprocess the data by tokenizing."""
    examples = [s + t for s, t in zip(sources, targets)]
    examples_tokenized, sources_tokenized = [_tokenize_fn(strings, tokenizer) for strings in (examples, sources)]
    input_ids = examples_tokenized["input_ids"]
    labels = copy.deepcopy(input_ids)
    for label, source_len in zip(labels, sources_tokenized["input_ids_lens"]):
        label[:source_len] = IGNORE_INDEX
    return dict(input_ids=input_ids, labels=labels)


class SupervisedDataset(Dataset):
    """Dataset for supervised fine-tuning."""

    def __init__(self, data_path: str, tokenizer: transformers.PreTrainedTokenizer):
        super(SupervisedDataset, self).__init__()
        # alpaca_data.json 파일에서 list 형태로 데이터 읽음.
        logging.warning("Loading data...")
        list_data_dict = utils.jload(data_path)

        # prompt 생성
        logging.warning("Formatting inputs...")
        prompt_input, prompt_no_input = PROMPT_DICT["prompt_input"], PROMPT_DICT["prompt_no_input"]

        #
        sources = [
            prompt_input.format_map(example) if example.get("input", "") != "" else prompt_no_input.format_map(example)
            for example in list_data_dict
        ]
        targets = [f"{example['output']}{tokenizer.eos_token}" for example in list_data_dict]

        logging.warning("Tokenizing inputs... This may take some time...")
        data_dict = preprocess(sources, targets, tokenizer)

        self.input_ids = data_dict["input_ids"]
        self.labels = data_dict["labels"]

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, i) -> Dict[str, torch.Tensor]:
        return dict(input_ids=self.input_ids[i], labels=self.labels[i])

@dataclass
class DataCollatorForSupervisedDataset(object):
    """Collate examples for supervised fine-tuning."""

    tokenizer: transformers.PreTrainedTokenizer

    def __call__(self, instances: Sequence[Dict]) -> Dict[str, torch.Tensor]:
        input_ids, labels = tuple([instance[key] for instance in instances] for key in ("input_ids", "labels"))
        input_ids = torch.nn.utils.rnn.pad_sequence(
            input_ids, batch_first=True, padding_value=self.tokenizer.pad_token_id
        )
        labels = torch.nn.utils.rnn.pad_sequence(labels, batch_first=True, padding_value=IGNORE_INDEX)
        return dict(
            input_ids=input_ids,
            labels=labels,
            attention_mask=input_ids.ne(self.tokenizer.pad_token_id),
        )

def make_supervised_data_module(tokenizer: transformers.PreTrainedTokenizer, data_args) -> Dict:
    """Make dataset and collator for supervised fine-tuning."""
    train_dataset = SupervisedDataset(tokenizer=tokenizer, data_path=data_args.data_path)
    data_collator = DataCollatorForSupervisedDataset(tokenizer=tokenizer)
    return dict(train_dataset=train_dataset, eval_dataset=None, data_collator=data_collator)

# train function
def train():
    parser = transformers.HfArgumentParser((ModelArguments, DataArguments, TrainingArguments))
    model_args, data_args, training_args = parser.parse_args_into_dataclasses(['--model_name_or_path', MODEL_PATH,
                                                                               '--output_dir', ROOT_PATH, 
                                                                               '--data_path', DATA_PATH])
    
    # model = transformers.AutoModelForCausalLM.from_pretrained(
    #     model_args.model_name_or_path,
    #     cache_dir=training_args.cache_dir,
    # )

    # tokenizer = transformers.AutoTokenizer.from_pretrained(
    #     model_args.model_name_or_path,
    #     cache_dir=training_args.cache_dir,
    #     model_max_length=training_args.model_max_length,
    #     padding_side="right",
    #     use_fast=False,
    # )
    # if tokenizer.pad_token is None:
    #     smart_tokenizer_and_embedding_resize(
    #         special_tokens_dict=dict(pad_token=DEFAULT_PAD_TOKEN),
    #         tokenizer=tokenizer,
    #         model=model,
    #     )
    # if "llama" in model_args.model_name_or_path:
    #     tokenizer.add_special_tokens(
    #         {
    #             "eos_token": DEFAULT_EOS_TOKEN,
    #             "bos_token": DEFAULT_BOS_TOKEN,
    #             "unk_token": DEFAULT_UNK_TOKEN,
    #         }
    #     )

    # data_module = make_supervised_data_module(tokenizer=tokenizer, data_args=data_args)
    # trainer = Trainer(model=model, tokenizer=tokenizer, args=training_args, **data_module)
    # trainer.train()
    # trainer.save_state()
    # safe_save_model_for_hf_trainer(trainer=trainer, output_dir=training_args.output_dir)


if __name__ == "__main__":
    train()