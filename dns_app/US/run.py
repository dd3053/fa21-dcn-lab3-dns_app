from flask import Flask,request,abort
import requests
import socket
import json
from socket import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/fibonacci')
def readRequest():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    sequence_number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')
    

    if hostname is None:
        abort(400)
    if fs_port is None:
        abort(400)
    if sequence_number is None:
        abort(400)
    if as_ip is None:
        abort(400)
    if as_port is None:
        abort(400)
    

    clientSocket = socket(AF_INET,SOCK_DGRAM)
    message = {
    "Name" : hostname,
    "Type" : "A"
    }
    message = json.dumps(message)
    clientSocket.sendto(message.encode(),(as_ip,int(as_port)))
    result,server = clientSocket.recvfrom(2048)
    result = result.decode()
    print(result)
    result = json.loads(result)
    #Create a GET Request
    url = "http://"+result["Value"]+":"+fs_port+"/fibonacci?"+"number="+sequence_number
    print(url)
    response = requests.get(url)
    print(response.text)
    return response.text
    
app.run(host='0.0.0.0',
        port=8080,
        debug=True)
