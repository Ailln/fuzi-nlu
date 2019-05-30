import os

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
import numpy as np

from model.en_decoder import Encoder, Decoder
from util.config_util import read_config
from util.data_util import DataUtil

USE_CUDA = torch.cuda.is_available()
print(f"CUDA: {USE_CUDA}")


def train(config):
    hidden_size = config["hidden_size"]
    save_dir = config["save_dir"]
    learning_rate = config["learning_rate"]
    batch_size = config["batch_size"]
    epoch_size = config["epoch_size"]

    dataset = DataUtil(config)
    input_vocab, target_vocab, intent_vocab = dataset.get_vocab()
    dataloader = DataLoader(dataset, batch_size, shuffle=True)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    encoder = Encoder(len(input_vocab), config)
    decoder = Decoder(len(target_vocab), len(intent_vocab), hidden_size * 2)

    if USE_CUDA:
        encoder = encoder.cuda()
        decoder = decoder.cuda()

    encoder.init_weights()
    decoder.init_weights()

    loss_function_1 = nn.CrossEntropyLoss(ignore_index=0)
    loss_function_2 = nn.CrossEntropyLoss()
    enc_optim = optim.Adam(encoder.parameters(), lr=learning_rate)
    dec_optim = optim.Adam(decoder.parameters(), lr=learning_rate)

    for epoch in range(1, epoch_size+1):
        losses = []
        for i, batch in enumerate(dataloader):
            input_batch, target_batch, intent_batch = batch
            input_batch = input_batch.long()
            target_batch = target_batch.long()
            if USE_CUDA:
                input_batch = input_batch.cuda()
                target_batch = target_batch.cuda()
                intent_batch = intent_batch.cuda()

            input_mask = torch.cat([Variable(torch.ByteTensor(tuple(map(lambda s: s == 0, t.data)))).cuda()
                                if USE_CUDA else Variable(torch.ByteTensor(tuple(map(lambda s: s == 0, t.data))))
                                for t in input_batch]).view(batch_size, -1)

            encoder.zero_grad()
            decoder.zero_grad()

            output, hidden_c = encoder(input_batch, input_mask)
            start_decode = Variable(torch.LongTensor([[input_vocab.index('PAD')] * batch_size])).transpose(1, 0)
            if USE_CUDA:
                start_decode = start_decode.cuda()

            tag_score, intent_score = decoder(start_decode, hidden_c, output, input_mask)

            loss_1 = loss_function_1(tag_score, target_batch.view(-1))
            loss_2 = loss_function_2(intent_score, intent_batch)

            loss = loss_1 + loss_2
            losses.append(loss.data.cpu().numpy() if USE_CUDA else loss.data.numpy())
            loss.backward()

            torch.nn.utils.clip_grad_norm_(encoder.parameters(), 5.0)
            torch.nn.utils.clip_grad_norm_(decoder.parameters(), 5.0)

            enc_optim.step()
            dec_optim.step()

            if i % 10 == 0:
                print(f"Epoch {epoch}: {np.mean(losses)}")
                losses = []

        if epoch % 100 == 0:
            torch.save(encoder, os.path.join(save_dir, f'encoder-{epoch}.pt'))
            torch.save(decoder, os.path.join(save_dir, f'decoder-{epoch}.pt'))
            print(f"Epoch: {epoch} save model...")

    print("Training Complete!")


if __name__ == '__main__':
    train_config = read_config("./config/guotie.yaml")
    train(train_config)
