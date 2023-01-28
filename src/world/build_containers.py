from src.world.buildings import BUILDINGS

class BuildContainer:
    def __init__(self, type:str, pos:tuple[int,int]) -> None:
        self.pos = pos
        self.type = type
        self.buffer = 0

    @property
    def NBT(self): return {"buffer":self.buffer, "pos":self.pos}
