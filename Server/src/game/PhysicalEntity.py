from typing import cast
from Server.src.game.BaseEntity import BaseEntity
from Server.src.game.Position import Position
from Server.src.game.post_data_interfaces.IEntity import IEntity
from Server.src.game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity


class PhysicalEntity(BaseEntity):
    
    _origin: Position

    def update(self, data: IEntity):
        physical_entity_data: IPhysicalEntity = cast(IPhysicalEntity, data)
        self._origin = Position(
            physical_entity_data["origin"]["x"],
            physical_entity_data["origin"]["y"],
            physical_entity_data["origin"]["z"]
        )