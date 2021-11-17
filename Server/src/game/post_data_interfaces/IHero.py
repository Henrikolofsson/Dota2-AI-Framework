from typing import Any, Union
from game.post_data_interfaces.IItem import IItem
from game.post_data_interfaces.IUnit import IUnit

class IHero(IUnit):
    hasTowerAggro: bool
    hasAggro: bool
    deaths: int
    items: dict[str, Union[IItem, list[Any]]]
