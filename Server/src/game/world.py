#!/usr/bin/env python3
from math import sqrt
from typing import Union, cast

from game.post_data_interfaces.IHero import IHero
from game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity

from game.base_entity import BaseEntity
from game.physical_entity import PhysicalEntity
from game.position import Position
from game.unit import Unit
from game.tower import Tower
from game.building import Building
from game.hero import Hero
from game.player_hero import PlayerHero
from game.tree import Tree
from game.courier import Courier
from game.rune import Rune


class World:

    _game_ticks: int
    _entities: list[PhysicalEntity]
    _player_heroes: list[PlayerHero]

    def __init__(self, team: int) -> None:
        self._team = team
        self._game_ticks = 0
        self._entities = []
        self._player_heroes = []

    def get_game_ticks(self) -> int:
        return self._game_ticks

    def update(self, entities: dict[str, IPhysicalEntity]) -> None:
        self._game_ticks += 1
        self._update_entities(entities)

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
            if new_hero["team"] == self._team: # ugly nested if, need better semantics: type = "Hero" & type = "PlayerHero"
                new_entity = PlayerHero(entity_id)
                self._player_heroes.append(new_entity)
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
        elif entity_data["type"] == "Courier":
            new_entity = Courier(entity_id)
        elif entity_data["type"] == "Rune":
            new_entity = Rune(entity_id)
        else:
            raise Exception(
                "Error, the following entity did not match our entities:\n{}".format(entity_data)
            )

        new_entity.update(entity_data)
        self._entities.append(new_entity)

    def get_entity_by_id(self, entity_id: str) -> Union[PhysicalEntity, None]:
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
        return sqrt(((position2.x - position1.x)**2) + ((position2.y - position1.y)**2))

    def get_distance_between_entities(self, entity1: PhysicalEntity, entity2: PhysicalEntity) -> float:
        '''Returns the distance between entity1 and entity2.'''
        return self.get_distance_between_positions(entity1.get_position(), entity2.get_position())

    def get_distance_between_units(self, unit1: Unit, unit2: Unit) -> float:
        '''Returns the distance between position of unit1 and position of unit2.'''
        return self.get_distance_between_entities(unit1, unit2)

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
            if unit.get_team() != to_get_enemies_of.get_team():
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
            and not isinstance(allied_unit, Hero)\
            and not isinstance(allied_unit, Courier):
                allied_creeps.append(allied_unit)

        return allied_creeps

    def get_enemy_creeps_of(self, unit: Unit) -> list[Unit]:
        '''Returns all enemy creeps of given unit.'''
        enemy_creeps: list[Unit] = []

        for enemy_unit in self.get_enemies_of(unit):
            if not isinstance(enemy_unit, Building)\
            and not isinstance(enemy_unit, Hero)\
            and not isinstance(enemy_unit, Courier):
                enemy_creeps.append(enemy_unit)

        return enemy_creeps

    def get_enemy_heroes_of(self, unit: Unit) -> list[Hero]:
        '''Returns all enemy heroes of given unit.'''
        enemy_heroes: list[Hero] = []

        for enemy_unit in self.get_enemies_of(unit):
            if isinstance(enemy_unit, Hero):
                enemy_heroes.append(enemy_unit)

        return enemy_heroes

    def get_runes(self) -> list[Rune]:
        '''Returns all runes.'''
        runes: list[Rune] = []
        
        for entity in self._entities:
            if isinstance(entity, Rune):
                runes.append(entity)
        
        return runes

    def get_all_trees(self) -> list[Tree]:
        '''Returns all trees.'''
        trees: list[Tree] = []

        for entity in self._entities:
            if isinstance(entity, Tree):
                trees.append(entity)

        return trees

    def get_trees_in_range_of(self, unit: Unit, range: float) -> list[Tree]:
        '''Returns all trees in specified range of given unit.'''
        trees: list[Tree] = []

        for tree in self.get_all_trees():
            if self.get_distance_between_entities(unit, tree) <= range:
                trees.append(tree)

        return trees