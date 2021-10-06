from typing import TypedDict
from src.game.post_data_interfaces.IHero import IHero
from src.game.post_data_interfaces.IWorld import IWorld

class IRoot(TypedDict):
    world: IWorld
    heroes: list[IHero]