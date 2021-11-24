from game.post_data_interfaces.IAbility import IAbility
from game.post_data_interfaces.IHero import IHero

class IPlayerHero(IHero):
    denies: int
    abilityPoints: int
    abilities: dict[str, IAbility]
    xp: int
    gold: int
    courier_id: str
    buybackCost: int
    buybackCooldownTime: float
    tpScrollAvailable: bool
    tpScrollCooldownTime: float
