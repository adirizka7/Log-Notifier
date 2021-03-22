from datetime import datetime

class Log:
    def __init__(self, log_message):
        self._time = self._get_time_from_log(log_message)
        self._type = log_message.split(' ')[2].lower()


    def _get_time_from_log(self, log_message):
        timestr = ' '.join(log_message.split(' ')[:2])
        return datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S').timestamp()

    def get_time(self):
        return self._time

    def get_type(self):
        return self._type
