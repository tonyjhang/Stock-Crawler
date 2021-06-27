from abc import ABCMeta
from abc import abstractmethod

class Crawler:
    __metaclass__= ABCMeta
    @abstractmethod
    def crawl_data(self):
        pass