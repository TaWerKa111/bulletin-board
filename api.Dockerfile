FROM python:3.11

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY contrib/docker-entripoin.sh docker-entrypoint.sh
RUN se -eux; chmod 0777 docker-entrypoint.sh

COPY ./ /app/

ENTRYPOINT ["/docker-entripoint.sh"]
