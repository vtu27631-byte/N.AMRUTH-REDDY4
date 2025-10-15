import numpy as np

# Given distance matrix
d = np.array([
    [0, 10, 12, 11, 14],
    [10, 0, 13, 15, 8],
    [12, 13, 0, 9, 14],
    [11, 15, 9, 0, 16],
    [14, 8, 14, 16, 0]
])

iteration = 100
n_ants = 5
n_citys = 5

# Initialization
m = n_ants
n = n_citys
e = 0.5  # evaporation rate
alpha = 1  # visibility factor
beta = 2   # pheromone factor

# Calculating visibility (1/distance)
visibility = 1 / d
visibility[visibility == np.inf] = 0

# Initial pheromone on paths
pheromone = 0.1 * np.ones((n, n))  # pheromone matrix should be n x n, not m x n

# Initialize route matrix (n_ants x n_citys+1)
route = np.ones((m, n + 1))

for ite in range(iteration):
    route[:, 0] = 1  # start at city 1

    for i in range(m):  # for each ant
        temp_visibility = np.array(visibility)  # copy of visibility
        for j in range(n - 1):  # traverse n-1 cities
            combine_feature = np.zeros(n)
            cum_prob = np.zeros(n)
            cur_loc = int(route[i, j] - 1)
            temp_visibility[:, cur_loc] = 0  # current city visibility = 0

            p_feature = np.power(pheromone[cur_loc, :], beta)
            v_feature = np.power(temp_visibility[cur_loc, :], alpha)
            combine_feature = p_feature * v_feature

            total = np.sum(combine_feature)
            if total == 0:
                probs = np.zeros(n)
            else:
                probs = combine_feature / total

            cum_prob = np.cumsum(probs)
            r = np.random.random_sample()
            city = np.nonzero(cum_prob > r)[0][0] + 1
            route[i, j + 1] = city

        # Add the last unvisited city
        left = list(set(range(1, n + 1)) - set(route[i, :-2]))[0]
        route[i, -2] = left

    route_opt = np.array(route)
    dist_cost = np.zeros((m, 1))

    # Calculate distance of each ant's tour
    for i in range(m):
        s = 0
        for j in range(n - 1):
            s += d[int(route_opt[i, j]) - 1, int(route_opt[i, j + 1]) - 1]
        dist_cost[i] = s

    # Find best route of this iteration
    dist_min_loc = np.argmin(dist_cost)
    dist_min_cost = dist_cost[dist_min_loc]
    best_route = route[dist_min_loc, :]

    # Evaporation
    pheromone = (1 - e) * pheromone

    # Update pheromone
    for i in range(m):
        for j in range(n - 1):
            dt = 1 / dist_cost[i]
            from_city = int(route_opt[i, j]) - 1
            to_city = int(route_opt[i, j + 1]) - 1
            pheromone[from_city, to_city] += dt
            pheromone[to_city, from_city] += dt  # optional for symmetric TSP

# Output results
print('Route of all ants at the end:')
print(route_opt)
print()
print('Best path:', best_route)
print('Cost of the best path:', int(dist_min_cost[0]) + d[int(best_route[-2]) - 1, 0])
