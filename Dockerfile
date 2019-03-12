FROM alpine

WORKDIR /data/web

COPY app/ app/
COPY run.py .
COPY requirements.txt .

EXPOSE 8100

# Setup
RUN apk update \
    && apk upgrade \
    && apk add --update python2 py2-pip

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "run.py"]