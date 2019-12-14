import random

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
from collections import namedtuple
from typing import List


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Graph:
    handle: str
    x_label: str
    y_label: str
    x_datapoints: List[int]
    y_datapoints: List[int]


# todo dilraj: Rename this class
class Visualization:

    ActiveGraphSubPlotMappings = namedtuple('GraphFigureMapping', ['graph_handle', 'sub_plot', 'color'])
    active_graphs = []
    graphs = {}
    figure = plt.figure()

    def publish_datapoint(self, graph_handle, x_value, y_value):
        graph = self.graphs[graph_handle]
        graph.x_datapoints.append(x_value)
        graph.y_datapoints.append(y_value)

    def refresh_graph(self, i):
        for graph_figure_mappings in self.active_graphs:
            print("refreshing for" + graph_figure_mappings.graph_handle)
            graph = self.graphs[graph_figure_mappings.graph_handle]

            print(graph.x_datapoints)
            graph_figure_mappings.sub_plot.clear()
            graph_figure_mappings.sub_plot.plot(graph.x_datapoints, graph.y_datapoints,
                                                color=graph_figure_mappings.color)

    def register_graph(self, graph_handle, x_label, y_label):
        graph = Graph(handle=graph_handle, x_label=x_label, y_label=y_label, x_datapoints=[], y_datapoints=[])
        self.graphs[graph_handle] = graph

    def activate_graph(self, graph_handle, row, col, index):
        color = 'red'
        s_plot = self.figure.add_subplot(row, col, index)
        self.active_graphs.append(self.ActiveGraphSubPlotMappings(graph_handle, s_plot, color))

    def show(self):
        sample = animation.FuncAnimation(self.figure, self.refresh_graph, interval=1000)
        plt.show()

    def random_color_generator(self):
        colors_in_use = [x.color for x in self.active_graphs]
        rgb = (int(random.random() * 256), int(random.random() * 256), int(random.random() * 256))
        while rgb in colors_in_use:
            rgb = (int(random.random() * 256), int(random.random() * 256), int(random.random() * 256))
        return rgb
