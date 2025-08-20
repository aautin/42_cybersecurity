FROM debian:latest

RUN apt update && apt install -y \
    build-essential \
    libpcap-dev \
    gcc \
    valgrind

WORKDIR /inquisitor

COPY . .
RUN rm -f Dockerfile

CMD tail -f