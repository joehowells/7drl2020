from esper import Processor, World

from action import ActionType
from ecs.components.equipment import Equipment
from ecs.components.inventory import Inventory
from ecs.components.item import Item
from ecs.components.lastknownposition import LastKnownPosition
from ecs.components.message import Message
from ecs.components.player import Player
from ecs.components.position import Position
from ecs.processors.spatialprocessor import Coincident


class GetItemProcessor(Processor):
    def process(self):
        self.world: World

        _, player = next(iter(self.world.get_component(Player)))

        if player.action.action_type is ActionType.GET_ITEM:
            for entity, (item, _) in self.world.get_components(Item, Coincident):
                for equipment in self.world.try_component(entity, Equipment):
                    self.world.delete_entity(entity, immediate=True)

                    if equipment is Equipment.WEAPON:

                        if player.attack_equip >= 9:
                            self.world.create_entity(Message(
                                text="You cannot upgrade your weapon any further."
                            ))
                        else:
                            player.attack_equip += 1
                            self.world.create_entity(Message(
                                text="You upgrade your weapon."
                            ))

                    if equipment is Equipment.ARMOUR:
                        if player.defend_equip >= 9:
                            self.world.create_entity(Message(
                                text="You cannot upgrade your armour any further!"
                            ))
                        else:
                            player.defend_equip += 1
                            self.world.create_entity(Message(
                                text="You upgrade your armour."
                            ))

                    break
                else:
                    self.world.remove_component(entity, Coincident)
                    self.world.remove_component(entity, Position)
                    self.world.remove_component(entity, LastKnownPosition)

                    self.world.add_component(entity, Inventory())

                    self.world.create_entity(Message(
                        text=f"You pick up the {item.name}."
                    ))
