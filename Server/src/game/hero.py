#!/usr/bin/env python3
from typing import cast
from game.enums.entity_type import EntityType
from game.post_data_interfaces.IEntity import IEntity
from game.post_data_interfaces.IHero import IHero
from game.unit import Unit
from game.ability import Ability


class Hero(Unit):

    _ability_points: int
    _abilities: list[Ability]
    _has_tower_aggro: bool
    _deaths: int
    _denies: int
    _gold: int
    _type: str
    _xp: int

    def update(self, data: IEntity):
        super().update(data)
        hero_data = cast(IHero, data)
        self._ability_points = hero_data["abilityPoints"]
        self._has_tower_aggro = hero_data["hasTowerAggro"]
        self._deaths = hero_data["deaths"]
        self._denies = hero_data["denies"]
        self._gold = hero_data["gold"]
        self._type = hero_data["type"]
        self._xp = hero_data["xp"]
        self._set_abilities(hero_data)

    def _set_abilities(self, data: IHero):
        self._abilities = []

        ability_id = 0
        for abilityData in data["abilities"].values():
            ability = Ability(str(ability_id))
            ability.update(abilityData)
            self._abilities.append(ability)
            ability_id += 1

    def get_ability_points(self) -> int:
        return self._ability_points

    def get_abilities(self) -> list[Ability]:
        return self._abilities

    def get_has_tower_aggro(self) -> bool:
        return self._has_tower_aggro

    def get_deaths(self) -> int:
        return self._deaths

    def get_denies(self) -> int:
        return self._denies

    def get_gold(self) -> int:
        return self._gold

    def get_xp(self) -> int:
        return self._xp

    def get_type(self) -> EntityType:
        return EntityType.HERO
