from src.multiplayer.src import *
class Instructions:
    def __init__(self, instructions:list[str]) -> None:
        self.instructs = []
        self.outputs = []
        for instruction in instructions:
            self.add_instruction(instruction)
    def str(self, delete:bool=False):
        output = MARKER.join(self.outputs)
        if delete:self.clear()
        return output
    def clear(self):
        self.outputs = []
        self.instructs = []
    @staticmethod
    def unstr(instructions:str):
        outputs = {"player_movements": [], "tile_changes":[]}
        for inst in instructions.split(MARKER):
            mode = inst[0]
            if mode == PLAYER_MOVEMENT:
                player_name = inst[1:inst.index("/")]
                new_pos = inst[inst.index("/"):].split(",")
                outputs["player_movements"].append((player_name, new_pos))
            elif mode == TILE_CHANGE:
                building_type = inst[1:inst.index("{")]
                NBT = inst[inst.index("{"):inst.index("}")]
                pos = inst[inst.index("/"):].split(",")
                outputs.append((building_type,NBT, pos))
        return outputs
    def add_player_move(self, name, new_pos):
        pos = self.process_pos(pos)
        self.outputs.append(f"{PLAYER_MOVEMENT}{name}/{new_pos}")
    def add_build_change(self, build, pos):
        pos = self.process_pos(pos)
        self.outputs.append(f"{TILE_CHANGE}{build.stringify()}/{pos}")

    def process_pos(self, pos:tuple[float,float]|tuple[int,int]):
        if isinstance(pos, str):
            return pos
        return f"{pos[0]},{pos[1]}"
    def add_instruction(self, instruction:str):
        mode = instruction[0]
        if mode == PLAYER_MOVEMENT:
            next_marker = instruction.index("/")
            player_name = instruction[1:next_marker]
            new_pos = instruction[next_marker:].split(",")
            self.outputs["player_movements"].append((player_name, new_pos))
        elif mode == TILE_CHANGE:
            building_type = instruction[1:instruction.index("{")]
            NBT = instruction[instruction.index("{"):instruction.index("}")]
            pos = instruction[instruction.index("/"):].split(",")
            self.outputs.append((building_type,NBT, pos))

class LoadingInstructions(Instructions):
    def __init__(self, loaded_map:dict) -> None:
        super().__init__()
        self.map = loaded_map
    def str(self, delete:bool=False):
        if delete: self.instructs = []; self.outputs = []
        return f"{MAP_INITIALISATION}{self.map}"
