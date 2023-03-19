class _MaterialType(str):pass

def process(buffer) -> int|float:
    if isinstance(buffer, Buffer):
        return buffer.buffer
    elif isinstance(buffer, int) or isinstance(buffer, float): return buffer
    raise ValueError("Unhandled buffer type")

class Buffer:
    def __init__(self, current:int|float, max:int|float, type:_MaterialType) -> None:
        self.buffer = current
        self.max = max
        self.type = type


    def __iadd__(self, other_buffer):self.buffer += process(other_buffer);return self
    def __isub__(self, other_buffer):return self.__iadd__( process(other_buffer))
    
    def __add__(self, other_buffer):return self.buffer + process(other_buffer)
    def __sub__(self, other_buffer):return self.__add__( process(other_buffer))
    
    def __gt__(self, other_buffer):return self.buffer > process(other_buffer)
    def __ge__(self, other_buffer):return self.buffer >= process(other_buffer)
    def __lt__(self, other_buffer):return self.buffer < process(other_buffer)
    def __le__(self, other_buffer):return self.buffer <= process(other_buffer)
    def __eq__(self, other_buffer):return self.buffer == process(other_buffer)
    def __ne__(self, other_buffer):return self.buffer != process(other_buffer)
    
    def __str__(self): return str(self.int)
    
    @property
    def precise(self):return self.buffer
    @property
    def int(self):return int(self.buffer)

    def force_push(self, destination_buffer, amount:int):
        destination_buffer += amount
        self.buffer -= amount
    
    def validate_amount(self, destination_buffer, amount:int) -> int:
        if self.buffer < amount: 
            amount = self.buffer
        if destination_buffer.max - destination_buffer.buffer <= amount:
            amount = destination_buffer.max - destination_buffer.buffer

        return amount
    
    def can_push(self, destination_buffer, amount, check_for_allow_type=True):
        can_push = self.buffer > amount and destination_buffer+amount <= destination_buffer.max
        return can_push and self.allow_type(destination_buffer) if check_for_allow_type else can_push

    def _push(self, destination_buffer, amount:int):
        if self.can_push(destination_buffer, amount): self.force_push(destination_buffer, amount)

    def push(self, destination_buffer, amount:int):
        self._push(destination_buffer, self.validate_amount(destination_buffer, amount))

    def allow_type(self, other_buffer):
        if isinstance(other_buffer, str):
            return self.type == other_buffer
        return self.type == other_buffer.type

    def clear(self):self.buffer = 0