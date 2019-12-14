import random
import matplotlib.pyplot as plt
import time


class TimeMetricsDecorator:

    _publisher = None

    @staticmethod
    def timed(metric_identifier):
        def wrap(func):
            def decorated_function(*args):
                time1 = time.time()
                ret = func(*args)
                time2 = time.time()
                if TimeMetricsDecorator._publisher is not None:
                    TimeMetricsDecorator._publisher.publish(metric_identifier, args, (time2 - time1) * 1000.0)
                return ret
            return decorated_function
        return wrap

    @staticmethod
    def register_publisher(metric_publisher):
        TimeMetricsDecorator._publisher = metric_publisher


class NarySearch:

    def __init__(self, factor):
        self.factor = factor

    @TimeMetricsDecorator.timed('factor')
    def search(self, target, sorted_input):

        if len(sorted_input) < 1:
            return -1

        lower_bound = 0
        upper_bound = len(sorted_input) - 1
        while lower_bound < upper_bound:
            candidate_index = lower_bound + int((upper_bound - lower_bound)/self.factor)
            if sorted_input[candidate_index] == target:
                return candidate_index
            if target < sorted_input[candidate_index]:
                upper_bound = candidate_index - 1 if candidate_index > 0 else candidate_index
            if target > sorted_input[candidate_index]:
                lower_bound = candidate_index + 1 if candidate_index < len(sorted_input) else candidate_index
        if lower_bound == upper_bound and target == sorted_input[lower_bound]:
            return lower_bound
        return -1


class NarySearchListPublisher:

    def __init__(self):
        self.datapoint_holders = {}

    def publish(self, metric_identifier, func_args, computation_time):
        x_value = len(func_args[2])
        dimension_handle = self.metric_handle_generator(metric_identifier, getattr(func_args[0], metric_identifier))
        if dimension_handle not in self.datapoint_holders:
            self.datapoint_holders[dimension_handle] = {}
        factor_datapoints = self.datapoint_holders[dimension_handle]
        if x_value in factor_datapoints:
            factor_datapoints[x_value].append(computation_time)
        else:
            factor_datapoints[x_value] = [computation_time]

    def metric_handle_generator(self, dimension_handle, dimension_value):
        return "{}={}".format(dimension_handle, dimension_value)


def execute_anaylsis_suite():
    # Pre-loading NarySearch objects
    nary_search_instances = [NarySearch(factor) for factor in range(0, 10)]

    # Initiating visualizations
    publisher = NarySearchListPublisher()
    TimeMetricsDecorator.register_publisher(publisher)

    complete_set = range(-1000000, 1000001)
    for sample_len in range(1, 1001):
        sample_set = sorted(random.sample(complete_set, sample_len))
        for exp in range(0, 100):
            target = sample_set[random.randrange(0, sample_len)]
            for factor in range(2, 6):
                nary_search_instances[factor].search(target, sample_set)

    return publisher.datapoint_holders


for factor, datapoints in execute_anaylsis_suite().items():
    x_datapoints = []
    y_datapoints = []
    for key, value in datapoints.items():
        aggregated_value = 0
        for v in value:
            aggregated_value += v
        aggregated_value = aggregated_value/len(value)
        x_datapoints.append(key)
        y_datapoints.append(aggregated_value)
    plt.plot(x_datapoints, y_datapoints, label=factor)

plt.xlabel("Sample set length")
plt.ylabel("Computation time")
plt.title("Nary search analysis")
plt.legend()
plt.show()

