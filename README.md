# Chatbot

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Ailln/chatbot/blob/master/LICENSE)
[![stars](https://img.shields.io/github/stars/Ailln/chatbot.svg)](https://github.com/Ailln/chatbot/stargazers)
[![stars](https://img.shields.io/github/forks/Ailln/chatbot.svg)](https://github.com/Ailln/chatbot/network/members)

🤖️ 基于 PyTorch 的任务型聊天机器人。

## 1 简介

常见的聊天机器人有两种：

1. 闲聊型 `open domain`
2. 任务型 `task oriented`

本项目属于第二种，即面向任务的聊天机器人。这类型机器人的常见应用是智能客服，**目的是为了解决用户的明确需求**。

![flow](src/chatbot-flow.png)

上图为面向任务的聊天机器人的一般流程，该项目目前实现了第一部分的 `NLU` 功能，包含 `Slot Filling` 和 `Intent Prediction`。

## 2 DEMO

![demo](./src/demo-screen-shot.jpg)

[点我立即尝试 DEMO](https://chatbot.dovolopor.com)

### 2.1 数据集

1. `guotie`：这份数据集的主要内容是关于我家🐱`锅贴`，只使用了意图识别的功能。
2. `weather`: 在 Github 上找到的一份关于天气的 [中文公开数据集](https://github.com/howl-anderson/NLU_benchmark_dataset/tree/master/dataset/dialogflow/weather/rasa_format) 。
3. `fewjoint`: [SMP2020](https://atmahou.github.io/attachments/FewJoint.zip)

### 2.2 数据标注

这里使用 RASA 开源的标注工具 [RASA-NLU-Trainer](https://github.com/RasaHQ/rasa-nlu-trainer) 进行标注。

标注完成后需要进行格式转化才能使用，这里以 `/back/data/guotie.json` 为例：

```bash
pip install rasa==2.6.3

cd ./back/data
mkdir guotie

# rasa 暂时不支持从 json 直接转成 yaml，因此需要先转 md，再转 yaml
rasa data convert nlu -f md --data guotie.json --out ./guotie/nlu.md
rasa data convert nlu -f yaml --data ./guotie/nlu.md --out ./guotie/

rm ./guotie/nlu.md
mv ./guotie/nlu_converted.yml ./guotie/nlu.yml

# 生成 domain
python -m run.generate_domain_from_nlu --nlu ./data/guotie/nlu.yml --domain ./data/guotie/domain.yml
```

## 3 运行

### 3.1 直接运行

```shell
# 1 下载文件
git clone https://github.com/Ailln/chatbot.git

# 2 启动后端
cd chatbot/back
# 安装依赖
pip install -r requirements.txt
# 运行
python -m run.server

# 3 启动前端
cd ../front
# 安装依赖
npm install
# 运行
npm run serve
# 在浏览器中打开 http://127.0.0.1:8080
```

### 3.2 以 docker 方式运行

```shell
# 1 下载文件
git clone https://github.com/Ailln/chatbot.git

# 2 运行后端
cd chatbot/back
docker build -t chatbot-back:1.0.0 .
docker run -d --restart=always --name chatbot-back -p 8002:8002 chatbot-back:1.0.0
docker logs -f chatbot-back

# 2 运行前端
cd ../front
docker build -t chatbot-front:1.0.0 .
docker run -d --restart=always --name chatbot-front -p 8080:80 chatbot-front:1.0.0
docker logs -f chatbot-front
# 在浏览器中打开 http://127.0.0.1:8080
```

### 3.3 重新训练模型
```bash
cd chatbot/back
# 训练
python -m run.train

# 测试
python -m run.test
```

## 4 架构

### 4.1 前端

- VueJS
- iView
- SocketIO

### 4.2 后端

- Flask
- SocketIO
- PyTorch

## 5 目录

```
.
├── front # 前端
│     ├── public
│     ├── src
│     ├── babel.config.js
│     ├── Dockerfile
│     ├── .dockerignore
│     ├── package.json
│     └── package-lock.json
├── back # 后端
│     ├── config
│     ├── data
│     ├── model
│     ├── util
│     ├── save
│     ├── qps_test.py
│     ├── Dockerfile
│     ├── .dockerignore
│     └── requirements.txt
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
- [A Frustratingly Easy Approach for Joint Entity and Relation Extraction](https://arxiv.org/pdf/2010.12812.pdf)
- [FewJoint: A Few-shot Learning Benchmark for Joint Language Understanding](https://arxiv.org/abs/2009.08138)

## 7 许可证

[![](https://award.dovolopor.com?lt=License&rt=MIT&rbc=green)](./LICENSE)
[![](https://award.dovolopor.com?lt=Ailln's&rt=idea&lbc=lightgray&rbc=red&ltc=red)](https://github.com/Ailln/award)

## 8 交流

请添加微信号：`Ailln_`，备注「chatbot」，我邀请你进入交流群。
