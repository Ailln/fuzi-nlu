import os

import torch
from torch.autograd import Variable

from util.config_util import read_config
from util.convert_util import ConvertUtil

USE_CUDA = torch.cuda.is_available()


def predict(text):
    config = read_config("./config/guotie.yaml")
    save_dir = config["save_dir"]
    batch_size = 1

    convert_util = ConvertUtil(config)
    test_input_list, vacab_list = convert_util.gen_test_data(text)
    input_vocab, target_vocab, intent_vocab = vacab_list

    # load model
    decoder = torch.load(os.path.join(save_dir, 'decoder-100.pt'))
    encoder = torch.load(os.path.join(save_dir, 'encoder-100.pt'))

    input_batch = torch.LongTensor(test_input_list)
    if USE_CUDA:
        input_batch = input_batch.cuda()

    input_mask = torch.cat([Variable(torch.ByteTensor(tuple(map(lambda s: s == 0, t.data)))).cuda()
                            if USE_CUDA else Variable(torch.ByteTensor(tuple(map(lambda s: s == 0, t.data))))
                            for t in input_batch]).view(batch_size, -1)
    encoder.zero_grad()
    decoder.zero_grad()

    output, hidden_c = encoder(input_batch, input_mask)
    start_decode = Variable(torch.LongTensor([[input_vocab.index("PAD")] * batch_size])).transpose(1, 0)
    if USE_CUDA:
        start_decode = start_decode.cuda()

    tag_score, intent_score = decoder(start_decode, hidden_c, output, input_mask)

    # batch, sequence_max_length, tag_length
    tag_score = tag_score.view(batch_size, -1, list(tag_score[1].size())[0])

    # calculate intent detection accuracy
    _, max_index = intent_score.max(1)
    intent_test = intent_vocab[max_index[0]]
    print(f"intent: {intent_test}")

    # calculate tag detection accuracy
    _, max_tag_index = tag_score.max(2)
    target_test = []
    for tag in max_tag_index[0]:
        target_test.append(target_vocab[tag])

    return intent_test


if __name__ == '__main__':
    predict("你叫什么名字？")

