import socket
from src.world.world import Map
from src.ressources import load
from src.multiplayer.src import *
from threading import Thread
import pygame


class Server:
    def __init__(self, host:str, port:int=9999, map:dict={}):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.listen((self.host, self.port))
        self.map = Map()
        map = map if map else self.get_map()
        self.map.load_map(map)
        self.clients = []

    def run(self):
        Thread(target=self.accept_connections)
        while True:
            for client in self.clients:
                client.run()
                self.send_outputs(client)

    def send_outputs(self, client):
        outputs = "|".join(self.instructions)
        client.send(outputs)

    def accept_connections(self):
        while True:
            self.handle_connect(*self.sock.accept())
    
    def handle_connect(self, sock:socket.socket, addr:str):
        client = _Client(self, sock, addr)
        client.initialize(self.map, self.clients, (0,0))
    
    def exit(self):
        GameSave
        with open('output.json', 'w') as f:
            json.dump(self., f)
        exit()



class Player:
    def __init__(self, client, pos:tuple[float,float], order:int) -> None:
        self.img = load("player.png")
        # TODO CHANGE HUE FROM ORDER
        self.surf = self.img

        self._x,self._y = pos
        self.client = client

    def move(self, new_x_or_pos:float|tuple[float,float], new_y:float=None):
        if isinstance(new_x_or_pos, tuple):
            self.pos = new_x_or_pos
        else:
            assert new_y, "You must set a new y if new_x_or_pos isn't a tuple !"
            self.x = new_x_or_pos
            self.y = new_y

    def draw(self, camera):
        camera.render(self.surf, self.pos)

    @property
    def x(self):return self._x
    @property
    def y(self):return self._y
    @property
    def pos(self):return self._x,self._y
    @x.setter
    def x(self, new_x:float):self._x = new_x
    @y.setter
    def y(self, new_y:float):self._y = new_y
    @pos.setter
    def pos(self, new_pos:tuple[float,float]):self._x,self._y = new_pos


class _Client:
    def __init__(self, server:Server, sock:socket.socket, addr) -> None:
        self.sock = sock
        self.addr = addr
        self.player = None
        self.server = server

    def initialize(self, map, clients:list, pos:tuple[float,float]):
        self.player = Player(self, len(clients), pos)
        self.send(f"{MAP_INITIALISATION}{map}")
        
    def run(self):
        self.handle_inputs()
        
    def handle_inputs(self):
        # Getting inputs from client (serverside)
        inputs = self.sock.recv(1024).decode('utf-8')
        # Parsing inputs
        instructions = inputs.split("|")
        for instruction in instructions:
            mode = instruction[0]
            if mode == PLAYER_MOVEMENT:
                new_x, new_y = command[1:].split(",")
                self.player.move(new_x,new_y)
                self.server.player_move()
            elif mode == TILE_CHANGE:
                index_of_marker = command.index("-")
                pos = command[1:index_of_marker].split(",")
                build = self.parse_building(command[index_of_marker+1:])
                self.server.build(pos, build)

    def send(self, outputs):
        self.sock.send(outputs.encode('utf-8'))
