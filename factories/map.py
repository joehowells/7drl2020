from collections import deque
from dataclasses import dataclass
from itertools import product, combinations
from random import shuffle, randint, random, choice
from typing import List, Tuple, Set, Dict

from constants import ROOM_SIZE, GRAPH_MIN_DEPTH, GRAPH_MAX_DEPTH

Node = Tuple[int, int]
Link = Tuple[Node, Node]


@dataclass()
class Room:
    x1: int
    x2: int
    y1: int
    y2: int

    @property
    def w(self):
        return self.x2 - self.x1

    @property
    def h(self):
        return self.y2 - self.y1

    @property
    def cells(self):
        return [(x, y) for x in range(self.x1, self.x2) for y in range(self.y1, self.y2)]


def make_graph() -> Tuple[Set[Node], Set[Link]]:
    nodes = set()
    links = set()
    stack = deque([((0, 0), 0)])

    while stack:
        v, depth = stack.popleft()

        if depth > randint(GRAPH_MIN_DEPTH, GRAPH_MAX_DEPTH):
            continue

        m, n = v
        neighbors = [
            (m - 1, n),
            (m + 1, n),
            (m, n - 1),
            (m, n + 1),
        ]
        neighbors = [neighbor for neighbor in neighbors if neighbor not in nodes]

        if not neighbors:
            continue

        shuffle(neighbors)

        for w in neighbors:
            nodes.add(w)
            stack.append((w, depth + 1))

            if w < v:
                links.add((w, v))
            else:
                links.add((v, w))

            if depth > randint(GRAPH_MIN_DEPTH, GRAPH_MAX_DEPTH):
                break

    return nodes, links


def apply_offset(nodes: Set[Node], links: Set[Link]) -> Tuple[Set[Node], Set[Link]]:
    m_min = min(m for m, _ in nodes)
    n_min = min(n for _, n in nodes)

    nodes = {
        (m - m_min, n - n_min)
        for m, n in nodes
    }

    links = {
        ((mv - m_min, nv - n_min), (mw - m_min, nw - n_min))
        for (mv, nv), (mw, nw) in links
    }

    return nodes, links


def add_more_links(nodes: Set[Node], links: Set[Link], probability: float = 0.2) -> None:
    for w, v in combinations(sorted(nodes), 2):
        if w > v:
            w, v = v, w

        adjacent_h = w[1] == v[1] and abs(w[0] - v[0]) == 1
        adjacent_v = w[0] == v[0] and abs(w[1] - v[1]) == 1

        if (adjacent_h or adjacent_v) and (w, v) not in links and random() < probability:
            links.add((w, v))


def node_box(node: Node) -> Room:
    m, n = node

    return Room(
        ROOM_SIZE * m + 1,
        ROOM_SIZE * m + ROOM_SIZE,
        ROOM_SIZE * n + 1,
        ROOM_SIZE * n + ROOM_SIZE,
    )


def link_box(link: Link) -> Room:
    u, w = link
    mu, nu = u
    mw, nw = w

    return Room(
        ROOM_SIZE * mu + 1,
        ROOM_SIZE * mw + ROOM_SIZE,
        ROOM_SIZE * nu + 1,
        ROOM_SIZE * nw + ROOM_SIZE,
    )


def make_map() -> Tuple[(List[List[bool]]), List[Room], Dict[Tuple[int, int], int]]:
    nodes, links = make_graph()
    nodes, links = apply_offset(nodes, links)
    add_more_links(nodes, links)

    nodes = {node: node_box(node) for node in nodes}
    links = {link: link_box(link) for link in links}

    h_links = {link: box for link, box in links.items() if box.w > box.h}
    v_links = {link: box for link, box in links.items() if box.w < box.h}

    for link in h_links.values():
        link.y1 = randint(link.y1 + 1, link.y2 - 3)
        link.y2 = link.y1 + 2

    for link in v_links.values():
        link.x1 = randint(link.x1 + 1, link.x2 - 3)
        link.x2 = link.x1 + 2

    for node, box in nodes.items():
        m, n = node
        x1_base = ROOM_SIZE * m + 1
        x2_base = ROOM_SIZE * m + ROOM_SIZE
        y1_base = ROOM_SIZE * n + 1
        y2_base = ROOM_SIZE * n + ROOM_SIZE

        h_neighbors = [r for key, r in h_links.items() if node in key]
        v_neighbors = [r for key, r in v_links.items() if node in key]

        x1 = min((r.x1 for r in v_neighbors), default=x1_base + 3)
        x2 = max((r.x2 for r in v_neighbors), default=x1_base + 5)
        y1 = min((r.y1 for r in h_neighbors), default=y1_base + 3)
        y2 = max((r.y2 for r in h_neighbors), default=y1_base + 5)

        box.x1 = x1
        box.x2 = x2
        box.y1 = y1
        box.y2 = y2

        dead_end = len(h_neighbors) + len(v_neighbors) == 1

        if dead_end or random() < 0.5:
            box.x1 = randint(x1_base, x1 - 1)
            box.x2 = randint(x2 + 1, x2_base)
            box.y1 = randint(y1_base, y1 - 1)
            box.y2 = randint(y2 + 1, y2_base)

    for (m, n), link in h_links.items():
        link.x1 = min(nodes[m].x2, nodes[n].x2)
        link.x2 = max(nodes[m].x1, nodes[n].x1)

    for (m, n), link in v_links.items():
        link.y1 = min(nodes[m].y2, nodes[n].y2)
        link.y2 = max(nodes[m].y1, nodes[n].y1)

    w = max(box.x2 for box in nodes.values()) + 1
    h = max(box.y2 for box in nodes.values()) + 1

    walkable = [[False for _ in range(w)] for _ in range(h)]
    glyphs = {}

    for room in nodes.values():
        for x, y in product(range(room.x1, room.x2), range(room.y1, room.y2)):
            walkable[y][x] = True

        # Decorations
        if room.w >= 7 and room.h >= 7 and random() < 0.2:
            for x, y in product(range(room.x1 + 2, room.x2 - 2), range(room.y1 + 2, room.y2 - 2)):
                walkable[y][x] = False
        elif room.w >= 5 and room.h >= 5 and random() < 0.5:
            if not room.w % 2 and not room.h % 2:
                for x, y in product(range(room.x1 + 1, room.x2 - 1), range(room.y1 + 1, room.y2 - 1)):
                    glyphs[(x, y)] = 0x002B
            else:
                if room.w % 2:
                    for x in range(room.x1 + 1, room.x2 - 1, 2):
                        walkable[room.y1 + 1][x] = False
                        walkable[room.y2 - 2][x] = False
                        glyphs[(x, room.y1+1)] = 0x0030
                        glyphs[(x, room.y2-2)] = 0x0030

                if room.h % 2:
                    for y in range(room.y1 + 1, room.y2 - 1, 2):
                        walkable[y][room.x1 + 1] = False
                        walkable[y][room.x2 - 2] = False
                        glyphs[(room.x1+1, y)] = 0x0030
                        glyphs[(room.x2-2, y)] = 0x0030

    for room in h_links.values():
        for x, y in product(range(room.x1, room.x2), range(room.y1, room.y2)):
            walkable[y][x] = True

    for room in v_links.values():
        for x, y in product(range(room.x1, room.x2), range(room.y1, room.y2)):
            walkable[y][x] = True

    for x, y in product(range(w), range(h)):
        if walkable[y][x] and (x, y) not in glyphs:
            glyphs[(x, y)] = choice([0x0027, 0x002C, 0x002E, 0x0060])

    return walkable, list(nodes.values()), glyphs
