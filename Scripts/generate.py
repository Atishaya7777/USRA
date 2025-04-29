from visualize import Point, PointConfiguration, CommunicationGraph
import networkx as nx


def generate_graphs():
    D = {1, 2, 4}
    n = 10
    pc = PointConfiguration(n, D)
    pc.generate_config()

    test_config = pc.configurations[0]
    cg = CommunicationGraph(test_config, D)
    print(f"POINTS\n {cg.points}")
    print(cg.edges)
    cg.generate_all_connected_graphs()
    print(f"GRAPHS\n {cg.graphs}")
    best_graph, best_interf = cg.get_best_graph()
    cg.plot_linear_graph(best_graph)
    # cg.plot_all_graphs()

    return cg.max_interference_summary(), best_interf, best_graph


def test_connected():
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 6, 10])
    G.add_edges_from(
        [(1, 2), (1, 3), (1, 4), (1, 6), (1, 10), (2, 3), (2, 4), (2, 6),
         (2, 10), (3, 4), (3, 6), (3, 10), (4, 6), (4, 10), (6, 10)]
    )

    print(nx.is_connected(G))


if __name__ == "__main__":
    interference_summary, best_interference, best_graph = generate_graphs()
    print("Interference Summary:", interference_summary)
    print("Best Interference:", best_interference)
