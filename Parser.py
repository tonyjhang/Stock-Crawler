from abc import ABCMeta
from abc import abstractmethod

class Parser:
    __metaclass__= ABCMeta
    @abstractmethod
    def parse_data(self):
        pass