import socket
from time import sleep
from threading import Thread

from src.server.parser import Parser
from src.server.src import PORT
import sys

class Server:
    LOCAL = "localhost"
    def __init__(self, host:str, port:int=None, map:dict={}):
        self.host = host
        self.port = port if port else PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.map = map
        self.clients = []
        self.instructions = []

    def run(self):Thread(target=self._run).start()
    def _run(self): 
        Thread(target=self.accept_connections).start()
        while True:
            if self.sock._closed: return
            self.broadcast_instructions()
            sleep(2)

    def accept_connections(self):
        while True:
            try:
                sock, addr = self.sock.accept()
                print(f"New client at {addr[0]}:{addr[1]}")
                self.initialize_client(sock, (0,0),self.map)
                pseudo = Parser.parse_pseudo(sock.recv(512).decode("utf-8"))
                self.clients.append(ServerClient(sock,addr,(0,0),pseudo))
                client_thread = Thread(target=self.handle_client, args=(sock,))
                client_thread.start()
            except OSError:
                return

    def handle_client(self, client:socket.socket):
        while True:
            try:
                move,disconnected,changes = Parser.parse_client(client.recv(2048).decode("utf-8"))
                if disconnected:
                    print(f"Player {self.get_addr(client)} disconnected because {disconnected}")
                    self.instructions.append((self.get_addr(client),disconnected))
                    client.close()
                    return
                if move:
                    print(self.get_addr(client),"moved at",move)
                    #                        Pseudo of player
                    self.instructions.append((self.get_addr(client),move))
                if changes: assert False, "Not implemented !"
            
            except (ConnectionAbortedError,ConnectionResetError):
                print(f"Player {self.get_addr(client)} aborted connection.")
                self.instructions.append((self.get_addr(client),"the connection was aborted."))
                client.close()
                return



    def broadcast_instructions(self):
        if self.instructions:
            outputs = Parser.create_output(self.instructions).encode("utf-8")
            print("Broadcasting",self.instructions)
            self.broadcast(outputs)
            self.instructions.clear()

    def broadcast(self,broadcasted:str|bytes):
        if isinstance(broadcasted, str): broadcasted = broadcasted.encode("utf-8")
        print("Broadcasting",broadcasted.decode("utf-8"))
        for client in self.socks:
            if not client._closed:
                client.send(broadcasted)
            else:self.remove_client(client)
        

    def initialize_client(self, sock:socket.socket, pos:tuple[float,float]|tuple[int,int],map:dict):
        init_instructions = f"IPos/{pos}|IMap/{map}|"
        sock.send(init_instructions.encode('utf-8'))
        
        
        self.broadcast("|".join(list(f"IPlayers/{addr}" for addr in self.addrs)))

    def exec_input(self, input:str):
        inp = input.lower()
        if inp == "gui":
            assert False, "Not implemented"
        elif inp == "broadcast":
            self.broadcast_instructions()
        #...

    def exit(self):
        print("Closing sockets...")
        for client in self.socks:
            client[0].close()
        self.sock.close()
        print("Exiting...")
        sys.exit()



class ServerClient:
    def __init__(self, sock:socket.socket, addr:str, pos:tuple[int|float,int|float], pseudo:str) -> None:
        self.sock = sock
        self.addr = addr
        self.x,self.y = pos
        self.pseudo = pseudo