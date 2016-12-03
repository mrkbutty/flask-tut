FROM alpine
RUN apk update && apk upgrade
RUN apk add --update python py-pip

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "/app/app.py", "-p 5000"]
