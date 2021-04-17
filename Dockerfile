FROM python:3

WORKDIR /api
COPY . .
EXPOSE 8090
CMD [ "python", "./main.py" ]