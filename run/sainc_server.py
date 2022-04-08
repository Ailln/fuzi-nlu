import os

from sanic import Sanic
from socketio import AsyncServer
from cn2an import transform

from run.test import predict
from util.log_util import get_logger
from util.other_util import get_all_data

logger = get_logger(__name__)
sio = AsyncServer(async_mode="sanic", cors_allowed_origins="*")
app = Sanic(name="chatbot")
app.config['CORS_AUTOMATIC_OPTIONS'] = True
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
sio.attach(app)

answer_dict = {
    "greet": "你好～",
    "name": "我叫锅贴。",
    "age": "喵龄一岁不到～",
    "sex": "我是公的！",
    "parents": "Ailln 啊！",
    "feature": "学猫叫，喵～喵～喵～",
    "bye": "886"
}
all_data = get_all_data()


@sio.on("chat-request")
async def index(sid, data):
    logger.info(f"chat-request # question: {data}")
    if ":" in data:
        mode, _msg = data.split(":")
        if mode in ["cn2an", "an2cn"]:
            answer = f"{transform(_msg, mode)}【by {mode}】"
        else:
            intent = predict(data)
            answer = answer_dict[intent]
    else:
        intent = predict(data)
        answer = answer_dict[intent]

    logger.info(f"chat-request # answer: {answer}")
    await sio.emit(event="chat-reply", data=answer, to=sid)


@sio.on("suggest-request")
async def index(sid, data):
    logger.info(f"suggest-request # question: {data}")
    new_list = []
    for line in all_data:
        if data in line:
            new_list.append(line)
            if len(new_list) >= int(os.environ.get("suggestNumber", 5)):
                break

    logger.info(f"suggest-request # suggest_list: {new_list}")
    await sio.emit(event="suggest-reply", data=new_list, to=sid)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
