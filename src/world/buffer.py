
class Buffer:
    def __init__(self, current:int|float, max:int|float) -> None:
        self.buffer = current
        self.max_buffer = max

    def __iadd__(self, other_buffer):self.buffer += other_buffer.buffer
    def __isub__(self, other_buffer):self.buffer -= other_buffer.buffer
    def __add__(self, other_buffer):return self.buffer + other_buffer.buffer
    def __sub__(self, other_buffer):return self.buffer - other_buffer.buffer
    def __gt__(self, other_buffer):return self.buffer > other_buffer
    def __ge__(self, other_buffer):return self.buffer >= other_buffer
    def __lt__(self, other_buffer):return self.buffer < other_buffer
    def __le__(self, other_buffer):return self.buffer <= other_buffer
    def __eq__(self, other_buffer):return self.buffer == other_buffer.buffer
    def __ne__(self, other_buffer):return self.buffer != other_buffer.buffer


    def force_push(self, destination, amount:int):
        destination.buffer += amount
        self.buffer -= amount
    
    def validate_amount(self, destination, amount:int) -> int:
        if self.buffer < amount: 
            amount = self.buffer
        if destination.max_buffer - destination.buffer <= amount:
            amount = destination.max_buffer - destination.buffer

        return amount
    
    def can_push(self, destination, amount):
        return self.buffer > amount and destination.buffer+amount <= destination.max_buffer and self.next_to(destination)
    def next_to(self, neighbor):
        return neighbor.x in (self.x-1,self.x+1) and neighbor.y in (self.y-1,self.y+1)
    
    def _push(self, destination, amount:int):
        if self.can_push(destination, amount): self.force_push(destination, amount)

    def push(self, destination, amount:int):
        self._push(destination, self.validate_amount(destination, amount))
