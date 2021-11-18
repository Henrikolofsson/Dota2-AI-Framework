#!/usr/bin/env python3
from typing import cast
from game.enums.entity_type import EntityType
from game.post_data_interfaces.IEntity import IEntity
from game.post_data_interfaces.IHero import IHero
from game.unit import Unit
from game.item import Item


class Hero(Unit):

    _has_tower_aggro: bool
    _has_aggro: bool
    _deaths: int
    _items: list[Item]

    def update(self, data: IEntity) -> None:
        super().update(data)
        hero_data = cast(IHero, data)

        self._has_tower_aggro = hero_data["hasTowerAggro"]
        self._has_aggro = hero_data["hasAggro"]
        self._deaths = hero_data["deaths"]
        self._set_items(hero_data)

    def _set_items(self, hero_data: IHero) -> None:
        self._items = []

        item_id = 0
        for item_data in hero_data["items"].values():
            if isinstance(item_data, list):
                continue
            item = Item(str(item_id))
            item.update(item_data)
            self._items.append(item)
            item_id += 1

    def get_has_tower_aggro(self) -> bool:
        return self._has_tower_aggro

    def get_has_aggro(self) -> bool:
        return self._has_aggro

    def get_deaths(self) -> int:
        return self._deaths

    def get_type(self) -> EntityType:
        return EntityType.HERO
