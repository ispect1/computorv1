FROM alpine

RUN apk update && \
  apk add python3 python3-dev build-base ncurses-dev bash && \
  python3 -m ensurepip && \
  pip3 install readline

COPY . .

CMD bash
