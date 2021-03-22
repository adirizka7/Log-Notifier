from Log import Log
from Subscribers import Subscribers
from Person import Person
from datetime import datetime

import json

LOG_TYPE_CRITICAL = 'critical'
LOG_TYPE_WARNING = 'warning'
LOG_TYPE_INFO = 'info'

class Driver:
    def __init__(self, file, subscribers):
        self._file = open(file, 'r').read()
        self._logs = [
            Log(log.strip()) for log in self._file.split('\n\n')
        ]
        self._config = json.loads(open('config.json', 'r').read())
        self._log_count = {
            log_type: {
                'count': 0,
                'first_occurence': None,
                'wait_until': 0
            }
            for log_type in self._config
        }
        self._subscribers = subscribers
        
    def get_log(self):
        return self._logs

    def run_through_log(self):
        for log in self._logs:
            self._count_log(log)

        self.execute_leftover()

    def _count_log(self, log):

        first_occurence = self._log_count[log.get_type()]['first_occurence']
        wait_until = self._log_count[log.get_type()]['wait_until']
        duration = self._config[log.get_type()]['duration']
        frequency = self._config[log.get_type()]['frequency']

        if first_occurence == None:
            self._log_count[log.get_type()]['first_occurence'] = log.get_time()
            first_occurence = log.get_time()

        if log.get_time() - first_occurence <= duration and log.get_time() >= wait_until:
            self._log_count[log.get_type()]['count'] += 1

            count = self._log_count[log.get_type()]['count']

        self.evaluate_configs(log)

    def evaluate_configs(self, log):
        first_occurence = self._log_count[log.get_type()]['first_occurence']
        frequency = self._config[log.get_type()]['frequency']
        count = self._log_count[log.get_type()]['count']
        wait_time = self._config[log.get_type()]['wait-time']

        if not first_occurence:
            return

        if count < frequency:
            return

        self.send_to_subscribers(log.get_type())
        self._log_count[log.get_type()]['first_occurence'] = None
        self._log_count[log.get_type()]['wait_until'] = log.get_time() + wait_time
        self._log_count[log.get_type()]['count'] = 0

    def execute_leftover(self):
        for log_type, log_info in self._log_count.items():
            if log_info['count'] == self._config[log_type]['frequency']:
                self.send_to_subscribers(log_type)

    def send_to_subscribers(self, log_type):
        print(log_type, end=':\n')
        for subscriber in self._subscribers.get_subscribers_of_log_type(log_type):
            print('-', subscriber.get_name())
        print()

if __name__ == '__main__':
    subscribers = Subscribers()
    subscribers.add_subscriber(Person('Adi'), ['info'])
    subscribers.add_subscriber(Person('Kumar'), ['info', 'critical', 'warning'])
    subscribers.add_subscriber(Person('Gilang'), ['critical'])

    driver = Driver('input.txt', subscribers)
    driver.run_through_log()
