import torch

from util.data_util import DataUtil
from util.conf_util import get_conf
from util.log_util import get_logger

logger = get_logger(__name__)
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"device: {device}")

conf = get_conf()
save_dir = conf["save_dir"]
batch_size = conf["batch_size"]
seq_length = conf["seq_length"]
data_util = DataUtil(conf)

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
    confidence = round(max_intent_prob[0].item(), 4)
    intent = intent_vocab[max_intent_index[0]]

    # calculate tag detection accuracy
    _, max_tag_index = slot_scores.max(-1)
    target_test = []
    for tag in max_tag_index[0]:
        _tag = target_vocab[tag]
        if _tag == data_util.pad_token:
            break
        else:
            target_test.append(_tag)

    return intent, confidence


if __name__ == '__main__':
    print("#"*29)
    print("#"*10 + " chatbot " + "#"*10)
    print("#"*29)
    print("// entry 'quit' to quit this program.\n")
    while True:
        data = input(">> ")
        if data != "quit":
            _intent, _confidence = predict(data)
            print(f"intent: {_intent}({_confidence})")
        else:
            print("\n// bye! see you again.\n")
            break
