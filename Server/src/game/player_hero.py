#!/usr/bin/env python3

from typing import Any, cast
from game.position import Position
from game.post_data_interfaces.IHero import IHero
from game.post_data_interfaces.IEntity import IEntity
from game.item import Item
from game.enums.entity_type import EntityType
from game.hero import Hero


class PlayerHero(Hero):

    _items: list[Item]

    def __init__(self, entity_id: str):
        super().__init__(entity_id)
        self.commands = [
            "ATTACK",
            "MOVE",
            "CAST",
            "BUY",
            "SELL",
            "USE_ITEM",
            "DISASSEMBLE",
            "UNLOCK_ITEM",
            "LOCK_ITEM"
            "PICK_UP_RUNE"
            "LEVELUP",
            "NOOP",
        ]
        self.command = None
        self.commands = []

    def update(self, data: IEntity):
        super().update(data)
        player_hero_data: IHero = cast(IHero, data)
        self._set_items(player_hero_data)

    def _set_items(self, player_hero_data: IHero) -> None:
        self._items = []

        item_id = 0
        for item_data in player_hero_data["items"].values():
            if isinstance(item_data, list):
                continue
            item = Item(str(item_id))
            item.update(item_data)
            self._items.append(item)
            item_id += 1

    def get_command(self) -> dict[str, Any]:
        return self.command

    def get_items(self) -> list[Item]:
        return self._items

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

    def cast_target_point(self, ability_index: int, position) -> None:
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

    def cast_target_unit(self, ability_index: int, target) -> None:
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_UNIT",
                "ability": ability_index,
                "target": target
            }
        }

    def cast_vector_targeting(self, ability_index: int, position) -> None:
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

    def cast_target_unit_aoe(self, ability_index: int, target) -> None:
        self.command = {
            self.get_name(): {
                "command": "CAST_ABILITY_TARGET_UNIT_AOE",
                "ability": ability_index,
                "target": target
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

    def get_type(self) -> EntityType:
        return EntityType.PLAYER_HERO
