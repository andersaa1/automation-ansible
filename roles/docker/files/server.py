#!/bin/env python3

from flask import Flask, request, jsonify
import socket
from traceback import format_exc
import os
import time

#https://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-the-currently-running-scrip
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

app = Flask(__name__)

def log_access_to_pesistent_storage():
    try:
        with open(os.path.join(__location__, "persistent_storage/last_access.txt"), "w+") as f:
            time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            f.write(time_string + "\n")
    except FileNotFoundError as e:
        app.logger.error(format_exc())

@app.route("/")
def hello():
    response = "Client IP: " + request.remote_addr + "\nHostname: " + socket.gethostname() + "\n"
    return response, 200

@app.route("/motd")
def message_of_the_day():
    log_access_to_pesistent_storage()

    response = "<h1>The message of the day is:</h1><br>"

    try:
        with open(os.path.join(__location__, "persistent_storage/motd.txt"), "r") as f:
            response += f.read()
    except FileNotFoundError as e:
        response += "No message today"
        app.logger.error(format_exc())


    return response, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)