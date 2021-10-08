#!/usr/bin/env python3
import math
from typing import Union, cast
from game.PhysicalEntity import PhysicalEntity
from game.post_data_interfaces.IHero import IHero
from game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity
from game.BaseEntity import BaseEntity
from game.Position import Position

from game.Unit import Unit
from game.Tower import Tower
from game.Building import Building
from game.Hero import Hero
from game.PlayerHero import PlayerHero
from game.Tree import Tree


class World:

    _entities: list[PhysicalEntity] = []
    _game_ticks: int = 0
    _player_heroes: list[PlayerHero] = []

    def update(self, world: dict[str, IPhysicalEntity]) -> None:
        self._game_ticks += 1
        self._update_entities(world)

    def _update_entities(self, new_entities: dict[str, IPhysicalEntity]) -> None:
        for entity_id, entity_data in new_entities.items():
            self._update_if_exists_else_add_new_entity(entity_id, entity_data)

        for entity in self._entities:
            if entity.get_id() not in new_entities.keys():
                self._set_dead_if_player_hero_else_remove_entity(entity)

    def _update_if_exists_else_add_new_entity(self, entity_id: str, entity_data: IPhysicalEntity) -> None:
        entity: Union[BaseEntity, None] = self.get_entity_by_id(entity_id)
        if entity is None:
            self._add_new_entity(entity_id, entity_data)
        else:
            entity.update(entity_data)

    def _set_dead_if_player_hero_else_remove_entity(self, entity: PhysicalEntity) -> None:
        if isinstance(entity, PlayerHero):
            entity.set_alive(False)
        else:
            self._entities.remove(entity)

    def _add_new_entity(self, entity_id: str, entity_data: IPhysicalEntity) -> None:
        new_entity: PhysicalEntity

        if entity_data["type"] == "Hero":
            new_hero: IHero = cast(IHero, entity_data)
            if new_hero["team"] == 2: # ugly nested if, need better semantics: type = "Hero" & type = "PlayerHero"
                new_entity = PlayerHero(entity_id)
            else:
                new_entity = Hero(entity_id)
        
        elif entity_data["type"] == "Tower":
            new_entity = Tower(entity_id)
        
        elif entity_data["type"] == "Building":
            new_entity = Building(entity_id)

        elif entity_data["type"] == "BaseNPC":
            new_entity = Unit(entity_id)

        elif entity_data["type"] == "Tree":
            new_entity = Tree(entity_id)

        else:
            raise Exception(
                "Error, the following entity did not match our entities:\n{}".format(entity_data)
            )

        new_entity.update(entity_data)
        self._entities.append(new_entity)

    def get_entity_by_id(self, entity_id: str) -> Union[BaseEntity, None]:
        for entity in self._entities:
            if entity.get_id() == entity_id:
                return entity

        return None

    def get_player_heroes(self) -> list[PlayerHero]:
        '''Returns all bot-controlled heroes.'''
        return self._player_heroes

    def get_unit_by_name(self, name: str) -> PhysicalEntity:
        '''Returns first entity with specified name.'''
        for unit in self.get_units():
            if unit.get_name() == name:
                return unit

        raise Exception("No entity with name: {0}".format(name))

    def get_distance_between_positions(self, position1: Position, position2: Position) -> float:
        '''Returns the distance between position1 and position2.'''
        return math.sqrt(((position2.x - position1.x)**2) + ((position2.y - position1.y)**2))

    def get_distance_between_units(self, unit1: Unit, unit2: Unit) -> float:
        '''Returns the distance between position of unit1 and position of unit2.'''
        return self.get_distance_between_positions(
            unit1.get_origin(),
            unit2.get_origin()
        )

    def get_enemies_in_attack_range_of(self, unit: Unit) -> list[Unit]:
        '''Returns all enemies in attack range of specified unit.'''
        return self.get_enemies_in_range_of(
            unit,
            range = unit.get_attack_range()
        )

    def get_enemies_in_range_of(self, unit: Unit, range: float) -> list[Unit]:
        '''Returns all enemy units in specified range of given unit.'''
        enemies: list[Unit] = []

        for enemy_entity in self.get_enemies_of(unit):
            if self.get_distance_between_units(unit, enemy_entity) <= range\
            and enemy_entity.is_alive():
                enemies.append(enemy_entity)

        return enemies

    def get_allies_in_range_of(self, unit: Unit, range: float) -> list[Unit]:
        '''Returns all allied units in specified range of given unit.'''
        allies: list[Unit] = []

        for allied_unit in self.get_allies_of(unit):
            if self.get_distance_between_units(unit, allied_unit) <= range\
            and allied_unit.is_alive():
                allies.append(allied_unit)

        return allies

    def get_allies_of(self, to_get_allies_of: Unit) -> list[Unit]:
        '''Returns all allies of given unit.'''
        allies: list[Unit] = []

        for unit in self.get_units():
            if unit.get_team() == to_get_allies_of.get_team():
                allies.append(unit)

        return allies

    def get_enemies_of(self, to_get_enemies_of: Unit) -> list[Unit]:
        '''Returns all enemies of given unit.'''
        enemies: list[Unit] = []
        
        for unit in self.get_units():
            if unit.get_team() == to_get_enemies_of.get_team():
                enemies.append(unit)

        return enemies

    def get_units(self) -> list[Unit]:
        '''Returns all units.'''
        units: list[Unit] = []
        
        for entity in self._entities:
            if isinstance(entity, Unit):
                units.append(entity)

        return units

    def get_enemy_towers_of(self, unit: Unit) -> list[Tower]:
        '''Returns all enemy towers of given unit.'''
        enemy_towers: list[Tower] = []

        for enemy_unit in self.get_enemies_of(unit):
            if isinstance(enemy_unit, Tower):
                enemy_towers.append(enemy_unit)

        return enemy_towers

    def get_allied_creeps_of(self, unit: Unit) -> list[Unit]:
        '''Returns all allied creeps of given unit.'''
        allied_creeps: list[Unit] = []

        for allied_unit in self.get_allies_of(unit):
            if not isinstance(allied_unit, Building)\
            and not isinstance(allied_unit, Hero):
                allied_creeps.append(allied_unit)

        return allied_creeps