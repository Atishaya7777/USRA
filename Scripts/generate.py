from visualize import Point, PointConfiguration, CommunicationGraph


def generate_graphs():
    D = {1, 2, 4}
    n = 10
    pc = PointConfiguration(n, D)
    pc.generate_config()

    test_config = pc.configurations[0]
    cg = CommunicationGraph(test_config, D)
    cg.generate_all_connected_graphs()
    best_graph, best_interf = cg.get_best_graph()

    return cg.max_interference_summary(), best_interf, best_graph


if __name__ == "__main__":
    interference_summary, best_interference, best_graph = generate_graphs()
    print("Interference Summary:", interference_summary)
    print("Best Interference:", best_interference)
