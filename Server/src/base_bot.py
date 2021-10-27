from abc import ABC, abstractmethod
from game.player_hero import PlayerHero


class BaseBot(ABC):
    @abstractmethod
    def initialize(self, heroes: list[PlayerHero]) -> None:
        pass

    @abstractmethod
    def actions(self, hero: PlayerHero) -> None:
        pass


