from typing import TypedDict

from game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity

class IWorld(TypedDict):
    entities: dict[str, IPhysicalEntity]