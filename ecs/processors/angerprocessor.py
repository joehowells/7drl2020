from esper import Processor

from constants import MAX_ANGER, ANGER_TIER_1, ANGER_TIER_2, ANGER_TIER_3, ANGER_TIER_4, ANGER_TIER_5
from ecs.components.message import Message
from ecs.components.player import Player
from script import ANGER_TIER_INCREASED, ANGER_TIER_DECREASED, GAIN_EXTRA_ATTACK, LOSE_EXTRA_ATTACK


class AngerProcessor(Processor):
    """Handles player anger and associated combat bonuses."""

    def __init__(self):
        self.old_tier = 0

    def process(self):
        for _, player in self.world.get_component(Player):
            player.attack_bonus = 0
            player.defend_bonus = 0
            new_tier = 0

            player.anger = min(max(player.anger + player.action.anger, 0), MAX_ANGER)
            player.number_of_attacks = 1

            if player.anger >= ANGER_TIER_1:
                new_tier = 1
                player.attack_bonus += 1

            if player.anger >= ANGER_TIER_2:
                new_tier = 2
                player.defend_bonus += 1

            if player.anger >= ANGER_TIER_3:
                new_tier = 3
                player.attack_bonus += 1

            if player.anger >= ANGER_TIER_4:
                new_tier = 4
                player.defend_bonus += 1

            if player.anger >= ANGER_TIER_5:
                new_tier = 5
                player.number_of_attacks += 1
                player.attack_bonus += 1
                player.defend_bonus += 1

            player.attack = player.base_attack + player.attack_equip + player.attack_bonus
            player.defend = player.base_defend + player.defend_equip + player.defend_bonus

            if new_tier > self.old_tier:
                self.world.create_entity(Message(text=ANGER_TIER_INCREASED, priority=20))

                if new_tier == 5:
                    self.world.create_entity(Message(text=GAIN_EXTRA_ATTACK, priority=20))

            if new_tier < self.old_tier:
                self.world.create_entity(Message(text=ANGER_TIER_DECREASED, priority=20))

                if new_tier == 4:
                    self.world.create_entity(Message(text=LOSE_EXTRA_ATTACK, priority=20))

            self.old_tier = new_tier
