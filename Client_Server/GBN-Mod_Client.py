# Go-Back-N Modified Demo
# Author : Ramaguru Radhakrishnan
# Description : GBN Modified 
# Assignment : 21CS637 - Advanced Networks
# execute as "python GBN-Mod_Client.py"

import time, socket, sys
import random

# Constants
sleepTimer = 1
port = 9001
bufferSize = 1024
verbose = 1
debug = 1

# Global Variables
name = ""
host = ""

# Program Header
print("\n\t\t#################################\n")
print("\t\t\tGo-Back-N Modified Demo\t\t\n")
print("\t\t#################################\n")
time.sleep(sleepTimer)

# Socker Definition and Connection
client = socket.socket()
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print("Server Address: ",ip,"\n")

# Ask the user for Demo Mode
typeRun = int(input(str("\nEnter your 1 for Simulation Demo, 2 for Interactive Demo: ")))

# Set the parameters based on user selection
if(typeRun == 1):
    host = ip
    name = "Ramya"
    print("\nDetails for Interactive Demo will be host \"",ip,"\" with username", name);
if(typeRun == 2):
    host = input(str("\nEnter server address: "))
    name = input(str("\nEnter your name: "))

print("\nTrying to connect to ", host, "(", port, ")... Please wait...\n")
time.sleep(sleepTimer)
client.connect((host, port))
print("Connected :)\n")

client.send(name.encode())
s_name = client.recv(bufferSize).decode()
print(s_name," has joined.\n")

print("\n************************* Receiving the Message ********************************")

# Start the loop
while True:
    originalMsg = client.recv(bufferSize).decode()
    length = int(client.recv(bufferSize).decode())
    ackCounter = 0
    msgToBeSent = ""
    message = ""
    conMsg = ""
    
    while ackCounter!=length:
       # Randomly Select the message acceptance [0 - LOST, 1 - RECEIVED]
       randSelect = random.randint(0,1)
       # verbose message
       if(verbose==1):
          print("--------------------------------------------------------------------------")
          print("\nVERBOSE:- Acknowledgement Counter:", ackCounter)
       # debug message
       if(debug==1):
          print("\nDEBUG:- Random:", randSelect)
        
       # Send ACK LOST
       if(randSelect==0):
          msgToBeSent = "ACK Lost"
          message = client.recv(bufferSize).decode()
          if(debug==1):
            print("\nDEBUG:- Received bit:", message)
          client.send(msgToBeSent.encode())
       # Send ACK #
       elif(randSelect==1):
          msgToBeSent = "ACK "+ str(ackCounter)
          message = client.recv(bufferSize).decode()
          if(debug==1):
            print("\nDEBUG:- Received bit:", message)
          client.send(msgToBeSent.encode())
          # Construct the Binary Message
          conMsg += message
          # Increment the Acknowledgement Counter
          ackCounter += 1
          
    print("\nReceived Message from Server :", originalMsg, " and Reconstructed Binary Data : ", conMsg)
   
