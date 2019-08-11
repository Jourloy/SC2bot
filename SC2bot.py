# Бот-протос для Starcraft 2
VERSION = 'v0.1'
AUTHOR = 'Jourloy'

#Основные библеотеки StarCraft2
import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.ids.buff_id import BuffId
from sc2.player import Bot, Computer, Human
from sc2.bot_ai import CanAffordWrapper
from sc2.data import Result
from sc2.game_info import *
from sc2.position import Point2
from sc2.unit import Unit, UnitOrder
from sc2.units import Units

#Другие библеотеки
import os
import hues

class Orange_Cat(sc2.BotAI):
    def __init__(self):
        super().__init__()
        self.actions = []

        self.iteration = None
        self.enemyRaceStr = "None"
        self.supplyBlocked = False
        self.probescout = False
        self.probeguard = False
        self.scoutProbe = False

    def printInfo(self):
        if self.supplyBlocked:
            supplyBlock = "ДА"
        else:
            supplyBlock = "НЕТ"
        os.system('cls')
        print("----------------------------------------------------------- ")
        print("Основная информация")
        print("Время в секундах: {}".format(str(round(self.time))))
        print("Раса противника: {}".format(self.enemyRaceStr))
        print("Сапплай блок: {}".format(supplyBlock))
        print("\nРесурсы")
        print("Минералы: {}".format(str(self.minerals)))
        print("Газ: {}".format(str(self.vespene)))
        print("\nЮниты")
        print("Рабы: {}".format(str(self.workers.amount)))
        print("----------------------------------------------------------- ")
        for x in self.actions:
            print(x)

    async def update(self):

        if not self.supplyBlocked and self.supply_left <= 1:
            self.supplyBlocked = True
        elif self.supplyBlocked and self.supply_left > 1:
            self.supplyBlocked = False

        if self.enemyRace == Race.Random:
            self.enemyRaceStr = "Неизвестно"
        elif self.enemyRace == Race.Terran:
            self.enemyRaceStr = "Терран"
        elif self.enemyRace == Race.Protoss:
            self.enemyRaceStr = "Протос"
        elif self.enemyRace == Race.Zerg:
            self.enemyRaceStr = "Зерг"

    async def scouting(self):
        if not self.probescout:
            if not self.units(UnitTypeId.PROBE).ready:
                return
            probes = self.units(UnitTypeId.PROBE).ready
            for probe in probes:
                if probe.is_idle and probe.tag != self.probeguard:
                    self.probescout = probe.tag
                    return
        else:
            scout = self.units.find_by_tag(self.probescout)
            if not scout:
                self.probescout = False
                return
            else:
                for enemyStartLoc in list(self.enemy_start_locations):
                    self.microActions.append(scout.move(enemyStartLoc.position, queue=True))
                self.scoutProbe = True
                return

        await self.scoutroutine(scout)

    async def scoutroutine(self, scout):
        if not scout:
            return

        if scout.noqueue:
            for enemyStartLoc in list(self.enemy_start_locations):
                if scout.noqueue:
                    self.microActions.append(scout.move(enemyStartLoc.position, queue=True))
                    self.microActions.append(scout.move(self.state.mineral_field.random.position, queue=True))


    async def on_step(self, iteration):
        self.enemyRace = self.enemy_race
        self.microActions = []

        await self.update()

        #Сообщения в чат
        if iteration == 0:
            await self.chat_send("Orange_Cat "+ VERSION)
        if iteration == 30:
            await self.chat_send("glhf")

        if self.enemyRace == Race.Random:
            self.scouting()

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
                self.actions.append("Пилон")

        #Заказ пробки
        for nx in self.units(NEXUS):
            if nx.assigned_harvesters != nx.ideal_harvesters:
                if self.can_afford(PROBE):
                    #Баф NEXUS
                    if not nexus.has_buff(BuffId.CHRONOBOOSTENERGYCOST):
                        abilities = await self.get_available_abilities(nexus)
                        if AbilityId.EFFECT_CHRONOBOOSTENERGYCOST in abilities:
                            await self.do(nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus))
                    await self.do(nexus.train(PROBE))
                    self.actions.append("Пробка")

        #Постройка пилона
        if not self.units(PYLON).exists and not self.already_pending(PYLON):
            if self.can_afford(PYLON):
                await self.build(PYLON, near=nexus)
                self.actions.append("Пилон")


        #Добыча минералов свободными пробками
        if self.workers.idle and self.scoutProbe:
            for nx in self.units(NEXUS):
                if nx.assigned_harvesters != nx.ideal_harvesters:
                    for idle_worker in self.workers.idle:
                        mf = self.state.mineral_field.closest_to(nx)
                        await self.do(idle_worker.gather(mf))

        #Постройка NEXUS'ов
        if self.units(NEXUS).amount < 3 and not self.already_pending(NEXUS):
            if self.can_afford(NEXUS):
                await self.expand_now()
                self.actions.append("Нексус")

        await self.do_actions(self.microActions)
        #
        Orange_Cat.printInfo(self)

if __name__ == '__main__':
    os.system('cls')
    try:
        print("Выберите режим:")
        print("1 - Играть самому против бота \n2 - Бот против бота\n\n")
        answer = str(input("Ответ: "))
    except:
        pass
    if answer == "1":
        try:
            os.system('cls')
            userName = str(input("Введите свой ник: "))
            os.system('cls')
            print("Выберите свою расу:")
            print("1 - Протос")
            print("2 - Зерг")
            print("3 - Терран")
            print("4 - Случайно\n\n")
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
            print("1 - Протос")
            print("2 - Зерг")
            print("3 - Терран")
            print("4 - Случайно\n\n")
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
