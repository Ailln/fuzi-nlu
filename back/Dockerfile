FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-devel

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY ./ /app/

CMD python -m run.server