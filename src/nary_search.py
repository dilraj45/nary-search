from time_metrics_decorator import TimeMetricsDecorator


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
