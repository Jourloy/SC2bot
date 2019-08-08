# Бот-протос для Starcraft 2
VERSION = 'v0.1'
AUTHOR = 'Jourloy'

#Основные библеотеки StarCraft2
import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

#Другие библеотеки
import os
import hues

class Orange_Cat(sc2.BotAI):
    async def on_step(self, iteration):
        #Сообщения в чат
        if iteration == 0:
            await self.chat_send("Orange_Cat "+ VERSION)
        if iteration == 30:
            await self.chat_send("(glhf)")

        #
        if not self.units(NEXUS).ready.exists:
            for worker in self.workers:
                await self.do(worker.attack(self.enemy_start_locations[0]))
            return
        else:
            nexus = self.units(NEXUS).ready.random

        #Добыча минералов свободными пробками
        for idle_worker in self.workers.idle:
            mf = self.state.mineral_field.closest_to(idle_worker)
            await self.do(idle_worker.gather(mf))

if __name__ == '__main__':
    sc2.run_game(sc2.maps.get("CyberForestLE"), [
        Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat"),
        Computer(Race.Protoss, Difficulty.Easy)
    ], realtime=True)
