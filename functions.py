import matplotlib
matplotlib.use('Agg')
import re
import matplotlib.pyplot as plt
import numpy as np


def dataset(filename):
    f = open("./dataset/" + filename, "r")
    content = f.read()
    optimal_value = re.search("Optimal value: (\d+)", content, re.MULTILINE)
    if optimal_value is not None:
        optimal_value = optimal_value.group(1)
    else:
        optimal_value = re.search("Best value: (\d+)", content, re.MULTILINE)
        if optimal_value is not None:
            optimal_value = optimal_value.group(1)
    capacity = re.search("^CAPACITY : (\d+)$", content, re.MULTILINE).group(1)
    graph = re.findall(r"^(\d+) (\d+) (\d+)$", content, re.MULTILINE)
    demand = re.findall(r"^(\d+) (\d+)$", content, re.MULTILINE)
    graph = {int(a): (int(b), int(c)) for a, b, c in graph}
    demand = {int(a): int(b) for a, b in demand}
    capacity = int(capacity)
    optimal = int(optimal_value)
    return capacity, graph, demand, optimal


def show_routes(dataset_filename, routes, image_name):
    vehicle_capacity, graph, delivery_demand, optimal = dataset(dataset_filename)
    # deport location
    deport_x, deport_y = graph.get(1)
    for i in range(0, len(routes)):

        points = {
            "x": [],
            "y": []
        }

        # start point
        points["x"].append(deport_x)
        points["y"].append(deport_y)

        for j in range(0, len(routes[i]) - 1):
            path_from = routes[i][j]
            path_to = routes[i][j + 1]

            x1, y1 = graph[path_from]
            x2, y2 = graph[path_to]
            # print( x1, x2, y1, y2 )

            points["x"].append(x1)
            points["y"].append(y1)
            points["x"].append(x2)
            points["y"].append(y2)

        # end point
        points["x"].append(deport_x)
        points["y"].append(deport_y)

        plt.plot(points["x"], points["y"], marker='o', linestyle="--")

    plt.plot(deport_x, deport_y, marker='x')
    plt.title('Paths')
    #plt.show()
    image = 'static/img/'+image_name +'.png'
    plt.savefig(image)
    plt.close()
    return image_name +'.png'


def plot_paths(graph, best_sol):
    print("best solution:", str(int(best_sol[1])), str(best_sol), " num trucks:", len(best_sol[0]))

    # deport location
    deport_x, deport_y = graph.get(1)

    for i in range(0, len(best_sol[0])):

        points = {
            "x": [],
            "y": []
        }

        # start point
        points["x"].append(deport_x)
        points["y"].append(deport_y)

        for j in range(0, len(best_sol[0][i]) - 1):
            path_from = best_sol[0][i][j]
            path_to = best_sol[0][i][j + 1]

            x1, y1 = graph[path_from]
            x2, y2 = graph[path_to]
            # print( x1, x2, y1, y2 )

            points["x"].append(x1)
            points["y"].append(y1)
            points["x"].append(x2)
            points["y"].append(y2)

        # end point
        points["x"].append(deport_x)
        points["y"].append(deport_y)

        plt.plot(points["x"], points["y"], marker='o', linestyle="--")

    plt.plot(deport_x, deport_y, marker='x')
    plt.title('Paths')
    plt.show()


def get_euclidean_distance(x1, x2, y1, y2):
    """
    Euclidean distance calculate
    """
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


