#!
# Abandonned

class MaterialStack:
    def __init__(self, type:str, amount:int) -> None:
        self.type = type
        self.amount = amount
        
    def process(self, other_material) -> int|float:
        if isinstance(other_material,int) or isinstance(other_material,float): return other_material
        assert other_material.type == self.type, "Not same type. Can't operate"
        return other_material.amount

    def __add__(self, other_material):return self.amount + self.process(other_material)
    def __sub__(self, other_material):return self.__add__(-self.process(other_material))
    def __iadd__(self, other_material): self.amount += self.process(other_material); return self
    def __isub__(self, other_material): return self.__iadd__(-self.process(other_material))
    