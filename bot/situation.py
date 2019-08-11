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

import logging

root_logger = logging.getLogger()

class Situation:
    def __init__(self, AI: sc2.BotAI, isChatAllowed: bool = False):
        self.iteration = 0
        self.enemyRace: Race  = AI.enemy_race
        self.supplyBlocked = False
        self.AI: sc2.BotAI = AI
        #self._knownEnemyUnitsWorkers: Units = Units([])
        self.supplyLeft = 1

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

        #self.updateEnemy()

    #@property
    #def knownEnemyWorkers(self) -> Units:
        #return self._knownEnemyUnitsWorkers

    #def updateEnemy(self):
        #if self.enemyRace == Race.Random:
            #if self._knownEnemyUnitsWorkers(UnitTypeId.SCV).exists:
                #self.enemyRace = Race.Terran
            #if self._knownEnemyUnitsWorkers(UnitTypeId.DRONE).exists:
                #self.enemyRace = Race.Zerg
            #if self._knownEnemyUnitsWorkers(UnitTypeId.PROBE).exists:
                #self.enemyRace = Race.Protoss
