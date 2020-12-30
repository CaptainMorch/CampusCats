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

ARG PIP_USE_TUNA
RUN pip install -r requirements.txt${PIP_USE_TUNA:+ -i https://pypi.tuna.tsinghua.edu.cn/simple}

COPY . .
RUN chown -R app:app .

USER app:app

CMD ["gunicorn", "campuscats.wsgi", "-c", "./settings/gunicorn.conf.py"]
ENTRYPOINT ["/home/app/web/entrypoint.sh"]