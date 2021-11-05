from typing import cast

from game.unit import Unit
from game.item import Item
from game.enums.entity_type import EntityType
from game.post_data_interfaces.ICourier import ICourier
from game.post_data_interfaces.IEntity import IEntity


class Courier(Unit):

    _items: list[Item]

    def get_type(self) -> EntityType:
        return EntityType.COURIER

    def update(self, data: IEntity):
        super().update(data)
        courier_entity_data: ICourier = cast(ICourier, data)
        self._set_items(courier_entity_data)

    def _set_items(self, courier_entity_data: ICourier) -> None:
        self._items = []

        item_id = 0
        for item_data in courier_entity_data["items"].values():
            if isinstance(item_data, list):
                continue
            item = Item(str(item_id))
            item.update(item_data)
            self._items.append(item)
            item_id += 1

    def get_items(self) -> list[Item]:
        return self._items