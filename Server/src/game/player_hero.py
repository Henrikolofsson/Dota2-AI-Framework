#!/usr/bin/env python3

from time import time
from typing import Any, cast
from game.ability import Ability
from game.post_data_interfaces.IPlayerHero import IPlayerHero
from game.position import Position
from game.post_data_interfaces.IHero import IHero
from game.post_data_interfaces.IEntity import IEntity
from game.item import Item
from game.enums.entity_type import EntityType
from game.hero import Hero


class PlayerHero(Hero):

    _time_of_death: float
    _ability_points: int
    _abilities: list[Ability]
    _denies: int
    _gold: int
    _xp: int
    _courier_id: str
    _buyback_cost: int
    _buyback_cooldown_time: float

    def __init__(self, entity_id: str):
        super().__init__(entity_id)
        self.command = None
        self.commands = []

    def update(self, data: IEntity):
        super().update(data)
        player_hero_data: IHero = cast(IPlayerHero, data)

        if player_hero_data["alive"]:
            self._time_of_death = 0

        self._ability_points = player_hero_data["abilityPoints"]
        self._denies = player_hero_data["denies"]
        self._gold = player_hero_data["gold"]
        self._xp = player_hero_data["xp"]
        self._courier_id = player_hero_data["courier_id"]
        self._buyback_cost = player_hero_data["buybackCost"]
        self._buyback_cooldown_time = player_hero_data["buybackCooldownTime"]
        self._set_abilities(player_hero_data)

    def _set_abilities(self, data: IPlayerHero):
        self._abilities = []

        ability_id = 0
        for abilityData in data["abilities"].values():
            ability = Ability(str(ability_id))
            ability.update(abilityData)
            self._abilities.append(ability)
            ability_id += 1

    def set_time_of_death(self, time: float) -> None:
        self._time_of_death = time

    def get_buyback_cooldown_time_remaining(self) -> float:
        if self._alive:
            return 0

        time_elapsed_since_death = time() - self._time_of_death
        return self._buyback_cooldown_time - time_elapsed_since_death

    def get_command(self) -> dict[str, Any]:
        return self.command

    def get_courier_id(self) -> str:
        return self._courier_id

    def get_buyback_cost(self) -> int:
        return self._buyback_cost

    def get_buyback_cooldown_time(self) -> float:
        return self._buyback_cooldown_time

    def get_ability_points(self) -> int:
        return self._ability_points

    def get_abilities(self) -> list[Ability]:
        return self._abilities

    def get_items(self) -> list[Item]:
        return self._items

    def get_denies(self) -> int:
        return self._denies

    def get_gold(self) -> int:
        return self._gold

    def get_xp(self) -> int:
        return self._xp

    def clear_and_archive_command(self) -> None:
        if self.command:
            self.commands.append(self.command)
            self.command = None

    def attack(self, target_id: str) -> None:
        self.command = {
            self.get_name(): {
                "command": "ATTACK",
                "target": target_id
            }
        }

    def move(self, x: float, y: float, z: float) -> None:
        self.command = {
            self.get_name(): {
                "command": "MOVE",
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast(self, ability_index: int, target=-1, position=(-1, -1, -1)) -> None:
        x, y, z = position
        self.command = {
            self.get_name(): {
                "command": "CAST",
                "ability": ability_index,
                "target": target,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def use_glyph_of_fortification(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "GLYPH"
            }
        }

    def buy(self, item: str) -> None:
        self.command = {self.get_name(): {"command": "BUY", "item": item}}

    def sell(self, slot: int) -> None:
        self.command = {self.get_name(): {"command": "SELL", "slot": slot}}

    def use_item(self, slot: int, target=-1, position=(-1, -1, -1)) -> None:
        x, y, z = position
        self.command = {
            self.get_name(): {
                "command": "USE_ITEM",
                "slot": slot,
                "target": target,
                "x": x,
                "y": y,
                "z": z
            }
        }
    
    def disassemble_item(self, slot: int) -> None:
        self.command = {
            self.get_name(): {
                "command": "DISASSEMBLE",
                "slot": slot
            }
        }

    def unlock_item(self, slot: int) -> None:
        self.command = {
            self.get_name(): {
                "command": "UNLOCK_ITEM",
                "slot": slot
            }
        }

    def lock_item(self, slot: int) -> None:
        self.command = {
            self.get_name(): {
                "command": "LOCK_ITEM",
                "slot": slot
            }
        }

    def pick_up_rune(self, target_id: str) -> None:
        self.command = {
            self.get_name(): {
                "command": "PICK_UP_RUNE",
                "target": target_id
            }
        }

    def level_up(self, ability_index: int) -> None:
        self.command = {
            self.get_name(): {
                "command": "LEVELUP",
                "abilityIndex": ability_index
            }
        }

    def noop(self) -> None:
        self.command = {self.get_name(): {"command": "NOOP"}}

    def cast_toggle(self, ability_index: int) -> None:
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TOGGLE",
                "ability": ability_index,
            }
        }

    def cast_no_target(self, ability_index: int) -> None:
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_NO_TARGET",
                "ability": ability_index,
            }
        }

    def cast_target_point(self, ability_index: int, position: Position) -> None:
        x, y, z = position
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_NO_TARGET",
                "ability": ability_index,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast_target_area(self, ability_index: int, position: Position) -> None:
        x, y, z = position
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_AREA",
                "ability": ability_index,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast_target_unit(self, ability_index: int, target_id: str) -> None:
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_UNIT",
                "ability": ability_index,
                "target": target_id
            }
        }

    def cast_vector_targeting(self, ability_index: int, position: Position) -> None:
        x, y, z = position
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_VECTOR_TARGETING",
                "ability": ability_index,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast_target_unit_aoe(self, ability_index: int, target_id: str) -> None:
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_UNIT_AOE",
                "ability": ability_index,
                "target": target_id
            }
        }

    def cast_combo_target_point_unit(self, ability_index: int, target=-1, position=(-1, -1, -1)) -> None:
        x, y, z = position
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_COMBO_TARGET_POINT_UNIT",
                "ability": ability_index,
                "target": target,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def buyback(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "BUYBACK"
            }
        }

    def courier_stop(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "COURIER_STOP"
            }
        }

    def courier_retrieve(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "COURIER_RETRIEVE"
            }
        }

    def courier_secret_shop(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "COURIER_SECRET_SHOP"
            }
        }

    def courier_return_items(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "COURIER_RETURN_ITEMS"
            }
        }

    def courier_speed_burst(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "COURIER_SPEED_BURST"
            }
        }

    def courier_transfer_items(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "COURIER_TRANSFER_ITEMS"
            }
        }

    def courier_shield(self) -> None:
        self.command = {
            self.get_name(): {
                "command": "COURIER_SHIELD"
            }
        }

    def courier_move_to_position(self, x: float, y: float, z: float=384.00) -> None:
        # 384 is the z value at ground level.
        self.command = {
            self.get_name(): {
                "command": "COURIER_MOVE_TO_POSITION",
                "x": x,
                "y": y,
                "z": z
            }
        }

    def courier_sell(self, slot: int) -> None:
        self.command = {
            self.get_name(): {
                "command": "COURIER_SELL",
                "slot": slot
            }
        }

    def get_type(self) -> EntityType:
        return EntityType.PLAYER_HERO
