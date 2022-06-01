import os
import random
from socket import *
import struct

serverPort = 2121
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen(5)
connectionSocket , addr = serverSocket.accept()
print('The server is ready to receive')
application_path = os.getcwd()

def HELP():
    connectionSocket.send(("\nHELP\n\n1.HELP              View Command List\n2.LIST              List of Files and size of each File\n3.DWLD FileName     Download filepath from Server\n4.PWD               Show our current location on the server\n5.CD DirName        Open the DirName Folder").encode())
    print("Sent HELP")



def LIST():
    listOfFile = os.listdir(os.getcwd())
    sentence=""
    ListSize=0
    for i in range(len(listOfFile)):
        if os.path.isdir(listOfFile[i]):
            sentence +="> "+ str(listOfFile[i])+"\n"
        else:
            sentence +="  "+ str(listOfFile[i])+" "+str(os.path.getsize(listOfFile[i]))+"\n"
        ListSize += os.path.getsize(listOfFile[i])
        
    connectionSocket.send((sentence+str(ListSize)).encode())
    print("Sent LIST")


def DWLD():
    randomPort=random.randint(3000,50000)
    connectionSocket.send(struct.pack("i", randomPort))
    connectionSocket.recv(1024)
    newSocket=socket(AF_INET, SOCK_STREAM)
    newSocket.connect(('127.0.0.1',randomPort))
    file_name_length = struct.unpack("h", newSocket.recv(2))[0]
    file_name = newSocket.recv(file_name_length).decode()
    print(file_name)
    if (os.path.isfile(file_name) and file_name.upper()!="SERVER.PY"):
        newSocket.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        print("File name not valid")
        newSocket.send(struct.pack("i", -1))
        newSocket.close()
        return
    newSocket.recv(1024)
    print("Sending file...")
    content = open(file_name, "rb")
    l = content.read(os.path.getsize(file_name))
    newSocket.send(l)    
    content.close()
    print("Sent DWLD")



def PWD():
    PathFile = os.getcwd()
    connectionSocket.send(str(PathFile).encode())
    print("Sent PWD")


def CD(path2):
    if os.path.isdir(path2):
        before = os.getcwd()
        os.chdir(path2)
        if not os.getcwd().startswith(application_path):
            os.chdir(before)
            connectionSocket.send("There is no going back!".encode())

        else:
            connectionSocket.send("Folder successfuly changed.".encode())
    else:
        connectionSocket.send("This folder does not exist in the current directory!".encode()) 
    print("Sent CD")

    



while True:
    dastor = connectionSocket.recv(1024).decode().split()
    if dastor[0] == "HELP":
        HELP()
    elif dastor[0] == "LIST":
        LIST()
    elif dastor[0] == "DWLD":
        DWLD()
    elif dastor[0] == "PWD":
        PWD()
    elif dastor[0] == "CD":
        CD(dastor[1])
    else:
        print ("Command not recognised\nplease try again")
