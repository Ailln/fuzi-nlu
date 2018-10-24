from flask import Flask
from flask_socketio import SocketIO, emit

from test import predict

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@socketio.on("receive")
def recevie_msg(msg):
    print(msg)
    intent = predict(msg)
    answer_dict = {
        "greet": "你好～",
        "name": "我叫锅贴。",
        "age": "喵龄一岁不到～",
        "sex": "我是公的！",
        "parents": "HaveTwoBrush 啊！",
        "feature": "学猫叫，喵～喵～喵～",
        "bye": "886"
    }
    answer = answer_dict[intent]

    with open("./dialog.txt", "a") as f_dialog:
        f_dialog.write(msg+"\t"+answer+"\n")

    emit("response", {"msg": answer})


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8002)
