import socket
from socket import AF_INET, SOCK_STREAM
from src.server.server import Server
from src.server.parser import Parser
from time import sleep
from threading import Thread

class Client:
    def __init__(self, app) -> None:
        self.app = app
        self.connected = False
    
    def connect_to_server(self, server_ip:str):
        try:
            self.sock = socket.socket(AF_INET, SOCK_STREAM)
            print("Connecting...")
            self.sock.connect(Parser.parse_ip(server_ip))
        except ConnectionRefusedError:return
        print("Getting the initialization")
        init_instructions = self.sock.recv(2048).decode("utf-8")
        print("Parse",init_instructions)
        map, players, self_pos = Parser.parse_initialization(init_instructions)
        print("Start at",self_pos)
        self.app.game.map.load_map(map)
        self.app.game.camera.load_players(players, self_pos)
        self.app.game.camera.player.pos = self_pos
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
                disconnected_players,players_movements,build_changes = Parser.parse(raw_instructions)
                print("Got",disconnected_players,players_movements,build_changes)
                self.app.game.camera.disconnect_players(disconnected_players)
                self.app.game.camera.move_players(players_movements)
                self.app.game.map.handle_map_change(build_changes)
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
            sleep(.1)

    def disconnect(self):
        print("Disconnecting from server...")
        try:
            self.sock.send(Parser.create_disconnect().encode("utf-8"))
        except (ConnectionResetError,OSError):print("Connection to server closed.")
        self.sock.close()
        self.connected = False
        self.app.stop()