import torch

from util.conf_util import read_config
from util.data_util import DataUtil

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device: {device}")

config = read_config()
save_dir = config["save_dir"]
batch_size = config["batch_size"]
seq_length = config["seq_length"]
data_util = DataUtil(config)

# load model
model = torch.load(f"{save_dir}/model.pt", map_location=torch.device("cpu"))
model.eval()


def predict(example):
    input_vocab, target_vocab, intent_vocab = data_util.get_vocab()
    target_vocab = input_vocab

    input_list = []
    for _ in range(batch_size):
        id_list = data_util.word2id(input_vocab, [c for c in example], seq_length)
        input_list.append(id_list)
    input_batch = torch.LongTensor(input_list).to(device)
    slot_scores, intent_score = model(input_batch)

    # calculate intent detection accuracy
    intent_score = torch.softmax(intent_score, dim=-1)
    max_intent_prob, max_intent_index = intent_score.max(-1)
    intent_test = intent_vocab[max_intent_index[0]]
    print(f"## input: {example}\n## intent: {intent_test}({max_intent_prob[0]:.4f})")

    # calculate tag detection accuracy
    _, max_tag_index = slot_scores.max(-1)
    target_test = []
    for tag in max_tag_index[0]:
        _tag = target_vocab[tag]
        if _tag == data_util.pad_token:
            break
        else:
            target_test.append(_tag)

    return intent_test


if __name__ == '__main__':
    print("#"*29)
    print("#"*10 + " chatbot " + "#"*10)
    print("#"*29)
    print("// entry 'quit' to quit this program.\n")
    while True:
        data = input(">> ")
        if data != "quit":
            predict(data)
        else:
            print("\n// bye! see you again.\n")
            break
