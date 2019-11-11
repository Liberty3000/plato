import numpy as np

def manhattan_distance(beg, end):
    return abs(beg[0] - end[0]) + abs(beg[1] + end[1])

def absolute_distance(beg, end):
    return np.sqrt((beg[0] - end[0])**2 + (beg[1]-end[1])**2)

def fixed_cost(cost):
    def func(a, b):
        return cost
    return func

def grid_neighbors(height, width):
    def func(coord):
        neighbor_list = [(coord[0], coord[1] + 1),
                         (coord[0], coord[1] - 1),
                         (coord[0] + 1, coord[1]),
                         (coord[0] - 1, coord[1]),
                         (coord[0] - 1, coord[1]-1),
                         (coord[0] + 1, coord[1]+1)]

        return [c for c in neighbor_list
                if c != coord
                and c[0] >= 0 and c[0] < width
                and c[1] >= 0 and c[1] < height]

    return func

def pathfinder(neighbors=grid_neighbors(100,100),
               distance=absolute_distance,
               cost=fixed_cost(1)):

    def reconstruct_path(came_from, current_node):
        if current_node in came_from:
            p = reconstruct_path(came_from, came_from[current_node])
            p.append(current_node)
            return p
        else:
            return [current_node]

    def func(beg, end, max_cost=None):
        open_set, closed_set = set([beg]),set()
        came_from = {}

        g_score = {beg: 0}
        f_score = {beg: cost(beg, end)}

        while len(open_set) != 0:
            current = min(open_set, key=lambda c:f_score[c])

            if max_cost != None and g_score[current] > max_cost: break

            if current == end: return g_score[current], reconstruct_path(came_from, end)

            open_set.discard(current)
            closed_set.add(current)
            for neighbor in neighbors(current):
                tentative_score = g_score[current] + cost(current, neighbor)

                if neighbor in closed_set and (neighbor in g_score and tentative_score >= g_score[neighbor]):
                    continue

                if neighbor not in open_set or (neighbor in g_score and tentative_score < g_score[neighbor]):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_score
                    f_score[neighbor] = tentative_score + distance(neighbor, end)
                    if neighbor not in open_set: open_set.add(neighbor)
        return None, []
    return func

def calculate_cost(src, dst, terrain):
    return np.random.randint(1,100)

def clip_route(route, bounds):
    for waypoint,(x,y) in enumerate(route):
        x = np.clip(x, 0, bounds[0]-1)
        y = np.clip(y, 0, bounds[1]-1)
        route[waypoint] = (x,y)
    return route
