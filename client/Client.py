from socket import *
import struct
import sys

serverName = "127.0.0.1"
serverPort = 2121
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))



def DWLD(file_name):   
    clientSocket.send(("DWLD"+" "+file_name).encode())
    try:
        port=struct.unpack("i", clientSocket.recv(1024))[0]
        newSocket=socket(AF_INET, SOCK_STREAM)
        newSocket.bind((serverName, port))
        newSocket.listen(5)
        clientSocket.send("1".encode())
        newConnectionSocket, addr2=newSocket.accept()
        newConnectionSocket.send(struct.pack("h", sys.getsizeof(file_name)))
        newConnectionSocket.send(file_name.encode())
        file_size = struct.unpack("i", newConnectionSocket.recv(4))[0]
        if file_size == -1:
            print("File does not exist. Make sure the name was entered correctly")
            newConnectionSocket.close()
            newSocket.close()
            return
    except:
        print("Error checking file")
    newConnectionSocket.send("1".encode())
    output_file = open(file_name, "wb")
    
    print("Downloading...")
    
    l = newConnectionSocket.recv(file_size)
    output_file.write(l)
    print("Download completed")
    output_file.close()




def CD(path):
    clientSocket.send(("CD"+" "+path).encode())
    message=clientSocket.recv(1024).decode()
    print(message)





while True:
    sentence = input("Input Sentence : ").split()

    if sentence[0].upper()=="DWLD":
        if len(sentence)==2:
            DWLD(sentence[1])
        else:
            print("BAD REQUEST!")

    elif sentence[0].upper()=="CD":
        if len(sentence)==2:
            CD(sentence[1])
        else:
            print("BAD REQUEST!")

    elif sentence[0].upper() == "HELP" or sentence[0].upper() == "LIST" or sentence[0].upper() == "PWD":
        if len(sentence)==1:
            clientSocket.send(sentence[0].upper().encode())
            modifiedSentence = clientSocket.recv(1024)
            print("\n" + modifiedSentence.decode() + "\n")
        else:
            print("BAD REQUEST!")
        
    else:
        print("BAD REQUEST!")

