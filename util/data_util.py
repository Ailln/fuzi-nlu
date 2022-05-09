import re

from ruamel.yaml import YAML


class DataUtil(object):
    def __init__(self, conf):
        self.input_vocab_path = conf["input_vocab_path"]
        self.nlu_path = conf["nlu_path"]
        self.domain_path = conf["domain_path"]
        self.seq_length = conf["seq_length"]
        self.pad_token = "PAD"
        self.unk_token = "UNK"

        self.yaml = YAML()

    def get_yml_data(self, yml_path):
        with open(yml_path, "r") as f_nlu:
            return self.yaml.load(f_nlu)

    @staticmethod
    def get_vocab_data(vocab_path):
        with open(vocab_path, "r") as f_vocab:
            return f_vocab.read().strip().split("\n")

    def get_vocab(self):
        input_vocab_data = self.get_vocab_data(self.input_vocab_path)
        input_vocab = [self.pad_token, self.unk_token] + input_vocab_data

        domain_data = self.get_yml_data(self.domain_path)
        target_vocab = [self.pad_token, self.unk_token, "O"]
        if "entities" in domain_data:
            for entity_item in domain_data["entities"]:
                target_vocab += [f"B-{entity_item}", f"I-{entity_item}"]

        intent_vocab = [self.pad_token, self.unk_token] + domain_data["intents"]

        return input_vocab, input_vocab, intent_vocab

    def word2id(self, input_vocab, sequence_list, max_length):
        seq_len = len(sequence_list)
        if seq_len >= max_length:
            word_item_list = sequence_list[:max_length]
        else:
            word_item_list = sequence_list + [self.pad_token] * (max_length - seq_len)

        id_list = []
        for word in word_item_list:
            if word in input_vocab:
                word_id = input_vocab.index(word)
            else:
                word_id = input_vocab.index(self.unk_token)
            id_list.append(word_id)
        return id_list

    def intent2id(self, intent_vocab, intent):
        if intent in intent_vocab:
            intent_id = intent_vocab.index(intent)
        else:
            intent_id = intent_vocab.index(self.unk_token)
        return intent_id

    def get_train_data(self):
        input_vocab, target_vocab, intent_vocab = self.get_vocab()

        nlu_data = self.get_yml_data(self.nlu_path)
        input_list = []
        target_list = []
        intent_list = []
        for nlu_item in nlu_data["nlu"]:
            if "intent" in nlu_item:
                for example in nlu_item["examples"].strip().split("\n"):
                    example = example[2:]
                    last = 0
                    target_line = ["O"] * len(example)
                    for res in re.finditer(r"\[.*?\]\(.*?\)", example):
                        span = res.span()
                        entity_item = res.group()
                        content = entity_item.split("](")[0][1:]
                        entity = entity_item.split("](")[1][:-1]
                        start = span[0] - last
                        end = start + len(content) - 1
                        example = example[:span[0] - last] + content + example[span[1] - last:]
                        last = len(entity) + 4

                        for i in range(start, end + 1, 1):
                            if i == start:
                                entity_label = f"B-{entity}"
                            else:
                                entity_label = f"I-{entity}"
                            target_line[i] = entity_label

                    input_list.append(self.word2id(input_vocab, [char for char in example], self.seq_length))
                    target_list.append(self.word2id(target_vocab, target_line, self.seq_length))
                    intent_list.append(self.intent2id(intent_vocab, nlu_item["intent"]))

        return input_list, target_list, intent_list

    def get_all_examples(self):
        nlu_data = self.get_yml_data(self.nlu_path)
        example_list = []
        for nlu_item in nlu_data["nlu"]:
            if "intent" in nlu_item:
                for example in nlu_item["examples"].strip().split("\n"):
                    example = example[2:]
                    example_list.append(example)

        return example_list
