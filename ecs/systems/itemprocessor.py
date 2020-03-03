from esper import Processor

from constants import DijkstraMap
from ecs.components.item import Item
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.map import Map
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.position import Position
from functions import dijkstra_map


class ItemProcessor(Processor):
    def process(self):
        _, game_map = next(iter(self.world.get_component(Map)))
        _, player = next(iter(self.world.get_component(Player)))

        event = player.action

        if event and event.name == "pickup":
            self.world.remove_component(event.data["item"], Position)
            self.world.remove_component(event.data["item"], LastKnownPosition)
            self.world.create_entity(Message("You pick up something."))

        _, game_map = next(iter(self.world.get_component(Map)))

        sources = []
        for entity, (position, item) in self.world.get_components(Position, Item):
            if game_map.explored[position.y][position.x]:
                sources.append((position.x, position.y))

        game_map.dijkstra[DijkstraMap.ITEM] = dijkstra_map(game_map, sources)
