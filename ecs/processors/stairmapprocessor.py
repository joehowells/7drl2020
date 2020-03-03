from esper import Processor, World

from constants import DijkstraMap
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.stair import Stair
from functions import dijkstra_map


class StairMapProcessor(Processor):
    def process(self):
        self.world: World

        _, game_map = next(iter(self.world.get_component(Map)))

        sources = []
        for _, (position, item) in self.world.get_components(LastKnownPosition, Stair):
            sources.append((position.x, position.y))

        game_map.dijkstra[DijkstraMap.ITEM] = dijkstra_map(game_map, sources)
