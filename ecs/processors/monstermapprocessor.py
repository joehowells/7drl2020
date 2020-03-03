from esper import Processor, World

from constants import DijkstraMap
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.monster import Monster
from functions import dijkstra_map


class MonsterMapProcessor(Processor):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))

        sources = []
        for _, (position, monster) in self.world.get_components(LastKnownPosition, Monster):
            sources.append((position.x, position.y))

        game_map.dijkstra[DijkstraMap.MONSTER] = dijkstra_map(game_map, sources)
