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

class tactics(sc2.BotAI):
    def __init__(self):
        
