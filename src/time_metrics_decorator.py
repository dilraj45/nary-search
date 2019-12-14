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
                    print("publishing")
                    TimeMetricsDecorator._publisher.publish(metric_identifier, args, (time2 - time1) * 1000.0)

                print('{:s} function took {:.3f} ms'.format(func.__name__, (time2 - time1) * 1000.0))
                return ret
            return decorated_function
        return wrap

    @staticmethod
    def register_publisher(metric_publisher):
        TimeMetricsDecorator._publisher = metric_publisher
