from sys import maxsize
from itertools import permutations

V = 4

def travellingSalesmanProblem(graph, s):
    vertex = []  # List of vertices except the starting point
    for i in range(V):
        if i != s:
            vertex.append(i)

    min_path = maxsize  # Initialize minimum path weight
    next_permutation = permutations(vertex)  # Generate all permutations of vertices

    for i in next_permutation:
        current_pathweight = 0
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]  # Return to starting point

        min_path = min(min_path, current_pathweight)

    return min_path

# Driver code
if __name__ == "__main__":
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    s = 0
    print("Minimum cost of the tour:", travellingSalesmanProblem(graph, s))
