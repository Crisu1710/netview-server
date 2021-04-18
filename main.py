#!/usr/bin/env python3

# source from: https://royportas.com/posts/2019-03-02-cors-python/

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from json import dumps
# import os

port = 8090  # int(os.environ["VUE_APP_API_PORT"])

""" The HTTP request handler """


class RequestHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS,PUT,DELETE")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")
        self.send_header("Content-Type", "application/json")

    def send_dict_response(self, d):
        """ Sends a dictionary (JSON) back to the client """
        self.wfile.write(bytes(dumps(d), "utf8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

        path = self.path.split('/')
        filename = "conf/" + path[1] + ".json"

        with open(filename) as file:
            file = json.load(file)
        response = file

        self.send_dict_response(response)

    def do_PUT(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        dataLength = int(self.headers["Content-Length"])
        data = self.rfile.read(dataLength)

        response = {}
        response["status"] = "OK"
        self.send_dict_response(response)

        update(data.decode(), self.path)

    def do_DELETE(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response = {}
        response["status"] = "OK"
        self.send_dict_response(response)

        delete(self.path)

    def do_POST(self):
        self.send_response(200)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        dataLength = int(self.headers["Content-Length"])
        data = self.rfile.read(dataLength)

        response = {}
        response["status"] = "OK"
        self.send_dict_response(response)

        create(data, self.path)


def create(data, path):
    path = path.split('/')
    filename = "conf/" + path[1] + ".json"

    file = open(filename, 'r')
    ln = len(open(filename, 'r').readlines())
    original_text = file.read()
    original_text = original_text.replace('[', '')
    file.close()
    file = open(filename, "wb")
    if ln == 3:
        file.write("[ \n".encode() + data + original_text.encode())
    else:
        file.write("[ \n".encode() + data + ",".encode() + original_text.encode())
    file.close()


def update(data, path):
    store = []
    path = path.split('/')
    update_id = path[2]
    filename = "conf/" + path[1] + ".json"

    lines = []
    with open(filename) as file:
        db = json.load(file)
        lines.append(db)

    for line in lines:
        for x in line:
            ids = str(x['id'])
            if ids != update_id:
                x = str(x)
                x = x.replace("'", '"')
                store.append(x)

        file = open(filename, "w")
        store.append(data)
        store = str(store)
        store = store.replace("'", "")
        store = store.replace("[", "[\n")
        store = store.replace("},", "},\n")
        store = store.replace(" ", "")
        store = store.replace("]", "\n\n]")
        file.write(store)


def delete(data):
    store = []
    data = data.split("/")
    filename = "conf/" + data[1] + ".json"
    del_id = data[2]

    lines = []
    with open(filename) as file:
        db = json.load(file)
        lines.append(db)

    for line in lines:
        for x in line:
            ids = str(x['id'])
            if ids != del_id:
                x = str(x)
                x = x.replace("'", '"')
                store.append(x)

        file = open(filename, "w")
        store = str(store)
        store = store.replace("'", "")
        store = store.replace("[", "[\n")
        store = store.replace("},", "},\n")
        store = store.replace(" ", "")
        store = store.replace("]", "\n]")
        file.write(store)


print("Starting server")
httpd = HTTPServer(("0.0.0.0", port), RequestHandler)  # TODO ip
print("Hosting server on port " + str(port))
httpd.serve_forever()
