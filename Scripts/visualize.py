import itertools
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations


'''
NOTE: The generating procedural problem can be summarized as follows:
Let D = {d_1, d_2, ..., d_n}
Let n be a natural number.

The procedular test case generating algorithm finds all solutions to the
following linear equation:

a_1d_1 + a_2d_2 + ... + a_nd_n = n - 1

The n - 1 is due to the discrepancy in distance vs points.

For some positive numberes a_1, a_2, ..., a_n.

Let z = n / min(D)

Note that a_1 lies between the range of 1 to z.

For implementation, you will have to check if the resulting equation is still
equal to n or not.
'''


class Point:
    def __init__(self, position: int):
        if position < 0:
            raise ValueError("Position must be a non-negative integer.")
        self.position = position

    def __repr__(self):
        return f"{self.position}"


class PointConfiguration:
    def __init__(self, n: int, distances: set):
        self.n = n
        self.distances = distances
        self.configurations = []

    def is_valid(self):
        used_distances = set()
        for config in self.configurations:
            for i in range(len(config) - 1):
                dist = config[i + 1].position - config[i].position
                if dist in self.distances:
                    used_distances.add(dist)

        return len(used_distances) == len(self.distances)

    def generate_config(self) -> bool:
        D = list(self.distances)

        def backtrack(current_path: list[int], remaining_length: int):
            if remaining_length <= 0:
                if self._uses_all_distances(current_path):
                    yield current_path
                return
            for distance in D:
                if remaining_length >= distance:
                    yield from backtrack(
                        current_path + [distance],
                        remaining_length - distance,
                    )

        results = backtrack([], self.n)

        for result in results:
            points = []
            pos = 0
            for dist in result:
                pos += dist
                points.append(Point(pos))
            self.configurations.append(points)

        return len(self.configurations) > 0

    def _uses_all_distances(self, path: list[int]) -> bool:
        used_distances = set(path)
        return self.distances.issubset(used_distances)

    def __repr__(self):
        return f"PointConfiguration({self.configurations})"


class CommunicationGraph:
    def __init__(self, points, distance_set):
        self.points = points
        self.n = len(points)
        self.D = distance_set
        self.graphs = []
        self.interference_records = []
        self.edges = self.generate_edges()

    def generate_edges(self):
        valid_edges = []

        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                valid_edges.append(
                    (self.points[i].position, self.points[j].position))

        return valid_edges

    def generate_all_graphs(self):
        point_positions = [p.position for p in self.points]
        all_edges = [(i, j) for i, j in itertools.combinations(point_positions, 2)
                     if abs(i - j) in self.D]

        for subset in itertools.chain.from_iterable(itertools.combinations(all_edges, r) for r in range(len(all_edges) + 1)):
            G = nx.Graph()
            G.add_nodes_from(point_positions)
            G.add_edges_from(subset)
            interference = self.calculate_interference(G)
            self.graphs.append((G, interference))
            self.interference_records.append(interference)

    def generate_all_connected_graphs(self):
        # r = n - 1 (A tree) to n choose 2 (A complete graph) - By default,
        # we have n choose 2 edges by construction
        for r in range(self.n - 1, len(self.edges) + 1):
            for edge_set in combinations(self.edges, r):
                G = nx.Graph()
                for v in self.points:
                    G.add_node(v.position)
                G.add_edges_from(edge_set)

                if nx.is_connected(G):
                    interference = self.calculate_interference(G)
                    self.graphs.append((G, interference))
                    self.interference_records.append(interference)

    def calculate_interference(self, G):
        interference = {p.position: 0 for p in self.points}
        for u, v in G.edges():
            radius = abs(u - v)
            for p in self.points:
                if u - radius <= p.position <= u + radius or v - radius <= p.position <= v + radius:
                    interference[p.position] += 1
        return interference

    def max_interference_summary(self):
        return [max(interf.values()) for _, interf in self.graphs]

    def get_best_graph(self):
        min_max = float('inf')
        best_graph = None
        best_interf = None
        for G, interf in self.graphs:
            curr_max = max(interf.values())
            if curr_max < min_max:
                min_max = curr_max
                best_graph = G
                best_interf = interf
        return best_graph, best_interf

    def plot_graph(self, G):
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue',
                node_size=500, font_size=10)
        plt.show()

    def plot_all_graphs(self):
        for G, interf in self.graphs:
            self.plot_graph(G)
            print(f"Interference: {interf}")

    def plot_linear_graph(self, G):
        pos = {node: (node, 0) for node in G.nodes()}
        nx.draw(G, pos, with_labels=True, node_color='lightblue',
                node_size=500, font_size=10)
        plt.show()
