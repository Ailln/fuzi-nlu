import torch
import torch.nn as nn
import torch.nn.functional as F

from util.data_util import DataUtil


class JointNLU(nn.Module):
    def __init__(self, config, device):
        super(JointNLU, self).__init__()
        self.embedding_size = config["embedding_size"]
        self.hidden_size = config["hidden_size"]
        self.batch_size = config["batch_size"]
        self.seq_length = config["seq_length"]
        self.dropout_p = 0.5

        data_util = DataUtil(config)
        input_vocab, target_vocab, intent_vocab = data_util.get_vocab()
        input_size = len(input_vocab)
        target_size = len(target_vocab)
        intent_size = len(intent_vocab)
        self.input_vocab = input_vocab
        self.en_embedding = nn.Embedding(input_size, self.embedding_size)
        # batch_first=True: the input and output tensors are provided as (batch, seq, feature)
        self.en_lstm = nn.LSTM(self.embedding_size, self.hidden_size, batch_first=True)

        self.de_embedding = nn.Embedding(target_size, self.embedding_size)
        self.de_lstm = nn.LSTM(self.embedding_size, self.hidden_size, batch_first=True)
        self.de_start = torch.LongTensor([[input_vocab.index(data_util.pad_token)]] * self.batch_size).to(device)
        self.de_slot_output = nn.Linear(self.hidden_size, target_size)
        self.de_intent_output = nn.Linear(self.hidden_size, intent_size)

        self.attn = nn.Linear(self.hidden_size * 2, self.seq_length)
        self.attn_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.attn_slot = nn.Linear(self.hidden_size * 2, self.seq_length)
        self.attn_slot_combine = nn.Linear(self.hidden_size * 2, self.hidden_size)
        self.dropout = nn.Dropout(self.dropout_p)

    def attention_layer(self, embedded, hidden, en_outputs):
        attn_weights = F.softmax(self.attn_slot(torch.cat((embedded, hidden[0].permute(1, 0, 2)), dim=-1)), dim=-1)
        attn_applied = torch.bmm(attn_weights, en_outputs)
        attn_output = F.relu(self.attn_combine(torch.cat((embedded, attn_applied), dim=-1)))
        return attn_output

    def forward(self, input_data):
        # encoder
        en_embedded = self.en_embedding(input_data)
        en_outputs, hidden = self.en_lstm(en_embedded)

        # decoder
        de_embedded = self.de_embedding(self.de_start)
        de_embedded = self.dropout(de_embedded)

        # decode intent
        attn_output = self.attention_layer(de_embedded, hidden, en_outputs)
        intent_score = self.de_intent_output(attn_output.squeeze(1))

        # decoder slot
        decode_list = []
        for _ in range(self.seq_length):
            attn_output = self.attention_layer(de_embedded, hidden, en_outputs)
            de_output, hidden = self.de_lstm(attn_output, hidden)
            slot_score = self.de_slot_output(de_output.squeeze(0))

            _, de_input = torch.max(slot_score, -1)
            de_embedded = self.de_embedding(de_input.detach())
            decode_list.append(slot_score.squeeze(1))

        slot_scores = torch.stack(decode_list, 1)
        return slot_scores, intent_score
