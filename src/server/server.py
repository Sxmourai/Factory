import json
import socket
from time import sleep
from threading import Thread
import sys

from src.server.parser import Parser
from src.server.src import PORT, TILE_CHANGE, PLAYER_MOVEMENT, DISCONNECT
from src.world.build_containers import BuildContainer


class _ServerClient:pass

class Server:
    LOCAL = "localhost"
    def __init__(self, host:str, port:int=None):
        self.host = host
        self.port = port if port else PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        try:
            with open("game.json", "r") as f:
                self.map = json.load(f)
                
                print(self.map)
        except (FileNotFoundError, json.decoder.JSONDecodeError): self.map = {}
        self.clients = []
        self.instructions = []

    def run(self):Thread(target=self._run).start()
    def _run(self):
        Thread(target=self.accept_connections).start()
        while True:
            if self.sock._closed: return
            self.broadcast_instructions()
            sleep(.05)

    def accept_connections(self):
        while True:
            try:
                sock, addr = self.sock.accept()
                print(f"New client at {addr[0]}:{addr[1]}")
                
                addrs = [(client.pseudo,client.pos) for client in self.clients]
                instructs = Parser.create_initialization(self.map,addrs,(0,0))
                print("in",instructs)
                self.send(instructs,sock)
                
                pseudo = Parser.parse_pseudo(sock.recv(512).decode("utf-8"))
                client = ServerClient(sock,addr,(0,0),pseudo)

                self.clients.append(client)
                
                client_thread = Thread(target=self.handle_client, args=(client,))
                client_thread.start()
                self.instructions.append((PLAYER_MOVEMENT, client.pseudo,client.pos))
                
            except OSError:
                return

    def handle_client(self, client:_ServerClient):
        while True:
            try:
                received = client.recv(2048).decode("utf-8")
                move,disconnected,changes = Parser.parse_client(received)
                if disconnected:
                    print(f"Player {client.pseudo} disconnected because {disconnected}")
                    self.instructions.append((DISCONNECT, client.pseudo,disconnected))
                    client.close()
                    self.clients.remove(client)
                    return
                if move:
                    self.instructions.append((PLAYER_MOVEMENT, client.pseudo,move))
                if changes:
                    for pos,build in changes:
                        self.map[pos] = build # build type is str
                        self.instructions.append((TILE_CHANGE, self.map[pos]))

            except (ConnectionAbortedError,ConnectionResetError):
                print(f"Player {client.pseudo} aborted connection.")
                self.instructions.append((DISCONNECT, client.pseudo,"the connection was aborted."))
                client.close()
                self.clients.remove(client)
                return
            except OSError:
                self.clients.remove(client)
                return

    def broadcast_instructions(self):
        if self.instructions:
            outputs = Parser.create_output(self.instructions)
            self.broadcast(outputs)
            self.instructions.clear()

    def broadcast(self,broadcasted:str|bytes):
        if isinstance(broadcasted, str): broadcasted = broadcasted.encode("utf-8")
        for client in self.clients:
            if not client.sock._closed:
                self.send(broadcasted, client)
            else:self.clients.remove(client)

    def send(self, msg:str|bytes, client:_ServerClient|socket.socket):
        if isinstance(msg, str):msg = msg.encode("utf-8")
        try:
            if isinstance(client, socket.socket):
                client.send(msg)
            else:
                client.send(msg)
        except (ConnectionResetError,ConnectionAbortedError,ConnectionRefusedError):
            self.clients.remove(client)
        for client in self.clients:
            if client.sock._closed:
                self.clients.remove(client)
                client.sock.close()


    def exec_input(self, input:str):
        inp = input.lower()
        if inp == "gui":
            assert False, "Not implemented"
        elif inp == "broadcast":
            self.broadcast_instructions()
        elif inp == "clients":
            print(len(self.clients),"=============")
            for client in self.clients:
                print(client.pseudo)
        elif inp == "map":
            print(*self.map.items(), sep=" - ")
        #...

    def exit(self):
        print("Closing sockets...")
        for client in self.clients:
            client.close()
        self.sock.close()
        print("Saving world...")
        with open("game.json", "wb") as f:
            map = {}
            for pos, build in self.map.items():
                map[str(pos)[1:-1]] = build
            c = list(str(map))
            for i,char in enumerate(c):
                if char == "'": c[i] = '"'
                elif char == '"': c[i] = "'"
            f.write(bytes(json.dumps(map), "utf-8"))
        sys.exit()



class ServerClient:
    def __init__(self, sock:socket.socket, addr:str, pos:tuple[int|float,int|float], pseudo:str) -> None:
        self.sock = sock
        self.addr = addr
        self.x,self.y = pos
        self.pseudo = pseudo
        
    @property
    def pos(self):return self.x,self.y
        
    def recv(self, bufsize:int):
        return self.sock.recv(bufsize)
    def send(self, data:str|bytes):
        data = data if isinstance(data,bytes) else data.encode("utf-8")
        return self.sock.send(data)
    def close(self):
        self.sock.close()
    def is_closed(self):
        return self.sock._closed