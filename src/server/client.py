import socket
from socket import AF_INET, SOCK_STREAM
from src.graphical.player import Player
from src.server.server import Server
from src.server.parser import Parser
from time import sleep
from threading import Thread
from random import sample

class Client:
    def __init__(self, app) -> None:
        self.app = app
        self.connected = False
    
    def construct(self, building):
        self.sock.send(Parser.build_change_create(building).encode("utf-8"))
    
    def connect_to_server(self, server_ip:str):
        try:
            self.sock = socket.socket(AF_INET, SOCK_STREAM)
            print("Connecting...")
            self.sock.connect(Parser.parse_ip(server_ip))
        except (ConnectionRefusedError, socket.gaierror):return
        print("Getting the initialization")
        while True:
            init_instructions = self.sock.recv(2048).decode("utf-8")
            if init_instructions:break
        print("Parse",init_instructions)
        self.app.game.map.start()
        players_move, self_pos = Parser.parse_initialization(init_instructions)

        if self_pos:
            if self.app.game.camera.player:
                self.app.game.camera.player.pos = self_pos
            else:
                self.app.game.camera.player = Player(self_pos, "".join(sample("abcdefghijklmnopqrstuvwxyz",10)))
        
        self.sock.send(Parser.create_pseudo(self.app.game.camera.player.pseudo).encode("utf-8"))
        self.app.game.camera.move_players(players_move)
        self.app.start()
        self.connected = True
        Thread(target=self.get_instructions).start()
        self.last_pos_player = self.app.game.camera.player.pos
        self.last_map = self.app.game.map.map
        Thread(target=self.send_instructions).start()

    def get_instructions(self):
        while True:
            if not self.connected:return
            try:
                raw_instructions = self.sock.recv(1024).decode('utf-8')
                if Parser.should_disconnect(raw_instructions, self.sock.getsockname()):self.disconnect();return
                disconnected_players,players_movements = Parser.parse_server(raw_instructions)

                self.app.game.camera.disconnect_players(disconnected_players)
                self.app.game.camera.move_players(players_movements)
            except (ConnectionResetError, ConnectionAbortedError):
                self.disconnect()
                return

    def send_instructions(self):
        while True:
            if not self.connected:return
            player_cond = self.last_pos_player != self.app.game.camera.player.pos
            build_cond = self.last_map != self.app.game.map.map
            if player_cond:
                self.sock.send(Parser.create_move_instruct(self.app.game.camera.player.pos))
                self.last_pos_player = self.app.game.camera.player.pos
            elif build_cond:
                print("sending !")
                self.last_map = self.app.game.map.map
            sleep(.01)

    def disconnect(self):
        try:
            self.sock.send(Parser.create_disconnect().encode("utf-8"))
        except (ConnectionResetError,OSError):print("Connection to server closed.")
        self.sock.close()
        self.connected = False
        self.app.stop()