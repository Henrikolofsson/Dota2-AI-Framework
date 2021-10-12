from typing import cast
from abc import ABC, abstractmethod
from game.enums.entity_type import EntityType
from game.base_entity import BaseEntity
from game.position import Position
from game.post_data_interfaces.IEntity import IEntity
from game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity


class PhysicalEntity(BaseEntity, ABC):
    
    _position: Position

    def update(self, data: IEntity):
        physical_entity_data: IPhysicalEntity = cast(IPhysicalEntity, data)
        self._position = Position(*physical_entity_data["origin"])

    @abstractmethod
    def get_type(self) -> EntityType:
        pass

    def get_position(self) -> Position:
        return self._position