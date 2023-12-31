from socket import *
from random import randint
import json
import threading


def isdigit(num): 
    try:
        int(num)
        return True
    except ValueError:
        return False

class Submission:
    def __init__(self, action, num1, num2, answer=0): # constructor, sets answer to 0 by default
        self.action = action
        self.num1 = num1
        self.num2 = num2
        self.answer = answer
    

def handle_client(connectionSocket, address):
    print("Connection from:", address)

    ClientJSON = connectionSocket.recv(1024).decode()
    
    ClientDict = json.loads(ClientJSON)
    
    actionRecv = ClientDict["action"]
    num1recv = ClientDict["num1"]
    num2recv = ClientDict["num2"]
    answer = ClientDict["answer"]
   
    if isdigit(num1recv) == False:
        num1 = float(num1recv)
    else:
        num1 = int(num1recv)

    if isdigit(num2recv) == False:
        num2 = float(num2recv)
    else:
        num2 = int(num2recv)
    
    action = str(actionRecv)
    
    print("Received:", action, num1, num2)

    def calculate(num1, num2, action):
        
        if action.lower() == "random": 
            if num1 > num2:
                calc = randint(num2, num1) # Random number between num2 and num1
                return Submission(action, num2, num1, calc)
            else:
                calc = randint(num1, num2) # Random number between num1 and num2
                return Submission(action, num1, num2, calc)
        
        elif action.lower() == "add":
            calc = num1 + num2
            return Submission(action, num1, num2, calc)
        
        elif action.lower() == "subtract":
            calc = num1 - num2
            return Submission(action, num1, num2, calc)
        else:
            return Submission(action, num1, num2, "Invalid action")

    result = json.dumps(calculate(num1, num2, action).__dict__)
    print("Sending:", result)
    connectionSocket.send(result.encode())
    connectionSocket.close()

def runserver():
    serverPort = 12000  # Port number
    serverHost = '127.0.0.1'  # Host name

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((serverHost, serverPort))
    serverSocket.listen(5)  # Allow up to 5 simultaneous connections
    print("The server is ready to receive")

    while True:
        connectionSocket, address = serverSocket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, address))
        client_thread.start()

if __name__ == "__main__":
    runserver()
