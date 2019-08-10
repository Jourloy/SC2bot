# Бот-протос для Starcraft 2
VERSION = 'v0.1'
AUTHOR = 'Jourloy'

#Основные библеотеки StarCraft2
import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.ids.buff_id import BuffId
from sc2.player import Bot, Computer, Human

#Основные библеотеки бота
from bot import situation
from bot import manager

#Другие библеотеки
import os
import hues

class Orange_Cat(sc2.BotAI):
    def __init__(self):
        super().__init__()
        self.situation = situation.Situation(sc2.BotAI)
        self.manager = manager.Manager(sc2.BotAI)
        self.actions = []

    def printInfo(self):
        if self.situation.supplyBlocked:
            supplyBlock = "ДА"
        else:
            supplyBlock = "НЕТ"
        os.system('cls')
        print("----------------------------------------------------------- ")
        print("Основная информация")
        print("Время в секундах: {}".format(str(round(self.time))))
        print("Раса противника: {}".format(str(self.situation.enemyRace)))
        print("Сапплай блок: {}".format(supplyBlock))
        print("\nРесурсы")
        print("Минералов: {}".format(str(self.minerals)))
        print("Газа: {}".format(str(self.vespene)))
        print("\nЮниты")
        print("Рабов: {}".format(str(self.workers.amount)))
        print("----------------------------------------------------------- ")
        for x in self.actions:
            pass

    async def on_step(self, iteration):
        if iteration > 0:
            await self.situation.update(iteration)

        #Сообщения в чат
        if iteration == 0:
            await self.chat_send("Orange_Cat "+ VERSION)
        if iteration == 30:
            await self.chat_send("glhf")

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

        #
        Orange_Cat.printInfo(self)

if __name__ == '__main__':
    os.system('cls')
    try:
        print("Выберите режим:")
        print("1 - играть самому против бота \n2 - Бот против бота\n\n")
        answer = str(input("Ответ: "))
    except:
        pass
    if answer == "1":
        try:
            os.system('cls')
            userName = str(input("Введите свой ник: "))
            os.system('cls')
            print("Выберите свою расу:")
            print("1 - Protoss")
            print("2 - Zerg")
            print("3 - Terran")
            print("4 - Random\n\n")
            answer = str(input("Ответ: "))
        except:
            pass
        if answer == "1":
            sc2.run_game(sc2.maps.get("CyberForestLE"), [
                Human(Race.Protoss, name=userName),
                Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat")
            ], realtime=True)
        elif answer == "2":
            sc2.run_game(sc2.maps.get("CyberForestLE"), [
                Human(Race.Zerg, name=userName),
                Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat")
            ], realtime=True)
        elif answer == "3":
            sc2.run_game(sc2.maps.get("CyberForestLE"), [
                Human(Race.Terran, name=userName),
                Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat")
            ], realtime=True)
        elif answer == "4":
            sc2.run_game(sc2.maps.get("CyberForestLE"), [
                Human(Race.Random, name=userName),
                Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat")
            ], realtime=True)
        else:
            print("Ошибка")
    elif answer == "2":
        try:
            os.system('cls')
            print("Выберите расу бота-противника:")
            print("1 - Protoss")
            print("2 - Zerg")
            print("3 - Terran")
            print("4 - Random\n\n")
            answer = str(input("Ответ: "))
        except:
            pass
        if answer == "1":
            sc2.run_game(sc2.maps.get("CyberForestLE"), [
                Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat"),
                Computer(Race.Protoss, Difficulty.Easy)
            ], realtime=True)
        elif answer == "2":
            sc2.run_game(sc2.maps.get("CyberForestLE"), [
                Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat"),
                Computer(Race.Zerg, Difficulty.Easy)
            ], realtime=True)
        elif answer == "3":
            sc2.run_game(sc2.maps.get("CyberForestLE"), [
                Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat"),
                Computer(Race.Terran, Difficulty.Easy)
            ], realtime=True)
        elif answer == "4":
            sc2.run_game(sc2.maps.get("CyberForestLE"), [
                Bot(Race.Protoss, Orange_Cat(), name="Orange_Cat"),
                Computer(Race.Random, Difficulty.Easy)
            ], realtime=True)
        else:
            print("Ошибка")
