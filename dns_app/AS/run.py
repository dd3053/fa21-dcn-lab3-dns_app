import socket
import os
import json
from socket import *

#if os.path.exists("DNSDatabase.txt"):
#    os.remove("DNSDatabase.txt")
#myfile = open("DNSDatabase.txt","w")
#myfile.close()


serverPort = 53533
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print("Going i While Loop")
while True:
    message =""
    print("Listening.................")
    message,clientAddress = serverSocket.recvfrom(2048)
    print("Got the Message")
    message = message.decode()
    print(message)
    message = json.loads(message)
    print(message)
    if len(message) ==2 :
        #DNSQuery Part
        with open('DNSDatabase.json') as f:
            myMap = json.load(f)
        print(myMap)
        message = myMap[message["Name"]]
        print("Message : ",message)
        message = json.dumps(message)
        serverSocket.sendto(message.encode(),clientAddress)
    elif len(message) ==4 :
        #DNS Registration
        #Append the contents to the file
        myfile = open("DNSDatabase.json","w")
        newDict = {
            message["Name"] : message
        }
        message = json.dumps(newDict)
        myfile.write(message)
        myfile.close()
        serverSocket.sendto(str(201).encode(),clientAddress)
    else :
        print("Incorrect Message")