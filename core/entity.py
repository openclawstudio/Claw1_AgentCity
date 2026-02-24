from .models import BusinessState, Position

class Business:
    def __init__(self, business_id: str, pos: Position, business_type: str):
        self.state = BusinessState(id=business_id, pos=pos, business_type=business_type)
        self.id = business_id

    @property
    def balance(self):
        return self.state.balance

    @balance.setter
    def balance(self, value):
        self.state.balance = value

    @property
    def business_type(self):
        return self.state.business_type

    @property
    def pos(self):
        return self.state.pos