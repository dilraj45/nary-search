from visualization import Visualization
from time_metrics_decorator import TimeMetricsDecorator
from nary_search import NarySearch
import random
import threading


class NarySearchMetricPublisher:

    def __init__(self, visualize):
        self.visualize = visualize

    def publish(self, metric_identifier, func_args, computation_time):
        x_value = len(func_args[2])
        dimension_handle = self.metric_handle_generator(metric_identifier, getattr(func_args[0], metric_identifier))

        self.visualize.publish_datapoint(dimension_handle, x_value, computation_time)

    def metric_handle_generator(self, dimension_handle, dimension_value):
        return "{}={}".format(dimension_handle, dimension_value)


def execute_analysis_suite(visualize):
    # Pre-loading NarySearch objects
    nary_search_instances = [NarySearch(factor) for factor in range(0, 10)]

    # Initiating visualizations
    publisher = NarySearchMetricPublisher(visualize)
    TimeMetricsDecorator.register_publisher(publisher)
    for value in range(1, 6):
        graph_handle = publisher.metric_handle_generator('factor', value)
        visualize.register_graph(graph_handle, "Sample set size", "Time (sec)")
        visualize.activate_graph(graph_handle, 5, 1, value)
    complete_set = range(-1000000, 1000001)

    for sample_len in range(1, 10000):
        sample_set = sorted(random.sample(complete_set, sample_len))
        # for exp in range(0, 10):
        target = sample_set[random.randrange(0, sample_len)]
        for factor in range(1, 6):
            nary_search_instances[factor].search(target, sample_set)


visualize = Visualization()
threading.Thread(target=execute_analysis_suite, args=[visualize]).start()
visualize.show()
