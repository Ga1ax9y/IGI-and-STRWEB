FROM python:alpine

WORKDIR /app

COPY square.py /app/
COPY circle.py /app/
COPY script.py /app/

ENV SIZE=10

CMD [ "python","-u","script.py" ]
