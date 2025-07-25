import time

class MetricsCollector:
    def __init__(self):
        self.metrics = []

    def collect(self, data: dict):
        data['timestamp'] = time.time()
        self.metrics.append(data)

    def get_metrics(self):
        return self.metrics