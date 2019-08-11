#Файл, отвечающий за знания бота

#Основные библеотеки StarCraft2
import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.ids.buff_id import BuffId
from sc2.player import Bot, Computer, Human
from sc2.bot_ai import CanAffordWrapper
from sc2.data import Result
from sc2.game_info import Ramp
from sc2.position import Point2
from sc2.unit import Unit, UnitOrder
from sc2.units import Units

class Situation:
    def __init__(self, AI: sc2.BotAI, isChatAllowed: bool = False):
        self.iteration = 0
        self.enemyRace = Race(self._game_info.player_races[self.enemy_id])
        self.supplyBlocked = False
        self.AI: sc2.BotAI = AI
        self.supplyLeft = 1
        self.enemyRaceStr = "None"

        if self.player_id == 1:
            self.enemy_id = 2
        else:
            self.enemy_id = 1

    async def update(self, interation: int):
        self.iteration = interation

        try:
            self.supplyLeft = self.AI.supply_left
        except:
            pass

        if not self.supplyBlocked and self.supplyLeft <= 0:
            self.supplyBlocked = True
        elif self.supplyBlocked and self.supplyLeft > 0:
            self.supplyBlocked = False

        self.knownEnemyRace()

    def knownEnemyRace(self):
        if self.enemyRace == Race.Random:
            self.enemyRaceStr = "Неизвестно"
        elif self.enemyRace == Race.Terran:
            self.enemyRaceStr = "Терран"
        elif self.enemyRace == Race.Protoss:
            self.enemyRaceStr = "Протос"
        elif self.enemyRace == Race.Zerg:
            self.enemyRaceStr = "Зерг"
