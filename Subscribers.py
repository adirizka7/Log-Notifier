class Subscribers:
    def __init__(self):
        self._subscriber = {}

    def add_subscriber(self, person, log_types):
        for log_type in log_types:
            if log_type not in self._subscriber:
                self._subscriber[log_type] = []

            self._subscriber[log_type].append(person)

    def get_subscribers_of_log_type(self, log_type):
        return self._subscriber[log_type]
