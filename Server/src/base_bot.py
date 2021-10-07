from abc import ABC, abstractmethod
from src.game.Hero import Hero


class BaseBot(ABC):
    @abstractmethod
    def initialize(self, heroes: list[Hero]) -> None:
        pass

    @abstractmethod
    def actions(self, hero: Hero) -> None:
        pass


