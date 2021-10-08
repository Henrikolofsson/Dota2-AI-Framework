from game.post_data_interfaces.IEntity import IEntity

class IItem(IEntity):
    charges: int
    castRange: int
    name: str
    slot: int