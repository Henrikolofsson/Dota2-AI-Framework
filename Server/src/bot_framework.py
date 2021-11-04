#!/usr/bin/env python3
from __future__ import annotations
from typing import Any
from game.post_data_interfaces.IRoot import IRoot
from game.world import World


class BotFramework:
    bot_class: type
    world: World
    agent: Any
    initialized: bool

    def __init__(self, bot_class: type, team: int) -> None:
        self.bot_class = bot_class
        self.world = World(team)
        self.team = team
        self.agent = bot_class(self.world, team)
        self.initialized = False

    def get_party(self) -> list[str]:
        return self.agent.party

    def update(self, data: IRoot) -> None:
        self.world.update(data["entities"])

    def generate_bot_commands(self) -> None:
        if not self.initialized:
            self.agent.initialize(self.world.get_player_heroes())
            self.initialized = True

        for hero in self.world.get_player_heroes():
            self.agent.actions(hero)

    def receive_bot_commands(self) -> list[dict[str, Any]]:
        commands: list[dict[str, Any]] = []

        for hero in self.world.get_player_heroes():
            command: dict[str, Any] = hero.get_command()
            if command:
                commands.append(command)
                hero.clear_and_archive_command()
        return commands

    def create_new_bot_framework(self) -> BotFramework:
        return BotFramework(self.bot_class, self.team)
