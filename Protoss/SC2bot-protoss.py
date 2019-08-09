# Бот-протос для Starcraft 2
VERSION = 'v0.1'
AUTHOR = 'Jourloy'

#Основные библеотеки StarCraft2
import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.ids.buff_id import BuffId
from sc2.player import Bot, Computer

#Другие библеотеки
import os
import hues

class Orange_Cat(sc2.BotAI):
    async def on_step(self, iteration):
        #Сообщения в чат
        if iteration == 0:
            await self.chat_send("Orange_Cat-SC2bot-prtoss "+ VERSION)
        if iteration == 30:
            await self.chat_send("(glhf)")

        #Если NEXUS сломан - все пробки идут в атаку
        if not self.units(NEXUS).ready.exists:
            for worker in self.workers:
                await self.do(worker.attack(self.enemy_start_locations[0]))
                await self.chat_send("(gg)")
            return
        else:
            nexus = self.units(NEXUS).ready.random

        #Постройка пилона если supply меньше двух
        if self.supply_left < 2 and not self.already_pending(PYLON):
            if self.can_afford(PYLON):
                await self.build(PYLON, near=nexus)
            return

        #Заказ пробки
        if self.workers.amount < self.units(NEXUS).amount*15 and nexus.noqueue:
            if self.can_afford(PROBE):
                #Баф NEXUS
                if not nexus.has_buff(BuffId.CHRONOBOOSTENERGYCOST):
                    abilities = await self.get_available_abilities(nexus)
                    if AbilityId.EFFECT_CHRONOBOOSTENERGYCOST in abilities:
                        await self.do(nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus))
                await self.do(nexus.train(PROBE))
        #Постройка пилона
        elif not self.units(PYLON).exists and not self.already_pending(PYLON):
            if self.can_afford(PYLON):
                await self.build(PYLON, near=nexus)

        #Добыча минералов свободными пробками
        for idle_worker in self.workers.idle:
            mf = self.state.mineral_field.closest_to(idle_worker)
            await self.do(idle_worker.gather(mf))

        #Постройка NEXUS'ов
        if self.units(NEXUS).amount < 3 and not self.already_pending(NEXUS):
            if self.can_afford(NEXUS):
                await self.expand_now()

if __name__ == '__main__':
    sc2.run_game(sc2.maps.get("CyberForestLE"), [
        Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat"),
        Computer(Race.Protoss, Difficulty.Easy)
    ], realtime=True)
