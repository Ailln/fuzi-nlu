# Chatbot 🤖️

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

> ⚠️ DEMO 中仅包含我编写的几十条训练样本（在 `back/data/train.json`），主要内容是关于我家🐱`锅贴`，这些只发挥了该项目的一部分功能。

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

## 4 运行

### 4.1 直接运行

```shell
# 1 下载文件
git clone https://github.com/Ailln/chatbot.git

# 2 启动后端
cd chatbot/back
# 安装依赖
pip install -r requirements.txt
# 运行
python server.py

# 3 启动前端
cd ../front
# 安装依赖
yarn
# 运行
yarn serve

# 4 接下来，根据提示访问网页即可
```

### 4.2 以 docker 方式运行

```shell
# 1 下载文件
git clone https://github.com/Ailln/chatbot.git

# 2 构建镜像（这一步可能会因为网络问题出错，可以多尝试几次）
cd chatbot && docker image build -t chatbot .

# 3 运行
docker run -p 8080:8080 -p 8002:8002 -it chatbot /bin/bash

cd /chatbot/back && python server.py &
cd /chatbot/front && npm run serve
```

## 5 目录

```shell
.
├── front #前端
│   ├── public
│   ├── src
│   ├── babel.config.js
│   ├── package.json
│   └── yarn.lock
├── back #后端
│   ├── config
│   ├── data
│   ├── model
│   ├── util
│   ├── save
│   ├── server.py
│   ├── test.py
│   ├── train.py
│   └── requirements.txt
├── src # 资源
├── LICENSE
├── README.md
└── .gitignore
```

## 6 参考

- [Tensorflow动态seq2seq使用总结（r1.3）](https://github.com/applenob/RNN-for-Joint-NLU/blob/master/tensorflow_dynamic_seq2seq.md)
- [Attention-Based Recurrent Neural Network Models for Joint Intent Detection and Slot Filling](https://arxiv.org/abs/1609.01454)
- [BERT for Joint Intent Classification and Slot Filling](https://arxiv.org/pdf/1902.10909.pdf)
- [从“连接”到“交互”—阿里巴巴智能对话交互实践及思考](https://yq.aliyun.com/articles/144035)

## 7 许可证

[![](https://award.dovolopor.com?lt=License&rt=MIT&rbc=green)](./LICENSE)

## 8 交流

请添加微信号：`kinggreenhall`，备注「chatbot」，我邀请你进入交流群。
