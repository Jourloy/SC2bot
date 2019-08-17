#Основные библеотеки StarCraft2
import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.ids.buff_id import BuffId
from sc2.player import Bot, Computer, Human
from sc2.bot_ai import *
from sc2.data import Result
from sc2.game_info import *
from sc2.position import Point2
from sc2.unit import Unit, UnitOrder
from sc2.units import Units

class situation(sc2.BotAI):
    def __init__(self):
        self.iteration = None
        self.enemyRace = None
        self.enemyRaceStr = None
        self.supplyBlocked = False
        self.supply_left = sc2.BotAI.supply_left

    def update(self, iteration):
        self.iteration = iteration

        if self.enemyRace == None:
            self.enemyRace = self.enemy_race

        if not self.supplyBlocked and self.supply_left <= 1:
            self.supplyBlocked = True
        elif self.supplyBlocked and self.supply_left > 1:
            self.supplyBlocked = False

        if self.enemyRace == Race.Random and self.enemyRaceStr == None:
            self.enemyRaceStr = "Неизвестно"
        elif self.enemyRace == Race.Terran and self.enemyRaceStr == None:
            self.enemyRaceStr = "Терран"
        elif self.enemyRace == Race.Protoss and self.enemyRaceStr == None:
            self.enemyRaceStr = "Протос"
        elif self.enemyRace == Race.Zerg and self.enemyRaceStr == None:
            self.enemyRaceStr = "Зерг"
