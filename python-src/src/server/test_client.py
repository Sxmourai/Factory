from src import END_DELIMITER
from threading import Thread
import sys
import socket
class Client:
    def __init__(self, host:str, port:int=9999) -> None:
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        
        initialization = self.sock.recv(4096).decode("utf-8")
        print("Init with", initialization)
    def run(self):
        while True:
            msg = self.sock.recv(2048).decode("utf-8")
            if msg: 
                print(*msg.split(END_DELIMITER))
    def close(self):
        self.sock.close()
    def send(self, msg:str):
        self.sock.send(msg.encode("utf-8"))


client = Client("localhost")

run_thread = Thread(target=client.run)
run_thread.start()
while True:
    cmd = input(">")
    if cmd == "exit":
        client.close()
        sys.exit()
    else:
        exec(cmd)