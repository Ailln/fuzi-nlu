import os

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchmetrics

from model.seq2seq import JointNLU
from util.conf_util import read_config
from util.dataset_util import DatasetUtil

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"device: {device}")


def train(config):
    save_dir = config["save_dir"]
    learning_rate = config["learning_rate"]
    batch_size = config["batch_size"]
    epoch_size = config["epoch_size"]

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    train_dataset = DatasetUtil(config)
    train_dataloader = DataLoader(train_dataset, batch_size, shuffle=True, drop_last=True)
    validate_dataset = DatasetUtil(config)
    validate_dataloader = DataLoader(validate_dataset, batch_size, shuffle=True, drop_last=True)

    model = JointNLU(config, device).to(device)
    model.train()

    slot_loss = nn.CrossEntropyLoss()
    intent_loss = nn.CrossEntropyLoss()
    model_optim = optim.Adam(model.parameters(), lr=learning_rate)

    val_slot_acc = torchmetrics.Accuracy()
    val_intent_acc = torchmetrics.Accuracy()

    slot_acc = 0
    intent_acc = 0
    for epoch in range(1, epoch_size+1):
        for index, (input_batch, target_batch, intent_batch) in enumerate(train_dataloader):
            input_batch = input_batch.long().to(device)
            target_batch = target_batch.long().to(device)
            intent_batch = intent_batch.to(device)

            model_optim.zero_grad()

            slot_scores, intent_score = model(input_batch)
            loss = slot_loss(slot_scores.permute(0, 2, 1), target_batch) + intent_loss(intent_score, intent_batch)
            loss.backward()

            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)

            model_optim.step()
            print(f"epoch: {epoch} batch: {index} loss: {loss.item():.2f} slot acc: {slot_acc:.2f} intent acc: {intent_acc:.2f}")

        for index, (input_batch, target_batch, intent_batch) in enumerate(validate_dataloader):
            input_batch = input_batch.long().to(device)

            with torch.no_grad():
                slot_scores, intent_score = model(input_batch)
                _, max_slot_index = slot_scores.max(-1)
                val_slot_acc(target_batch, max_slot_index.detach().cpu())

                _, max_intent_index = intent_score.max(-1)
                val_intent_acc(intent_batch, max_intent_index.detach().cpu())

        slot_acc = val_slot_acc.compute()
        intent_acc = val_intent_acc.compute()

        val_slot_acc.reset()
        val_intent_acc.reset()

        if epoch % 5 == 0 and slot_acc > 0.98 and intent_acc > 0.98:
            model_path = f"{save_dir}/model.pt"
            torch.save(model, model_path)
            print(f"save model in {model_path}...")

    print("train complete!")


if __name__ == '__main__':
    train_config = read_config("./config/guotie.yaml")
    train(train_config)
