from src.server.src import *
import json
import socket
from typing import Any
####################################
# Strings sent with sockets be-likes
#
# For init                                      Position of the incoming player
# IMap/{...}|IPlayers/{"name":"skin_url"}|IPos/X,Y
#
# For game
# DSxmourai/Got kicked by example.|PHades/15.6,9.5|BFactory/{buffer:999}
#
#CLient side
# D/I quit because I want|P/(10.5,10.7)|CGen/{buffer:999}


class Parser:
    @staticmethod
    def create_initialization(map:dict, players:dict, player_pos:tuple[float,float]|tuple[int,int]):
        parsed = ""
        parsed += f"{INIT_MARKER}Map{MODE_DELIMITER}{map}{END_DELIMITER}"
        parsed += f"{INIT_MARKER}Players{MODE_DELIMITER}{players}{END_DELIMITER}"
        parsed += f"{INIT_MARKER}Pos{MODE_DELIMITER}{player_pos[0]},{player_pos[1]}{END_DELIMITER}"
        return parsed
    @staticmethod
    def parse_initialization(instructions:str) -> list:
                #Map    Players   Pos of player
        parsed = [{},   {},         ()]
        for instruction in instructions.split(END_DELIMITER):
            if not instruction:continue
            tag = instruction[0]
            if tag == INIT_MARKER:
                mode_delimiter_index = instruction.index(MODE_DELIMITER)
                mode = instruction[1:mode_delimiter_index]
                if mode == "Map":
                    
                    parsed[0] = json.loads(instruction[mode_delimiter_index+1:])
                elif mode == "Players":
                    parsed[1] = json.loads(instruction[mode_delimiter_index+1:])
                elif mode == "Pos":
                    parsed[2] = instruction[mode_delimiter_index+2:-1].split(",")
                    parsed[2][0] = int(parsed[2][0])
                    parsed[2][1] = int(parsed[2][1])
        return parsed
    @staticmethod
    def sync_parse(): assert False, "Not implemented"
    @staticmethod
    def move_player_parse(player) -> str:
        parsed_move = f"{PLAYER_MOVEMENT}"
        parsed_move += f"{player.x},{player.y}"
        return parsed_move
    @staticmethod
    def build_change_parse(build):
        parsed_change = f"{TILE_CHANGE}"
        parsed_change += f"{build.type}{MODE_DELIMITER}{build.NBT}"
        return parsed_change
    @staticmethod
    def disconnect_parse(player,msg:str=None) -> bool|str:
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
    def parse(instructions:str) -> tuple[list,list,list]:
        parsed = ([],[],[])
        if not instructions: return parsed
        
        for inst in instructions.split(END_DELIMITER):
            if not inst:continue
            print(inst)
            tag = inst[0]
            if tag == {DISCONNECT}:
                player,i = Parser.get_model(inst)
                msg = Parser.get_last(inst)
                parsed[0].append((player,msg))
            elif tag == {PLAYER_MOVEMENT}:
                player,i = Parser.get_model(inst)
                pos = Parser.get_last(inst).split(",")
                parsed[1].append((player,pos))
            elif tag == {TILE_CHANGE}:
                build_type = Parser.get_model(inst)
                build_nbt,i = Parser.get_nbts(inst)
                build_pos = inst[i:].split(",")
                parsed[2].append((build_type, build_nbt, build_pos))
        return parsed
    @staticmethod
    def get_nbts(instruction:str) -> tuple[str,int]:
        mode_index = instruction.index(MODE_DELIMITER)
        last_mode_index = instruction[mode_index:].index(MODE_DELIMITER)
        return instruction[mode_index:last_mode_index], last_mode_index
    
    @staticmethod
    def stringify_parsed(parsed:tuple[list,list,list]) -> list[str]:
        stringified_parse = []
        for disconnected_player_name, msg in parsed[0]:
            stringified_parse += f"{DISCONNECT}{disconnected_player_name}{MODE_DELIMITER}{msg}{END_DELIMITER}"
        for player_name, new_pos in parsed[1]:
            stringified_parse += f"{PLAYER_MOVEMENT}{player_name}{MODE_DELIMITER}{new_pos}{END_DELIMITER}"
        for build_type, nbt, new_pos in parsed[2]:
            stringified_parse += f"{TILE_CHANGE}{build_type}{MODE_DELIMITER}{nbt}{END_DELIMITER}"

        return stringified_parse
    
    @staticmethod
    def parse_client(raw:str):
        parsed = [(),   False,           {}]
        if not raw: return parsed
        # Player moves    If disconnected   Build changes
        instructions = raw.split(END_DELIMITER)
        for craw in instructions:
            if not craw:continue
            tag = craw[0]
            if tag == {PLAYER_MOVEMENT}:
                x,y = Parser.get_last(craw)[1:-1].split(",")
                pos = float(x),float(y)
                parsed[0] = pos
            elif tag == {DISCONNECT}:
                parsed[1] = Parser.get_last(craw)
                print("so",Parser.get_last(craw),type(Parser.get_last(craw)))
            elif tag == {TILE_CHANGE}:
                assert False, "Not done yet !"
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
        
        for client_instructions in instructions:
            client, instruct = client_instructions
            if isinstance(instruct, str):
                parsed = f"{DISCONNECT}{client}{MODE_DELIMITER}{instruct}"
            elif isinstance(instruct, tuple):
                parsed = f"{PLAYER_MOVEMENT}{client}{MODE_DELIMITER}({instruct[0]},{instruct[1]})"
            #elif isinstance(instruct, unknown): TILE_CHANGE
            else:print("Unknown:",instruct,type(instruct),"from",client);continue
            outputs += END_DELIMITER + parsed
        return outputs
    
    @staticmethod
    def should_disconnect(raw:str, player_name:str):
        return str(player_name) in raw

    @staticmethod
    def create_move_instruct(new_move:tuple) -> bytes:
        x,y = round(new_move[0], 3),round(new_move[1], 3)
        return f"{PLAYER_MOVEMENT}{MODE_DELIMITER}({x},{y}){END_DELIMITER}".encode("utf-8")