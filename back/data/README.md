# 数据

## 1 格式

举例：
```json
 {
    "text": "我想找一个光谷附近的酒店",
    "intent": "restaurant_search",
    "entities": [
      {
        "start": 5,
        "end": 7,
        "value": "光谷",
        "entity": "location"
      }
    ]
  }
```

## 2 标注

数据标注使用了 RASA 开源的标注工具 [RASA-NLU-Trainer](https://github.com/RasaHQ/rasa-nlu-trainer)，我把它部署在了自己服务器上，点击[这里](https://rasa.dovolopor.com)可以免费使用。