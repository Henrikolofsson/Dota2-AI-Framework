from game.post_data_interfaces.IEntity import IEntity

class IAbility(IEntity):
    targetFlags: int
    targetTeam: int
    abilityDamageType: int
    toggleState: bool
    abilityDamage: int
    behavior: int
    abilityType: int
    maxLevel: int
    cooldownTimeRemaining: float
    cooldownTime: float
    targetType: int
    abilityIndex: int
    type: str
    name: str
    level: int