#!/usr/bin/env python3

from typing import cast
from game.enums.entity_type import EntityType
from game.post_data_interfaces.IAbility import IAbility
from game.post_data_interfaces.IEntity import IEntity
from game.BaseEntity import BaseEntity


class Ability(BaseEntity):
    _targetFlags: int
    _targetTeam: int
    _abilityDamageType: int
    _toggleState: bool
    _abilityDamage: int
    _behavior: int
    _abilityType: int
    _maxLevel: int
    _cooldownTimeRemaining: float
    _cooldownTime: float
    _targetType: int
    _abilityIndex: int
    _type: str
    _name: str
    _level: int


    def update(self, data: IEntity):
        super().update(data)
        ability_data: IAbility = cast(IAbility, data)
        self._targetFlags = ability_data["targetFlags"]
        self._targetTeam = ability_data["targetTeam"]
        self._abilityDamageType = ability_data["abilityDamageType"]
        self._toggleState = ability_data["toggleState"]
        self._abilityDamage = ability_data["abilityDamage"]
        self._behavior = ability_data["behavior"]
        self._abilityType = ability_data["abilityType"]
        self._maxLevel = ability_data["maxLevel"]
        self._cooldownTimeRemaining = ability_data["cooldownTimeRemaining"]
        self._cooldownTime = ability_data["cooldownTime"]
        self._abilityIndex = ability_data["abilityIndex"]
        self._type = ability_data["type"]
        self._name = ability_data["name"]

    def getAbilityDamage(self) -> int:
        return self.data["abilityDamage"]

    def getAbilityDamageType(self) -> int:
        return self.data["abilityDamageType"]

    def getAbilityIndex(self) -> int:
        return self.data["abilityIndex"]

    def getAbilityType(self) -> int:
        return self.data["abilityType"]

    def getBehavior(self) -> int:
        return self.data["behavior"]

    def getCooldownTime(self) -> float:
        return self.data["cooldownTime"]

    def getCooldownTimeRemaining(self) -> float:
        return self.data["cooldownTimeRemaining"]

    def getLevel(self) -> int:
        return self.data["level"]

    def getMaxLevel(self) -> int:
        return self.data["maxLevel"]

    def getTargetFlags(self) -> int:
        return self.data["targetFlags"]

    def getTargetTeam(self) -> int:
        return self.data["targetTeam"]

    def getTargetType(self) -> int:
        return self.data["targetType"]

    def getToggleState(self) -> bool:
        return self.data["toggleState"]

    def get_type(self) -> EntityType:
        return EntityType.ABILITY