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
        return f"Point is at {self.position}"


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
        num_distance: int = len(D)

        def backtrack(
            index: int, current_a: tuple[int, ...], remaining_length: int
        ):
            if index > num_distance - 1:
                if remaining_length == 0:
                    yield current_a
                return

            distance = D[index]

            min_possible = (num_distance - index) * distance

            if remaining_length < min_possible:
                return

            max_ai = remaining_length // distance

            for ai in range(1, max_ai + 1):
                new_remaining_length = remaining_length - (distance * ai)
                if new_remaining_length < 0:
                    break
                yield from backtrack(
                    index + 1, current_a + (ai,), new_remaining_length
                )

        results = backtrack(0, tuple(), self.n - 1)

        for result in results:
            self.configurations.append([Point(x) for x in result])

        return len(self.configurations) > 0

    def __repr__(self):
        return f"PointConfiguration({self.configurations})"


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
