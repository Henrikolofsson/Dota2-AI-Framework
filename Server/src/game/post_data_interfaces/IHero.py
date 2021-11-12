from typing import Any, Union
from game.post_data_interfaces.IAbility import IAbility
from game.post_data_interfaces.IItem import IItem
from game.post_data_interfaces.IUnit import IUnit

class IHero(IUnit):
    denies: int
    abilityPoints: int
    abilities: dict[str, IAbility]
    items: dict[str, Union[IItem, list[Any]]]
    xp: int
    hasTowerAggro: bool
    hasAggro: bool
    gold: int
    deaths: int
    courier_id: str