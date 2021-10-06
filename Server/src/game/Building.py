#!/usr/bin/env python3

from src.game.Unit import Unit


class Building(Unit):

    def get_type(self) -> str:
        return "Building"