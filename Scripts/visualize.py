import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations


class Point:
    def __init__(self, position: int):
        self.position = position

    def __repr__(self):
        return f"Point is at {self.position}"


class PointConfiguration:
    def __init__(self, points: list[Point], distances: set):
        self.points = sorted(points, key=lambda p: p.position)
        self.distances = distances

    def is_valid(self):
        used_distances = set()
        for i in range(len(self.points) - 1):
            dist = self.points[i + 1].position - self.points[i].position
            if dist in self.distances:
                used_distances.add(dist)
        return used_distances == self.distances

    def __repr__(self):
        return f"PointConfiguration({self.points})"


class CommunicationGraph:
    def __init__(self, configuration):
        self.configuration = configuration
        self.graph = nx.Graph()

    def build_graph(self):
        for point in self.configuration.points:
            self.graph.add_node(point.position)
        for p1, p2 in combinations(self.configuration.points, 2):
            dist = abs(p2.position - p1.position)
            if dist in self.configuration.distances:
                self.graph.add_edge(p1.position, p2.position, weight=dist)

    def visualize(self):
        self.build_graph()
        pos = {point.position: (point.position, 0)
               for point in self.configuration.points}
        labels = {point.position: str(point.position)
                  for point in self.configuration.points}
        edge_labels = {
            (p1, p2): f"{data['weight']}" for p1, p2, data in self.graph.edges(data=True)
        }

        plt.figure(figsize=(10, 2))
        nx.draw(self.graph, pos, with_labels=True, labels=labels,
                node_color='skyblue', node_size=500, font_size=10)
        nx.draw_networkx_edge_labels(
            self.graph, pos, edge_labels=edge_labels, font_size=8)
        plt.title("Communication Graph")
        plt.xlabel("Position on Line Segment")
        plt.yticks([])
        plt.show()


n = 10
D = {1, 2, 4}


def generate_all_configurations(n, distances):
    def backtrack(current_positions, remaining_length):
        if remaining_length == 0:
            config = PointConfiguration(
                [Point(pos) for pos in current_positions], distances)
            if config.is_valid():
                configurations.append(config)
            return
        for d in distances:
            if remaining_length - d >= 0:
                backtrack(current_positions +
                          [current_positions[-1] + d], remaining_length - d)

    configurations = []
    backtrack([0], n)
    return configurations


configurations = generate_all_configurations(n, D)
print(f"Total valid configurations found: {len(configurations)}")
for config in configurations:
    print(config)
    graph = CommunicationGraph(config)
    # graph.visualize()
