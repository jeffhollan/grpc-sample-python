import grpc

# import the generated classes
from protos import greet_pb2
from protos import greet_pb2_grpc

import os
import logging
import flask
from flask import request, jsonify
from flask import json
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)
CORS(app)

# initialize the gRPC channel
channel = grpc.insecure_channel('localhost:50051')
greeter = greet_pb2_grpc.GreeterStub(channel)

@app.route('/hello', methods=['GET'])
def getOrder():
    app.logger.info('order service called')
    helloRequest = greet_pb2.HelloRequest(name='Azure Container Apps')
    response = greeter.SayHello(helloRequest)
    return response.message

app.run(host='0.0.0.0', port=os.getenv('PORT', '8050'))