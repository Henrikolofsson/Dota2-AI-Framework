#!/usr/bin/env python3

from time import time
from typing import TypedDict, Union, cast
from game.physical_entity import PhysicalEntity
from game.ability import Ability
from game.post_data_interfaces.IPlayerHero import IPlayerHero
from game.position import Position
from game.post_data_interfaces.IHero import IHero
from game.post_data_interfaces.IEntity import IEntity
from game.item import Item
from game.enums.entity_type import EntityType
from game.hero import Hero


class CommandProps(TypedDict, total=False):
    command: str
    item: str
    slot: int
    slot1: int
    slot2: int
    ability: int
    target: str
    x: float
    y: float
    z: float


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
    _tp_scroll_available: bool
    _tp_scroll_cooldown_time: float
    _tp_scroll_charges: int
    _in_range_of_home_shop: bool
    _in_range_of_secret_shop: bool
    _items: list[Item]
    _stash_items: list[Item]

    _command: Union[dict[str, CommandProps], None]
    _commands: list[dict[str, CommandProps]]

    def __init__(self, entity_id: str):
        super().__init__(entity_id)
        self._command = None
        self._commands = []

    def update(self, data: IEntity) -> None:
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
        self._tp_scroll_available = player_hero_data["tpScrollAvailable"]
        self._tp_scroll_cooldown_time = player_hero_data["tpScrollCooldownTime"]
        self._tp_scroll_charges = player_hero_data["tpScrollCharges"]
        self._in_range_of_home_shop = player_hero_data["inRangeOfHomeShop"]
        self._in_range_of_secret_shop = player_hero_data["inRangeOfSecretShop"]
        self._set_items(player_hero_data)
        self._set_stash_items(player_hero_data)
        self._set_abilities(player_hero_data)

    def _set_items(self, player_hero_data: IPlayerHero) -> None:
        self._items = []

        item_id = 0
        for item_data in player_hero_data["items"].values():
            if isinstance(item_data, list):
                continue
            item = Item(str(item_id))
            item.update(item_data)
            self._items.append(item)
            item_id += 1

    def _set_stash_items(self, player_hero_data: IPlayerHero) -> None:
        self._stash_items = []

        item_id = 0
        for item_data in player_hero_data["stashItems"].values():
            if isinstance(item_data, list):
                continue
            item = Item(str(item_id))
            item.update(item_data)
            self._stash_items.append(item)
            item_id += 1

    def _set_abilities(self, player_hero_data: IPlayerHero) -> None:
        self._abilities = []

        ability_id = 0
        for ability_data in player_hero_data["abilities"].values():
            ability = Ability(str(ability_id))
            ability.update(ability_data)
            self._abilities.append(ability)
            ability_id += 1

    def set_time_of_death(self, time: float) -> None:
        self._time_of_death = time

    def is_in_range_of_home_shop(self) -> bool:
        return self._in_range_of_home_shop

    def is_in_range_of_secret_shop(self) -> bool:
        return self._in_range_of_secret_shop

    def get_buyback_cooldown_time_remaining(self) -> float:
        if self._alive:
            return 0

        time_elapsed_since_death = time() - self._time_of_death
        return self._buyback_cooldown_time - time_elapsed_since_death

    def get_command(self) -> Union[dict[str, CommandProps], None]:
        return self._command

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

    def get_stash_items(self) -> list[Item]:
        return self._stash_items

    def get_denies(self) -> int:
        return self._denies

    def get_gold(self) -> int:
        return self._gold

    def get_xp(self) -> int:
        return self._xp

    def is_tp_scroll_available(self) -> bool:
        return self._tp_scroll_available

    def get_tp_scroll_cooldown_time(self) -> float:
        return self._tp_scroll_cooldown_time

    def get_tp_scroll_charges(self) -> int:
        return self._tp_scroll_charges

    def clear_and_archive_command(self) -> None:
        if self._command:
            self._commands.append(self._command)
            self._command = None

    def attack(self, target: Union[str, PhysicalEntity]) -> None:
        if isinstance(target, PhysicalEntity):
            target = target.get_id()

        self._command = {
            self.get_name(): {
                "command": "ATTACK",
                "target": target
            }
        }

    def move(self, x: float, y: float, z: float = 0) -> None:
        self._command = {
            self.get_name(): {
                "command": "MOVE",
                "x": x,
                "y": y,
                "z": z
            }
        }

    def stop(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "STOP",
            }
        }

    def cast(self, ability_index: int, target: Union[str, PhysicalEntity] = "-1", position: Union[Position, None] = None) -> None:
        if position is None:
            position = Position(0, 0, 0)

        if isinstance(target, PhysicalEntity):
            target = target.get_id()

        x, y, z = position
        self._command = {
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
        self._command = {
            self.get_name(): {
                "command": "GLYPH"
            }
        }

    def use_tp_scroll(self, position: Position) -> bool:
        '''
        Use town portal on position.
        If position is not a legitimate teleport location, the closest valid teleport location is used instead.
        
        ---
        Returns `True` if town portal scroll is available, `False` otherwise.
        '''
        if not self._tp_scroll_available:
            return False

        x, y, z = position
        self._command = {
            self.get_name(): {
                "command": "TP_SCROLL",
                "x": x,
                "y": y,
                "z": z,
            }
        }

        return True

    def buy(self, item: str) -> None:
        self._command = {
            self.get_name(): {
                "command": "BUY",
                "item": item
            }
        }

    def sell(self, slot: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "SELL",
                "slot": slot
            }
        }

    def use_item(self, slot: int, target: Union[str, PhysicalEntity] = "-1", position: Union[Position, None] = None) -> None:
        if position is None:
            position = Position(0, 0, 0)

        if isinstance(target, PhysicalEntity):
            target = target.get_id()

        x, y, z = position
        self._command = {
            self.get_name(): {
                "command": "USE_ITEM",
                "slot": slot,
                "target": target,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def swap_item_slots(self, slot1: int, slot2: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "SWAP_ITEM_SLOTS",
                "slot1": slot1,
                "slot2": slot2,
            }
        }

    def toggle_item(self, slot: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "TOGGLE_ITEM",
                "slot": slot
            }
        }

    def disassemble_item(self, slot: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "DISASSEMBLE",
                "slot": slot
            }
        }

    def unlock_item(self, slot: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "UNLOCK_ITEM",
                "slot": slot
            }
        }

    def lock_item(self, slot: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "LOCK_ITEM",
                "slot": slot
            }
        }

    def pick_up_rune(self, target: Union[str, PhysicalEntity]) -> None:
        if isinstance(target, PhysicalEntity):
            target = target.get_id()

        self._command = {
            self.get_name(): {
                "command": "PICK_UP_RUNE",
                "target": target
            }
        }

    def level_up(self, ability_index: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "LEVEL_UP",
                "ability": ability_index
            }
        }

    def noop(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "NOOP"
            }
        }

    def cast_toggle(self, ability_index: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TOGGLE",
                "ability": ability_index,
            }
        }

    def cast_no_target(self, ability_index: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "CAST_ABILITY_NO_TARGET",
                "ability": ability_index,
            }
        }

    def cast_target_point(self, ability_index: int, position: Position) -> None:
        x, y, z = position
        self._command = {
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
        self._command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_AREA",
                "ability": ability_index,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast_target_unit(self, ability_index: int, target: Union[str, PhysicalEntity]) -> None:
        if isinstance(target, PhysicalEntity):
            target = target.get_id()

        self._command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_UNIT",
                "ability": ability_index,
                "target": target
            }
        }

    def cast_vector_targeting(self, ability_index: int, position: Position) -> None:
        x, y, z = position
        self._command = {
            self.get_name(): {
                "command": "CAST_ABILITY_VECTOR_TARGETING",
                "ability": ability_index,
                "x": x,
                "y": y,
                "z": z
            }
        }

    def cast_target_unit_aoe(self, ability_index: int, target: Union[str, PhysicalEntity]) -> None:
        if isinstance(target, PhysicalEntity):
            target = target.get_id()

        self._command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_UNIT_AOE",
                "ability": ability_index,
                "target": target
            }
        }

    def cast_combo_target_point_unit(self, ability_index: int, target: Union[str, PhysicalEntity] = "-1",
                                     position: Union[Position, None] = None) -> None:
        if position is None:
            position = Position(0, 0, 0)

        if isinstance(target, PhysicalEntity):
            target = target.get_id()

        x, y, z = position
        self._command = {
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
        self._command = {
            self.get_name(): {
                "command": "BUYBACK"
            }
        }

    def courier_stop(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "COURIER_STOP"
            }
        }

    def courier_retrieve(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "COURIER_RETRIEVE"
            }
        }

    def courier_secret_shop(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "COURIER_SECRET_SHOP"
            }
        }

    def courier_return_items(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "COURIER_RETURN_ITEMS"
            }
        }

    def courier_speed_burst(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "COURIER_SPEED_BURST"
            }
        }

    def courier_transfer_items(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "COURIER_TRANSFER_ITEMS"
            }
        }

    def courier_shield(self) -> None:
        self._command = {
            self.get_name(): {
                "command": "COURIER_SHIELD"
            }
        }

    def courier_move_to_position(self, x: float, y: float, z: float = 384.00) -> None:
        # 384 is the z value at ground level.
        self._command = {
            self.get_name(): {
                "command": "COURIER_MOVE_TO_POSITION",
                "x": x,
                "y": y,
                "z": z
            }
        }

    def courier_sell(self, slot: int) -> None:
        self._command = {
            self.get_name(): {
                "command": "COURIER_SELL",
                "slot": slot
            }
        }

    def get_type(self) -> EntityType:
        return EntityType.PLAYER_HERO
