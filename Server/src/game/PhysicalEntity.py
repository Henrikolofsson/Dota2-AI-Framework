from typing import cast
from game.BaseEntity import BaseEntity
from game.Position import Position
from game.post_data_interfaces.IEntity import IEntity
from game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity


class PhysicalEntity(BaseEntity):
    
    _origin: Position

    def update(self, data: IEntity):
        physical_entity_data: IPhysicalEntity = cast(IPhysicalEntity, data)
        self._origin = Position(*physical_entity_data["origin"])