# 构建bot镜像

FROM 9fevrier/python-ta-lib-pandas


ENV PYTHON_PANDAS_VERSION 0.25.3

WORKDIR /data/bot

COPY . /data/bot

RUN apk add --no-cache --virtual .build-deps \
    musl-dev \
    gcc \
    g++ \
    make \
    && apk add --update libstdc++ \
    && apk add --update  libffi-dev libressl-dev \
    && pip3 install cython \
        pandas==${PYTHON_PANDAS_VERSION} \
    && pip3 install -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /root/.cache \
              /var/cache/apk/* \
              /var/lib/apk/lists/*

WORKDIR /data/bot

CMD python3