FROM python:3.6.7

RUN mkdir -p /usr/src/app  && \
    mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple  && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /usr/src/app

ENV FLASK_ENV develop
CMD ["/usr/local/bin/gunicorn", "-c", "App/config/gunicorn.conf.py", "manager:app"]
