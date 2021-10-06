#!/usr/bin/env python3

from src.game.PhysicalEntity import PhysicalEntity


class Tree(PhysicalEntity):

    def get_type(self) -> str:
        return "Tree"