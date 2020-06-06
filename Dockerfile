FROM ubuntu:16.04

COPY . /chatbot
WORKDIR /chatbot

RUN apt update && apt install -y curl
# fix "OSError: protocol not found"
RUN apt -o Dpkg::Options::="--force-confmiss" install --reinstall -y netbase

ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
ENV CONDA_INSTALLER Miniconda3-py37_4.8.2-Linux-x86_64.sh
RUN curl -O https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh
RUN mkdir -p $CONDA_DIR && /bin/bash $CONDA_INSTALLER -f -b -p $CONDA_DIR && rm $CONDA_INSTALLER
RUN cd back && /opt/conda/bin/pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENV NODE_INSTALLER nodesource_setup.sh
RUN curl -sL https://deb.nodesource.com/setup_10.x -o $NODE_INSTALLER
RUN /bin/bash $NODE_INSTALLER && rm $NODE_INSTALLER
RUN apt install -y nodejs
RUN cd front && /usr/bin/npm install --registry=https://registry.npm.taobao.org

EXPOSE 8002
EXPOSE 8080
