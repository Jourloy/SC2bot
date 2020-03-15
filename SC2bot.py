# BOT for STARCRAFT 2
VERSION = 'v0.1'
AUTHOR = 'Jourloy'

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

from Brain import controlFile

class HIVE(sc2.BotAI):
    def __init__(self):
        self.builders = []
        self.spawnOverlords = 0
        self.overlordAmount = 0

        self.pool = False

    #Print current game information
    async def logging(self):
        os.system("clear")
        print(f"""
----------
MINERALS: {self.minerals} | VESPENE: {self.vespene}

SUPPLY: {self.supplyLeft} ({self.supply_used} / {self.supply_cap}) | OVERLORDS: {self.overlords.amount} (+{self.spawnOverlords})

{self.expansion_locations[}
----------
        """)

    #Return your units
    async def getUnits(self):
        self.drone = self.units(DRONE)
        self.larva = self.units(LARVA)
        self.overlords = self.units(OVERLORD)
        self.egg = self.units(EGG)
        self.zergling = self.units(ZERGLING)

    #Return your structures
    async def getStructures(self):
        self.pool = self.units(SPAWNINGPOOL)

    #Return supply left
    async def getSupplyLeft(self):
        self.supplyLeft = self.supply_left

        if (self.spawnOverlords > 0 and self.overlords.amount < self.overlordAmount + self.spawnOverlords):
            self.supplyLeft += 8 * self.spawnOverlords
        elif (self.overlords.amount >= self.overlordAmount + self.spawnOverlords):
            self.overlordAmount = 0
            self.spawnOverlords = 0

    #Spawn overlord if can
    async def spawnOverlord(self):
        if (self.can_afford(OVERLORD) and self.larva.exists):
            await self.do(self.larva.random.train(OVERLORD))
            self.spawnOverlords += 1
            self.overlordAmount = self.overlords.amount

    #Split the workers
    async def splitWorkers(self):
        for drone in self.drones:
            if (drone not in self.builders):
                self.add_action(drone.gather(self.state.mineral_field.closest_to(drone)))

    async def attackZegling(self):
        for zerg in self.zergling:
            await self.do(zerg.attack(self.enemy_start_locations[0]))
        
    async def on_start(self):
        os.system("clear")

    #Main module
    async def on_step(self, iteration):
        await self.getUnits()
        await self.getStructures()
        await self.getSupplyLeft()

        self.splitWorkers()
        
        if (self.zergling.amount > 0):
            await self.attackZegling()

        if (self.supplyLeft <= 4 and self.supply_cap != 200 and self.pool):
            await self.spawnOverlord()

        if (not self.pool.exists and self.already_pending(SPAWNINGPOOL) == 0):
            if (len(self.builders) < 1):
                self.builders.append(self.drone.random)
            await controlFile.ControlClass.placeBuilding(self, SPAWNINGPOOL, self.builders[0])
        
        if (not self.pool.exists and self.already_pending(HATCHERY) == 0):
            if (len(self.builders) < 1):
                self.builders.append(self.drone.random)
            await controlFile.ControlClass.placeBuilding(self, HATCHERY, self.builders[0])
        
        if (self.pool.exists and self.townhalls.random.assigned_harvesters < self.townhalls.random.ideal_harvesters and self.larva.exists):
            if (self.townhalls.random.assigned_harvesters < 14 and self.zergling.amount < 4):
                if (self.can_afford(DRONE)):
                    await self.do(self.larva.random.train(DRONE))
            elif (self.townhalls.random.assigned_harvesters >= 14 and self.zergling.amount < 4):
                if (self.can_afford(ZERGLING)):
                    await self.do(self.larva.random.train(ZERGLING))
            elif (self.townhalls.random.assigned_harvesters >= 14 and self.zergling.amount > 4):
                if (self.can_afford(DRONE)):
                    await self.do(self.larva.random.train(DRONE))
        else:
            if (self.larva.exists):
                if (self.can_afford(ZERGLING)):
                    await self.do(self.larva.random.train(ZERGLING))

        if (self.minerals > 320):
            if (len(self.builders) < 1):
                    self.builders.append(self.drone.random)
            if (self.can_afford(HATCHERY)):
                for i in self.expansion_locations:
                    positionTar = await self.find_placement(HATCHERY, i, max_distance=20)
                    if (await self.can_place(HATCHERY, positionTar)):
                        self.pos = positionTar
                        break
                
                await self.build(HATCHERY, self.pos, unit=self.builders[0])
        
        await self.logging()

if __name__ == "__main__":
    sc2.run_game(sc2.maps.get("WorldofSleepersLE"), [
        Bot(Race.Zerg, HIVE(), name="HIVE"),
        Computer(Race.Random, Difficulty.Medium)
    ], realtime=False)