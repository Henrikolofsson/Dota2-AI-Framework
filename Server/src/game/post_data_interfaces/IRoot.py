from typing import TypedDict
from game.post_data_interfaces.IHero import IHero
from game.post_data_interfaces.IWorld import IWorld

class IRoot(TypedDict):
    world: IWorld
    heroes: list[IHero]