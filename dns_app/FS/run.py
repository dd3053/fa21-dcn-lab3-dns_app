from flask import Flask,abort,request
import requests,socket
import json
from socket import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/register',methods = ['GET','PUT'])
def registerUser():
    ServerDetails = {
        "hostname" : request.args.get('hostname'),
        "ip" : request.args.get('ip'),
        "as_ip" : request.args.get('as_ip'),
        "as_port" : request.args.get('as_port')
    }
    return registerToAuthorativeServer(ServerDetails)

def registerToAuthorativeServer(ServerDetails):
    serverName = ServerDetails["as_ip"]
    serverPort = ServerDetails["as_port"]
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    message = {
        "type" : "A",
        "Name" : str(ServerDetails['hostname']),
        "Value" : str(ServerDetails['ip']),
        "TTL" : 10
    }
    app_json = json.dumps(message)
    print(app_json)
    clientSocket.sendto(app_json.encode(),(serverName,int(serverPort)))
    print("I am here")
    response, serverAddress = clientSocket.recvfrom(2048)
    clientSocket.close()
    print("Got the response")
    response = response.decode()
    print(response)
    return "Registration Done ",response

@app.route('/fibonacci')
def calculateFib():
    print(request.args)
    num = request.args.get('number')
    if not num.isnumeric() :
        abort(400)

    return str(calculateFib(int(num))), 200

def calculateFib(n):
    fib = []
    fib.append(0)
    fib.append(1)
    for i in range(2,n+1):
        fib.append(fib[i-1]+fib[i-2])
    return fib[n]

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
