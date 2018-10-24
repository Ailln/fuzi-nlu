import json

import numpy as np


class ConvertUtil(object):
    def __init__(self, config):
        self.input_json_path = config["input_json_path"]
        self.input_iob_path = config["input_iob_path"]

        self.train_data_path = config["train_data_path"]
        self.validate_data_path = config["validate_data_path"]
        self.input_vocab_path = config["input_vocab_path"]
        self.target_vocab_path = config["target_vocab_path"]
        self.intent_vocab_path = config["intent_vocab_path"]
        self.seq_length = config["seq_length"]

    def json2iob(self):
        with open(self.input_json_path, "r", encoding='utf_8_sig') as f_read:
            json_data = json.load(f_read)

        bio_save_list = []
        label_list = []
        for json_item in json_data["rasa_nlu_data"]["common_examples"]:
            # TODO 特殊字符替换
            text = json_item["text"].replace(" ", ",")
            text_split = " ".join([word for word in text])
            intent = json_item["intent"]
            entity_list = json_item["entities"]
            label_entity_list = ["O" for _ in range(len(text))]
            for entity_item in entity_list:
                pos_start = entity_item["start"]
                pos_end = entity_item["end"]
                label = entity_item["entity"]
                label_entity_list[pos_start] = f"B-{label}"
                label_entity_list[pos_end-1] = f"I-{label}"
                if f"B-{label}" not in label_list:
                    label_list.append(f"B-{label}")
                    label_list.append(f"I-{label}")

            label_entity = " ".join(label_entity_list)
            save_line = f"{text_split}\t{label_entity}\t{intent}"
            bio_save_list.append(save_line)

        with open(self.input_iob_path, "w", encoding="utf-8") as f_output:
            f_output.write("\n".join(bio_save_list))

    @staticmethod
    def read_data(input_data_path):
        input_data_list = []
        target_data_list = []
        intent_data_list = []
        with open(input_data_path, "r") as f_input:
            for line in f_input:
                input_data, target_data, intent_data = line.split("\t")
                input_data_list.append(input_data.split())
                target_data_list.append(target_data.split())
                intent_data_list.append([intent_data.strip()])

        return input_data_list, target_data_list, intent_data_list

    @staticmethod
    def get_vocab(vocab_path, all_data, is_train):
        if is_train:
            vocab_list = ["PAD", "UNK"]
            for data_item in all_data:
                for data in data_item:
                    if data not in vocab_list:
                        vocab_list.append(data)
            with open(vocab_path, "w") as f_vocab:
                f_vocab.write("\n".join(vocab_list))
        else:
            with open(vocab_path, "r") as f_vocab:
                vocab_list = [v.strip() for v in f_vocab]

        return vocab_list

    @staticmethod
    def word2id(input_vocab, input_word_list, seq_length):
        all_input_id_list = np.zeros([len(input_word_list), seq_length])
        for i_input, word_item in enumerate(input_word_list):
            word_item_list = [word for word in word_item]
            word_item_len = len(word_item_list)

            if word_item_len >= seq_length:
                word_item_list = word_item_list[:seq_length]
            else:
                word_item_list = word_item_list + ["PAD"] * (seq_length - word_item_len)

            input_id_list = []
            for word in word_item_list:
                if word in input_vocab:
                    word_id = input_vocab.index(word)
                else:
                    word_id = input_vocab.index("UNK")
                input_id_list.append(word_id)
            all_input_id_list[i_input] = np.array(input_id_list)

            read_percent = i_input / (len(input_word_list) / 100)
            if not i_input % 10:
                print(f">> convert: {read_percent:3.1f}%", end="\r")

        return all_input_id_list

    @staticmethod
    def intent2id(intent_vocab, intent_data):
        target_id_list = []
        for intent_item in intent_data:
            if intent_item[0] in intent_vocab:
                target_id_list.append(intent_vocab.index(intent_item[0]))
            else:
                raise ValueError(intent_item[0])
        return target_id_list

    def gen_train_data(self):
        print("\n>> start read train data...")
        train_input, train_target, train_intent = self.read_data(self.train_data_path)
        print(">> start read validate data...")
        validate_input, validate_target, validate_intent = self.read_data(self.validate_data_path)

        print("\n>> start read input vocab...")
        input_vocab = self.get_vocab(self.input_vocab_path, train_input, True)
        print(">> start read target vocab...")
        target_vocab = self.get_vocab(self.target_vocab_path, train_target, True)
        print(">> start read intent vocab...")
        intent_vocab = self.get_vocab(self.intent_vocab_path, train_intent, True)

        print("\n>> word to id: train...")
        train_input_list = self.word2id(input_vocab, train_input, self.seq_length)
        print(">> word to id: validate...")
        validate_input_list = self.word2id(input_vocab, validate_input, self.seq_length)

        print("\n>> target to id: train...")
        train_target_list = self.word2id(target_vocab, train_target, self.seq_length)
        print(">> target to id: validate...")
        validate_target_list = self.word2id(target_vocab, validate_target, self.seq_length)

        print("\n>> intent to id: train...")
        train_intent_list = self.intent2id(intent_vocab, train_intent)
        print(">> intent to id: validate...")
        validate_intent_list = self.intent2id(intent_vocab, validate_intent)

        train_data_list = [train_input_list, train_target_list, train_intent_list]
        validate_data_list = [validate_input_list, validate_target_list, validate_intent_list]
        vacab_list = [input_vocab, target_vocab, intent_vocab]

        return train_data_list, validate_data_list, vacab_list

    def gen_test_data(self, test_data):
        # print("\n>> start read input vocab...")
        input_vocab = self.get_vocab(self.input_vocab_path, "", False)
        # print(">> start read target vocab...")
        target_vocab = self.get_vocab(self.target_vocab_path, "", False)
        # print(">> start read intent vocab...")
        intent_vocab = self.get_vocab(self.intent_vocab_path, "", False)

        # print("\n>> word to id: test...")
        test_input_list = self.word2id(input_vocab, [test_data], self.seq_length)

        vacab_list = [input_vocab, target_vocab, intent_vocab]

        return test_input_list, vacab_list
