FROM python:3

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y netcat default-libmysqlclient-dev \
    # install netcat just in case
    && useradd -U -m -l -s /bin/bash app
    # create an app user
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/static_root \
    && mkdir -p $APP_HOME/media_root
    # create file directives

WORKDIR $APP_HOME
COPY requirements.txt .

# 若网络环境位于国内，pip 默认源难以使用，
# 则注释掉以下第一行，再启用第二行即可
RUN pip install -r requirements.txt
# RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .
RUN chown -R app:app .


USER app:app

# CMD gunicorn campuscats.wsgi -c /run/secrets/gunicorn.conf.py

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
