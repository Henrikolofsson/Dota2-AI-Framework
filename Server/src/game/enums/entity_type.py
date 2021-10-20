from enum import Enum, unique

@unique
class EntityType(Enum):
    ABILITY = 0
    BUILDING = 1
    HERO = 2
    ITEM = 3
    PHYSICAL_ENTITY = 4
    PLAYER_HERO = 5
    TOWER = 6
    TREE = 7
    UNIT = 8
    COURIER = 9
