#!/usr/bin/env python3
import math
from typing import Any, cast
from src.game.post_data_interfaces.IHero import IHero
from src.game.post_data_interfaces.IPhysicalEntity import IPhysicalEntity
from src.game.BaseEntity import BaseEntity
from src.game.Position import Position

from src.game.Unit import Unit
from src.game.Tower import Tower
from src.game.Building import Building
from src.game.Hero import Hero
from src.game.PlayerHero import PlayerHero
from src.game.Tree import Tree


class World:

    entities: Any = {}
    game_ticks: int = 0
    player_heroes: list[PlayerHero] = []

    def update(self, world: dict[str, IPhysicalEntity]) -> None:
        self.game_ticks += 1
        new_entities = {}
        for eid, data in world.items():
            entity = None
            if eid in self.entities:
                entity = self.entities[eid]
                entity.setData(data)
            else:
                entity = self._create_entity_from_data(eid, data)
            new_entities[eid] = entity

        for eid, edata in self.entities.items():
            if edata.data["type"] == "Hero" and edata.data["team"] == 2:
                if eid not in new_entities:
                    edata.data["alive"] = False
                    new_entities[eid] = edata
        self.entities = new_entities

    def _create_entity_from_data(self, entity_id: str, data: IPhysicalEntity) -> BaseEntity:
        if data["type"] == "Hero":
            hero_data: IHero = cast(IHero, data)

            if hero_data["team"] == 2:
                player_hero: PlayerHero = PlayerHero(entity_id)
                player_hero.update(data)
                self.player_heroes.append(player_hero)
                return player_hero
            else:
                hero = Hero(entity_id)
                hero.update(data)
                return hero

        elif data["type"] == "Tower":
            tower = Tower(entity_id)
            tower.update(data)
            return tower

        elif data["type"] == "Building":
            building = Building(entity_id)
            building.update(data)
            return building

        elif data["type"] == "BaseNPC":
            unit = Unit(entity_id)
            unit.update(data)
            return unit

        elif data["type"] == "Tree":
            tree = Tree(entity_id)
            tree.update(data)
            return tree

        raise Exception(
            "Error, the following entity did not match our entities:\n{}".format(data)
        )

    def get_player_heroes(self) -> list[PlayerHero]:
        '''Returns all bot-controlled heroes.'''
        return self.player_heroes

    def get_entity_by_name(self, name: str) -> BaseEntity:
        '''Returns first entity with specified name.'''
        for entity in self.entities.values():
            if entity.get_name() == name:
                return entity

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
        
        for entity in self.entities.values():
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