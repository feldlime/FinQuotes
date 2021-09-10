# syntax=docker/dockerfile:experimental
FROM python:3.7-slim

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apt-get update && apt-get install gcc -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# setup timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# add app
COPY project /usr/src/app/project
COPY ./gunicorn.conf.py /usr/src/app
COPY ./main.py /usr/src/app

EXPOSE 5000

# run server
CMD ["/usr/src/app/entrypoint.sh"]
