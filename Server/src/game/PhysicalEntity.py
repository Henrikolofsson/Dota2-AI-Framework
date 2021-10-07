from typing import cast
from src.game.BaseEntity import BaseEntity
from src.game.Position import Position
from src.game.post_data_interfaces.IEntity import IEntity
from src.game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity


class PhysicalEntity(BaseEntity):
    
    _origin: Position

    def update(self, data: IEntity):
        physical_entity_data: IPhysicalEntity = cast(IPhysicalEntity, data)
        self._origin = Position(*physical_entity_data["origin"])