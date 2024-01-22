FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --upgrade -r /tmp/requirements.txt

COPY ./ /app/
COPY ./contrib/docker-entrypoint.sh /docker-entrypoint.sh
RUN se -eux; chmod 0777 /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
