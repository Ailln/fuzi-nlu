# 🤖️ chatbot

[![language](https://img.shields.io/badge/language-Py3.6+-yellow.svg)](https://docs.python.org/3.6/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/HaveTwoBrush/chatbot/blob/master/LICENSE)
[![stars](https://img.shields.io/github/stars/HaveTwoBrush/chatbot.svg)](https://github.com/HaveTwoBrush/chatbot/stargazers)
[![stars](https://img.shields.io/github/forks/HaveTwoBrush/chatbot.svg)](https://github.com/HaveTwoBrush/chatbot/network/members)

基于 PyTorch 的任务型聊天机器人。

## 1 简介

常见的聊天机器人有两种：

1. 闲聊型 `open domain`
2. 任务型 `task oriented`

本项目属于第二种，即面向任务的聊天机器人。这类型机器人的常见应用是智能客服，**目的是为了解决用户的明确需求**。

![flow](src/chatbot-flow.png)

上图为面向任务的聊天机器人的一般流程，该项目目前实现了第一部分的 `NLU` 功能，包含 `Slot Filling` 和 `Intent Prediction`。

## 2 DEMO

![demo](./src/demo-screen-shot.jpg)

> ⚠️ DEMO 中仅包含我编写的几十条训练样本，主要内容是关于我家🐱`锅贴`，这些只发挥了该项目的一部分功能。

[点我立即尝试 DEMO](https://chatbot.dovolopor.com)

## 3 架构

### 2.1 前端

- VueJS
- iView
- SocketIO

### 2. 后端

- Flask
- SocketIO
- PyTorch

> ⚠️ 后端代码基于 [RNN-for-Joint-NLU](https://github.com/applenob/RNN-for-Joint-NLU) 进行了改进。

## 4 安装

```shell
git clone https://github.com/HaveTwoBrush/chatbot.git

# 启动后端
cd chatbot/back
python server.py

# 启动前端
cd ../front
yarn
yarn serve

# 接下来，请根据提示访问网页
```

## 5 目录

```shell
.
├── front #前端
│   ├── babel.config.js
│   ├── package.json
│   ├── public
│   ├── README.md
│   ├── src
│   └── yarn.lock
├── back #后端
│   ├── config
│   ├── data
│   ├── model
│   ├── requirements.txt
│   ├── save
│   ├── server.py
│   ├── test.py
│   ├── train.py
│   └── util
├── src # 资源
├── LICENSE
└── README.md
```

## 6 参考

### 安装

- [如何安装 Node 开发环境？](https://www.v2ai.cn/linux/2018/11/11/LX-10.html)
- [如何安装 python 开发环境？](https://www.v2ai.cn/linux/2018/04/29/LX-2.html)
- [PyTorch 从安装到计算 1+1](https://www.v2ai.cn/dl/2018/08/20/DL-5.html)

### 模型

- [Tensorflow动态seq2seq使用总结（r1.3）](https://github.com/applenob/RNN-for-Joint-NLU/blob/master/tensorflow_dynamic_seq2seq.md)
- [Attention-Based Recurrent Neural Network Models for Joint Intent Detection and Slot Filling](https://arxiv.org/abs/1609.01454)

### 论文

- [Attention-Based Recurrent Neural Network Models for Joint Intent Detection and Slot Filling](https://arxiv.org/abs/1609.01454)
- [BERT for Joint Intent Classification and Slot Filling](https://arxiv.org/pdf/1902.10909.pdf)

## 7 执照

[MIT](./LICENSE)

## 8 交流

请添加微信号：`kinggreenhall`，备注「chatbot」，我邀请你进入交流群。
