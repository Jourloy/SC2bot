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

import os

class ControlClass():
    def __init__(self):
        self.builders = []

    async def calculatePos(self, building, tar1, tar2):
        if (building == HATCHERY):
            pass
        positionTar = await self.find_placement(building, tar1.position, max_distance=20)
        pos = positionTar.is_closer_than(20, tar2)
        dist = 20
        dist2 = 20
        while (pos):
            positionTar = await self.find_placement(building, tar1.position, max_distance=dist)
            pos = positionTar.is_closer_than(dist2, tar2)
            dist += 2
            dist2 -= 0.1
            tar1 = self.drone.random
        check = await self.can_place(building, positionTar)
        if (check):
            return positionTar

    async def placeBuilding(self, building, drone):
        if (self.can_afford(building)):
            pos = await self.calculatePos(building, self.builders[0], self.townhalls.first)
            await self.build(building, pos, unit=self.builders[0])
