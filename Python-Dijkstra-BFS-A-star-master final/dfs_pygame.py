import pygame as pg
from random import random
from collections import deque

def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2

def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

cols, rows = 15, 10
TILE = 60

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()

# grid creation with random obstacles
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]
# dict of adjacency lists for graph representation
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# DFS settings
start = (0, 0)
stack = [start]
visited = {start: None}
cur_node = start

while True:
    sc.fill(pg.Color('black'))

    # Draw obstacles and visited nodes
    [[pg.draw.rect(sc, pg.Color('brown'), get_rect(x, y), border_radius= 0)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    [pg.draw.rect(sc, pg.Color('lightgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkgray'), get_rect(x, y)) for x, y in stack]
    # DFS logic
    if stack:
        cur_node = stack.pop()
        next_nodes = graph.get(cur_node, [])
        for next_node in next_nodes:
            if next_node not in visited:
                stack.append(next_node)
                visited[next_node] = cur_node

    # Draw the path
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 5)
        path_segment = visited[path_segment]
    pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(*start), border_radius=TILE // 5)
    pg.draw.rect(sc, pg.Color('red'), get_rect(*path_head), border_radius=TILE // 5)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    pg.display.flip()
    clock.tick(7)
