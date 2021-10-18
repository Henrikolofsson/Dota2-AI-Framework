#!/usr/bin/env python3
from typing import Any
from game.post_data_interfaces.IRoot import IRoot
from game.world import World

class BotFramework:
    
    world: World
    agent: Any
    initialized: bool

    def __init__(self, BotClass: type, team: int) -> None:
        self.world = World(team)
        self.agent = BotClass(self.world, team)
        self.initialized = False

    def get_party(self) -> list[str]:
        return self.agent.party

    def update(self, data: IRoot) -> None:
        self.world.update(data["entities"])

    def generate_bot_commands(self) -> None:
        if self.initialized:
            for hero in self.world.get_player_heroes():
                self.agent.actions(hero)
        else:
            self.agent.initialize(self.world.get_player_heroes())
            self.initialized = True

    def receive_bot_commands(self) -> list[dict[str, Any]]:
        commands: list[dict[str, Any]] = []

        for hero in self.world.get_player_heroes():
            command: dict[str, Any] = hero.get_command()
            if command:
                commands.append(command)
                hero.clear_and_archive_command()
        return commands
