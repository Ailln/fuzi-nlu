from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

from run.test import predict
from util.log_util import get_logger
from util.data_util import DataUtil
from util.conf_util import get_conf
from util.data_model_util import Question

logger = get_logger(__name__)
app = Sanic(name="fuzi-nlu")
CORS(app)

default_conf = get_conf()
data_util = DataUtil(default_conf)


@app.get("/")
async def index(request):
    return json({
        "status": 1,
        "message": "welcome to fuzi-nlu service, please use /nlu"
    })


@app.post("/nlu")
async def nlu_index(request):
    try:
        msg = Question(**request.json)
        question = msg.question
        logger.info(f"question: {question}")

        intent, confidence = predict(question)
        logger.info(f"intent: {intent}({confidence})")

        data = msg.dict()
        data["intent"] = intent
        data["confidence"] = confidence
        res = {
            "data": data,
            "status": 1,
            "message": "success"
        }
    except Exception as e:
        res = {
            "status": 0,
            "message": str(e)
        }
    return json(res)


@app.get("/questions")
async def get_questions(request):
    try:
        res = {
            "data": data_util.get_all_examples(),
            "status": 1,
            "message": "success"
        }
    except Exception as e:
        res = {
            "status": 0,
            "message": str(e)
        }
    return json(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
