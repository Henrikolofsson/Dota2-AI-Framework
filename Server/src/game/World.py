#!/usr/bin/env python3
import math
from typing import Any
from Server.src.game.BaseEntity import BaseEntity
from Server.src.game.Position import Position

from src.game.BaseNPC import BaseNPC
from src.game.Tower import Tower
from src.game.Building import Building
from src.game.Hero import Hero
from src.game.PlayerHero import PlayerHero
from src.game.Tree import Tree


class World:

    entities: Any = {}
    game_ticks: int = 0
    player_heroes: list[PlayerHero] = []

    def update(self, world: Any) -> None:
        self.game_ticks = self.game_ticks + 1
        new_entities = {}
        for eid, data in world.items():
            entity = None
            if eid in self.entities:
                entity = self.entities[eid]
                entity.setData(data)
            else:
                entity = self._create_entity_from_data(data)
            new_entities[eid] = entity

        for eid, edata in self.entities.items():
            if edata.data["type"] == "Hero" and edata.data["team"] == 2:
                if eid not in new_entities:
                    edata.data["alive"] = False
                    new_entities[eid] = edata
        self.entities = new_entities

    def _create_entity_from_data(self, data: Any) -> BaseEntity:
        if data["type"] == "Hero" and data["team"] == 2:
            player_hero: PlayerHero = PlayerHero(data)
            self.player_heroes.append(player_hero)
            return player_hero
        elif data["type"] == "Hero":
            return Hero(data)
        elif data["type"] == "Tower":
            return Tower(data)
        elif data["type"] == "Building":
            return Building(data)
        elif data["type"] == "BaseNPC":
            return BaseNPC(data)
        elif data["type"] == "Tree":
            return Tree(data)

        raise Exception(
            "Error, the following entity did not match our entities:\n{}".format(data)
        )

    def get_player_heroes(self) -> list[PlayerHero]:
        return self.player_heroes

    def find_entity_by_name(self, name: str) -> BaseEntity:
        for entity in self.entities.values():
            if entity.getName() == name:
                return entity

        raise Exception("No entity with name: {0}".format(name))

    def get_distance_pos(self, pos1: Position, pos2: Position) -> float:
        x1 = pos1.x
        y1 = pos1.y
        x2 = pos2.x
        y2 = pos2.y
        return math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))

    def get_distance_units(self, entity1: BaseNPC, entity2: BaseNPC) -> float:
        return self.get_distance_pos(
            entity1.getOrigin(),
            entity2.getOrigin()
        )

    def get_id(self, entity: BaseEntity) -> int:
        return entity.get_id()

    def get_enemies_in_attack_range(self, entity: BaseNPC) -> list[BaseNPC]:
        return self.get_enemies_in_range(
            entity,
            range = entity.getAttackRange()
        )

    def get_enemies_in_range(self, entity: BaseNPC, range: float) -> list[BaseNPC]:
        enemies: list[BaseNPC] = []
        for enemy_entities in self.entities.values():
            if enemy_entities.getTeam() != entity.getTeam()\
            and self.get_distance_units(entity, enemy_entities) <= range\
            and enemy_entities.isAlive():
                enemies.append(enemy_entities)

        return enemies

    def get_allies_in_range(self, entity, range):
        allies = []
        for allied_entities in self.entities.values():
            if isinstance(allied_entities, Tree):
                continue
            if isinstance(allied_entities, Building):
                continue
            if self.get_distance_units(entity, allied_entities) > range:
                continue
            if allied_entities.getTeam() == entity.getTeam() and allied_entities.isAlive():
                allies.append(allied_entities)
        return allies

    def get_allies(self, entity: BaseNPC) -> list[BaseNPC]:
        entity
        for 

    def set_console_command(self, command):
        self.console_command = command

    def get_console_command(self):
        return self.console_command

    def get_enemy_towers(self, entity):
        towers = []

        for e in self.entities:
            if isinstance(e,
                          Tower) and e.getTeam() != entity.getTeam():
                towers.append(e)
        return towers

    def get_friendly_creeps(self, entity):
        creeps = []

        for e in self.entities.values():
            if isinstance(e, Building):
                continue
            if isinstance(e, Hero):
                continue
            if e.getTeam() == entity.getTeam():
                creeps.append(e)

        return creeps
