#!/usr/bin/env python3
from __future__ import annotations
from typing import Union
from base_bot import BaseBot
from game.post_data_interfaces.IRoot import IRoot
from game.world import World
from game.player_hero import CommandProps


class BotFramework:
    bot_class: type
    world: World
    agent: BaseBot
    initialized: bool

    def __init__(self, bot_class: type, team: int) -> None:
        self.bot_class = bot_class
        self.world = World(team)
        self.team = team
        self.agent = bot_class(self.world, team)
        self.initialized = False

    def get_party(self) -> list[str]:
        if len(self.agent.get_party()) > 5:
            raise Exception("Invalid party: list contains too many hero names.")
        if len(self.agent.get_party()) < 5:
            raise Exception("Invalid party: list contains too few hero names.")
        if len(set(self.agent.get_party())) != 5:
            raise Exception("Invalid party: list contains duplicate hero names.")
        return self.agent.get_party()

    def update_and_receive_commands(self, data: IRoot) -> list[dict[str, CommandProps]]:
        self.update(data)
        self.generate_bot_commands()
        commands = self.receive_bot_commands()
        return commands

    def update(self, data: IRoot) -> None:
        self.world.update(data["entities"])

    def generate_bot_commands(self) -> None:
        if not self.initialized:
            self.agent.initialize(self.world.get_player_heroes())
            self.initialized = True

        for hero in self.world.get_player_heroes():
            self.agent.actions(hero)

    def receive_bot_commands(self) -> list[dict[str, CommandProps]]:
        commands: list[dict[str, CommandProps]] = []

        for hero in self.world.get_player_heroes():
            command: Union[dict[str, CommandProps], None] = hero.get_command()
            if command:
                commands.append(command)
                hero.clear_and_archive_command()
        return commands

    def create_new_bot_framework(self) -> BotFramework:
        return BotFramework(self.bot_class, self.team)
