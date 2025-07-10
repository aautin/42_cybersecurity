FROM python:3.11-slim

ENV HOME=/home/aautin
RUN mkdir /home/aautin
COPY infection /home/aautin/infection

ENV VIRTUAL_ENV=/WannaCry/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /WannaCry

COPY src/ ./src/
COPY requirements.txt ./requirements.txt
COPY Makefile ./Makefile
COPY key.pub ./key.pub

RUN apt-get update \
    && apt-get install -y make

RUN python3 -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["/bin/bash"]
