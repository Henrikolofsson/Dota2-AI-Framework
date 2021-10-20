from typing import cast

from game.unit import Unit
from game.enums.entity_type import EntityType
from game.post_data_interfaces import ICourier, IEntity


class Courier(Unit):

    def get_type(self) -> EntityType:
        return EntityType.COURIER

    def update(self, data: IEntity):
        super().update(data)
        courier_entity_data: ICourier = cast(ICourier, data)

