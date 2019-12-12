from flask import Flask, request, send_file, send_from_directory, safe_join, abort
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

# The absolute path of the directory containing obj files
# look here: https://pythonise.com/series/learning-flask/sending-files-with-flask
# app.config["CLIENT_IMAGES"] = "<path to objfile"
@app.route("/teddy", methods=["POST"])
def teddy_obj():

    # calling the teddy algorithm
    # vertices = request.form.get("vertices");
    # obj_file = teddy(Vertices);
    # return obj_file;

    html = "<h3>HEllo World!</h3>"
    return html

# def teddy(vertices):
    # teddy algorithm
    # return obj file
    # dirpath = os.getcwd()
    # 
    # return 0
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

