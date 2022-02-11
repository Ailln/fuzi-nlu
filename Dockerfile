FROM conda/miniconda3

COPY . /chatbot
WORKDIR /chatbot

RUN apt update && apt install -y curl
# fix "OSError: protocol not found"
RUN apt -o Dpkg::Options::="--force-confmiss" install --reinstall -y netbase

RUN cd back && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV NODE_INSTALLER nodesource_setup.sh
RUN curl -sL https://deb.nodesource.com/setup_10.x -o $NODE_INSTALLER
RUN /bin/bash $NODE_INSTALLER && rm $NODE_INSTALLER
RUN apt install -y nodejs
RUN cd front && /usr/bin/npm install --registry=https://registry.npmmirror.com

EXPOSE 8002
EXPOSE 8080
