FROM python:3

ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/home/app/web

RUN apt-get update && apt-get install -y netcat \
    # install netcat just in case
    && useradd -U -m -l -s /bin/bash app \
    # create an app user
    && mkdir -p $APP_HOME/static_root \
    && mkdir -p $APP_HOME/media_root \
    # create file directives

WORKDIR $APP_HOME
COPY requirements.txt $APP_HOME

# 若网络环境位于国内，pip 默认源难以使用，
# 则注释掉以下第一行，再启用第二行即可
RUN pip install -r requirements.txt
# RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . $APP_HOME
RUN chown -R app:app $APP_HOME


USER app:app

CMD gunicorn campuscats.wsgi -c /gunicorn.conf.py

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
