import json
import socket
from typing import Any

from src.server.src import *
from src.world.buildings import Building, TITLES

####################################
# Strings sent with sockets be-likes
#
# For init                                      Position of the incoming player
# IMap/{...}|IPos/X,Y
#
# For game
# DSxmourai/Got kicked by example.|PHades/15.6,9.5|BFactory/{buffer:999}
#
#CLient side
# D/I quit because I want|P/(10.5,10.7)|CGen/{buffer:999}


class Parser:
    @staticmethod
    def create_initialization(map:dict, players:tuple, player_pos:tuple[float,float]|tuple[int,int]):
        parsed = ""
        nmap = ""
        for build in map.values():
            nmap += f"{build}{BUILD_DELIMITER}"
        # nmap = nmap.replace("'", "")
        parsed += f"{INIT_MARKER}Map{MODE_DELIMITER}{nmap[:-1]}{END_DELIMITER}"
        for player in players:
            parsed += f"{PLAYER_MOVEMENT}{player[0]}{MODE_DELIMITER}{player[1]}{END_DELIMITER}"
        parsed += f"{INIT_MARKER}Pos{MODE_DELIMITER}{player_pos[0]},{player_pos[1]}{END_DELIMITER}"
        return parsed

    @staticmethod
    def create_build(type:str, nbts:dict, construct:bool=True):
        build = TITLES[type](nbts["pos"])
        build.buffer = nbts["buffer"]
        if construct: build.construct(buy=False, send=False)
        return build


    @staticmethod
    def create_build_from_str(build:str, construct:bool=True) -> Building:
        try:
            type,i = Parser.to("{", build, start=0)
        except ValueError: print("Unknown build:",build);return
        nbts_str = Parser.from_str(i, build)
        print(nbts_str)
        nbts = json.loads(nbts_str)
        build = TITLES[type](nbts["pos"])
        build.buffer = nbts["buffer"]
        if construct: build.construct(buy=False, send=False)
        return build
    
    @staticmethod
    def create_build_str(type:str, nbts:dict) -> str:
        return f"{type}{json.dumps(nbts)}"

    @staticmethod
    def parse_initialization(instructions:str) -> list:
                #Players moves   Pos of player
        parsed = [[],               ()]
        for instruction in instructions.split(END_DELIMITER):
            if not instruction:continue
            tag = instruction[0]
            mode_delimiter_index = instruction.index(MODE_DELIMITER)
            mode = instruction[1:mode_delimiter_index]
            if tag == PLAYER_MOVEMENT:
                #       mode= Player name       Pos of player
                x,y = instruction[mode_delimiter_index+2:-1].split(",")
                x,y = round(int(x),3),round(int(y),3)
                parsed[0].append((mode, (x,y)))
            elif tag == INIT_MARKER:
                if mode == "Map":
                    builds = Parser.from_str(mode_delimiter_index+1, instruction)
                    if not builds: continue
                    for build in builds.split(BUILD_DELIMITER):
                        if not build: continue
                        Parser.create_build_from_str(build, construct=True)

                elif mode == "Pos":
                    x,y = [float(coord) for coord in instruction[mode_delimiter_index+1:].split(",")]
                    parsed[1] = x,y
        return parsed
    @staticmethod
    def sync_parse(): assert False, "Not implemented"
    @staticmethod
    def move_player_create(player) -> str:
        parsed_move = f"{PLAYER_MOVEMENT}"
        parsed_move += f"{player.x},{player.y}"
        return parsed_move
    @staticmethod
    def build_change_create(build):
        return f"{TILE_CHANGE}{build.str()}{END_DELIMITER}"
    @staticmethod
    def disconnect_create(player,msg:str=None) -> bool|str:
        msg = msg if msg else "Disconnected"
        return f"{DISCONNECT}{player}{MODE_DELIMITER}{msg}"
    
    @staticmethod
    def get_model(instruction:str) -> tuple[str,int]:
        mode_index = instruction.index(MODE_DELIMITER)
        return instruction[1:mode_index], mode_index
    
    @staticmethod
    def get_last(instruction:str) -> str:
        mode_index = instruction.index(MODE_DELIMITER)
        return instruction[mode_index+1:]

    @staticmethod
    def parse_server(instructions:str) -> tuple[list,list]:
        parsed = ([],[])
        if not instructions: return parsed
        
        for inst in instructions.split(END_DELIMITER):
            if not inst:continue
            tag = inst[0]
            if tag == DISCONNECT:
                player,i = Parser.get_model(inst)
                msg = Parser.get_last(inst)
                parsed[0].append((player,msg))
            elif tag == PLAYER_MOVEMENT:
                player,i = Parser.get_model(inst)
                x,y = Parser.get_last(inst)[1:-1].split(",")
                pos = float(x),float(y)
                parsed[1].append((player,pos))
            elif tag == TILE_CHANGE:
                Parser.create_build_from_str(inst[1:])

        return parsed

    @staticmethod
    def to(stop:str, overall:str, start:int=1):
        i = overall.index(stop)
        return overall[start:i], i
    @staticmethod
    def from_str(start_index:int|str, overall:str, end=None):
        if isinstance(start_index, str): start_index = overall.index(start_index)
        if end: return overall[start_index:end]
        return overall[start_index:]

    @staticmethod
    def get_nbts(instruction:str) -> tuple[str,int]:
        mode_index = instruction.index(MODE_DELIMITER)
        last_mode_index = instruction[mode_index:].index(MODE_DELIMITER)
        return instruction[mode_index:last_mode_index], last_mode_index
    
    
    @staticmethod
    def parse_client(raw:str):
        # Player moves    If disconnected   Build changes
        parsed = [(),   False,           []]
        if not raw: return parsed
        
        for craw in raw.split(END_DELIMITER):
            if not craw:continue
            tag = craw[0]
            if tag == PLAYER_MOVEMENT:
                x,y = craw[3:-1].split(",")
                pos = float(x),float(y)
                parsed[0] = pos
            elif tag == DISCONNECT:
                parsed[1] = Parser.get_last(craw)
                print("so",Parser.get_last(craw),type(Parser.get_last(craw)))
            elif tag == TILE_CHANGE:#CString-Generator{...}
                build_str = Parser.from_str(1, craw)
                nbts = Parser.from_str("{", craw).replace("'", '"')
                pos = json.loads(nbts)["pos"]
                parsed[2].append((tuple(pos), build_str))
        return parsed


    @staticmethod
    def create_disconnect(message:str="Disconnected."):
        return f"{DISCONNECT}{MODE_DELIMITER}{message}"
    
    @staticmethod
    def parse_ip(server_ip:str) -> tuple[str, int]:
        if ":" in server_ip:
            ip,port = server_ip.split(":")
        else:
            ip = server_ip
            port = PORT
        return ip,int(port)

    @staticmethod
    def create_output(instructions:list[tuple[socket.socket, Any]]) -> str:
        outputs = ""
        
        move_clients = []
        moved_clients = []
        
        for instruct in instructions:
            mode = instruct[0]
            if mode is DISCONNECT:
                client,message = instruct[1], instruct[-1]
                parsed = f"{DISCONNECT}{client}{MODE_DELIMITER}{message}"
            elif mode is PLAYER_MOVEMENT:
                client, pos = instruct[1], instruct[-1]
                if client in moved_clients:
                    index = moved_clients.index(client)
                    move_clients[index] = pos
                else:
                    move_clients.append(pos)
                    moved_clients.append(client)
                continue
            
            elif mode is TILE_CHANGE:
                parsed = f"{TILE_CHANGE}{instruct[1]}"
            else:print("Unknown:",instruct,type(instruct));continue
            outputs += END_DELIMITER + parsed

        for i in range(len(moved_clients)):
            outputs += END_DELIMITER + f"{PLAYER_MOVEMENT}{moved_clients[i]}{MODE_DELIMITER}({move_clients[i][0]},{move_clients[i][1]})"
        
        return outputs
    
    @staticmethod
    def should_disconnect(raw:str, player_name:str):
        return str(player_name) in raw

    @staticmethod
    def create_move_instruct(new_move:tuple) -> bytes:
        x,y = round(new_move[0], 3),round(new_move[1], 3)
        return f"{PLAYER_MOVEMENT}{MODE_DELIMITER}({x},{y}){END_DELIMITER}".encode("utf-8")
    
    @staticmethod
    def parse_pseudo(pseudo:str) -> str:
        return pseudo[1:-1]
    
    @staticmethod
    def create_pseudo(pseudo:str) -> str:
        return f"{INIT_MARKER}{pseudo}{END_DELIMITER}"