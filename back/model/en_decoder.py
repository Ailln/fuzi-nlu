import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

USE_CUDA = torch.cuda.is_available()


class Encoder(nn.Module):
    def __init__(self, input_vocab_size, config):
        super().__init__()
        self.embedding_size = config["embedding_size"]
        self.hidden_size = config["hidden_size"]
        self.n_layers = config["n_layers"]

        self.batch_size = config["batch_size"]

        self.embedding = nn.Embedding(input_vocab_size, self.embedding_size)

        self.lstm = nn.LSTM(self.embedding_size, self.hidden_size, self.n_layers, batch_first=True, bidirectional=True)

    def init_weights(self):
        self.embedding.weight.data.uniform_(-0.1, 0.1)

    def forward(self, input_data, input_masking):
        """
        input : B,T (LongTensor)
        input_masking : B,T
        """
        hidden = Variable(torch.zeros(self.n_layers * 2, input_data.size(0), self.hidden_size))
        if USE_CUDA:
            hidden = hidden.cuda()

        context = Variable(torch.zeros(self.n_layers * 2, input_data.size(0), self.hidden_size))
        if USE_CUDA:
            context = context.cuda()

        output, _ = self.lstm(self.embedding(input_data), (hidden, context))

        real_context = []
        for i, o in enumerate(output):  # B,T,D
            # 得到最后一个output的状态
            real_length = input_masking[i].data.tolist().count(0)
            real_context.append(o[real_length - 1])

        return output, torch.cat(real_context).view(input_data.size(0), -1).unsqueeze(1)


class Decoder(nn.Module):

    def __init__(self, slot_size, intent_size, hidden_size, batch_size=16, n_layers=1, dropout_p=0.1):
        super(Decoder, self).__init__()

        self.hidden_size = hidden_size
        self.slot_size = slot_size
        self.intent_size = intent_size
        self.n_layers = n_layers
        self.dropout_p = dropout_p
        self.batch_size = batch_size

        # Define the layers
        self.embedding = nn.Embedding(self.slot_size, 40)

        # self.dropout = nn.Dropout(self.dropout_p)
        self.lstm = nn.LSTM(40 + self.hidden_size * 2, self.hidden_size, self.n_layers, batch_first=True)
        self.attn = nn.Linear(self.hidden_size, self.hidden_size)  # Attention
        self.slot_out = nn.Linear(self.hidden_size * 2, self.slot_size)
        self.intent_out = nn.Linear(self.hidden_size * 2, self.intent_size)

    def init_weights(self):
        self.embedding.weight.data.uniform_(-0.1, 0.1)

    def Attention(self, hidden, encoder_outputs, encoder_maskings):
        """
        hidden : 1,B,D
        encoder_outputs : B,T,D
        encoder_maskings : B,T # ByteTensor
        """

        hidden = hidden.squeeze(0).unsqueeze(2)

        batch_size = encoder_outputs.size(0)  # B
        max_len = encoder_outputs.size(1)  # T
        energies = self.attn(encoder_outputs.contiguous().view(batch_size * max_len, -1))  # B*T,D -> B*T,D
        energies = energies.view(batch_size, max_len, -1)  # B,T,D
        attn_energies = energies.bmm(hidden).transpose(1, 2)  # B,T,D * B,D,1 --> B,1,T
        attn_energies = attn_energies.squeeze(1).masked_fill(encoder_maskings, -1e12)  # PAD masking

        alpha = F.softmax(attn_energies, dim=1)  # B,T
        alpha = alpha.unsqueeze(1)  # B,1,T
        context = alpha.bmm(encoder_outputs)  # B,1,T * B,T,D => B,1,D

        return context  # B,1,D

    def init_hidden(self, input):
        hidden = Variable(
            torch.zeros(self.n_layers * 1, input.size(0), self.hidden_size)).cuda() if USE_CUDA else Variable(
            torch.zeros(self.n_layers, input.size(0), self.hidden_size))
        context = Variable(
            torch.zeros(self.n_layers * 1, input.size(0), self.hidden_size)).cuda() if USE_CUDA else Variable(
            torch.zeros(self.n_layers, input.size(0), self.hidden_size))
        return (hidden, context)

    def forward(self, input, context, encoder_outputs, encoder_maskings, training=True):
        """
        input : B,L(length)
        enc_context : B,1,D
        """
        # Get the embedding of the current input word
        embedded = self.embedding(input)
        hidden = self.init_hidden(input)
        decode = []
        aligns = encoder_outputs.transpose(0, 1)
        length = encoder_outputs.size(1)
        for i in range(length):  # Input_sequence Output_sequence
            aligned = aligns[i].unsqueeze(1)  # B,1,D
            _, hidden = self.lstm(torch.cat((embedded, context, aligned), 2),
                                  hidden)  # input, context, aligned encoder hidden, hidden

            # for Intent Detection
            if i == 0:
                intent_hidden = hidden[0].clone()
                intent_context = self.Attention(intent_hidden, encoder_outputs, encoder_maskings)
                concated = torch.cat((intent_hidden, intent_context.transpose(0, 1)), 2)  # 1,B,D
                intent_score = self.intent_out(concated.squeeze(0))  # B,D

            concated = torch.cat((hidden[0], context.transpose(0, 1)), 2)
            score = self.slot_out(concated.squeeze(0))
            softmaxed = F.log_softmax(score, dim=1)
            decode.append(softmaxed)
            _, input = torch.max(softmaxed, 1)
            embedded = self.embedding(input.unsqueeze(1))

            context = self.Attention(hidden[0], encoder_outputs, encoder_maskings)

        slot_scores = torch.cat(decode, 1)
        return slot_scores.view(input.size(0) * length, -1), intent_score