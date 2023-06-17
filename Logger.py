import logging
import os

class MainLogger():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.counter = 1
        self.path = f'logs/main'
        if os.path.isfile(self.path + '.log'):
            while os.path.isfile(self.path + f'_{self.counter}.log'):
                self.counter += 1
            self.path = self.path + f'_{self.counter}.log'
        else:
            self.path = self.path + '.log'
        self.fileHandler = logging.FileHandler(filename=self.path, encoding='utf-8')
        logging.basicConfig(format='[%(levelname)-10s] - %(message)s', handlers=[self.fileHandler],
                    level=logging.INFO)

    def info(self, mes):
        self.logger.info(mes)

    def error(self, mes):
        self.logger.error(mes)
