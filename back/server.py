from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, engineio_logger=True)

@socketio.on("receive")
def recevie_msg(msg):
    print(msg)
    emit("response",{"msg": msg+"，真的吗？"})

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=3000)
