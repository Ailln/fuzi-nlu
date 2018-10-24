# chatbot

基于 PyTorch 的聊天机器人。

## 文档目录

```shell
.
├── back
│   ├── config
│   ├── data
│   ├── model
│   ├── requirements.txt
│   ├── save
│   ├── server.py
│   ├── test.py
│   ├── train.py
│   └── util
├── front
│   ├── babel.config.js
│   ├── package.json
│   ├── public
│   ├── README.md
│   ├── src
│   └── yarn.lock
├── LICENSE
└── README.md

```

## 安装

```shell
git clone https://github.com/kinggreenhall/chatbot.git

# 启动后端
cd chatbot/back
python server.py

# 启动前端
cd ../front
yarn
yarn add vue-cli
yarn serve
```

根据提示访问 http://127.0.0.1:8080 。