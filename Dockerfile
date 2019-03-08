FROM python:3.6

ENV WD /root

WORKDIR ${WD}

ADD . ${WD}

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    python3 setup.py install && \
    rm -rf ~/.cache/pip

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# Generate configuration files for Jupyter
RUN jupyter notebook --generate-config

# Copy a predefined file to access to Jupyter
# See http://jupyter-notebook.readthedocs.io/en/latest/public_server.html
COPY jupyter_notebook_config.json /root/.jupyter/

EXPOSE 8888