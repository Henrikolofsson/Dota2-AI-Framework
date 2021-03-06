from enum import Enum

class AbilityBehavior(Enum):
    NONE = 0
    HIDDEN = 1
    PASSIVE = 2
    NO_TARGET = 4
    UNIT_TARGET = 8
    POINT = 16
    AOE = 32
    NOT_LEARNABLE = 64
    CHANNELLED = 128
    ITEM = 256
    TOGGLE = 512
    DIRECTIONAL = 1024
    IMMEDIATE = 2048
    AUTOCAST = 4096
    OPTIONAL_UNIT_TARGET = 8192
    OPTIONAL_POINT = 16384
    OPTIONAL_NO_TARGET = 32768
    AURA = 65536
    ATTACK = 131072
    DONT_RESUME_MOVEMENT = 262144
    ROOT_DISABLES = 524288
    UNRESTRICTED = 1048576
    IGNORE_PSEUDO_QUEUE = 2097152
    IGNORE_CHANNEL = 4194304
    DONT_CANCEL_MOVEMENT = 8388608
    DONT_ALERT_TARGET = 16777216
    DONT_RESUME_ATTACK = 33554432
    NORMAL_WHEN_STOLEN = 67108864
    IGNORE_BACKSWING = 134217728
    RUNE_TARGET = 268435456
    DONT_CANCEL_CHANNEL = 536870912
    LAST_BEHAVIOR = 536870912