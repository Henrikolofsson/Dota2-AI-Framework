from typing import cast
from game.base_entity import BaseEntity
from game.enums.entity_type import EntityType
from game.post_data_interfaces.IEntity import IEntity
from game.post_data_interfaces.IItem import IItem

class Item(BaseEntity):

    _charges: int
    _cast_range: int
    _name: str
    _slot: int

    def update(self, data: IEntity):
        super().update(data)
        item_data: IItem = cast(IItem, data)
        self._charges = item_data["charges"]
        self._name = item_data["name"]
        self._cast_range = item_data["castRange"]
        self._slot = item_data["slot"]

    def get_charges(self) -> int:
        return self._charges

    def get_cast_range(self) -> int:
        return self._cast_range

    def get_name(self) -> str:
        return self._name

    def get_slot(self) -> int:
        return self._slot

    def get_type(self) -> EntityType:
        return EntityType.ITEM