FROM python:3.6

ENV WD /root

WORKDIR ${WD}

ADD . ${WD}

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    python3 setup.py install && \
    rm -rf ~/.cache/pip
