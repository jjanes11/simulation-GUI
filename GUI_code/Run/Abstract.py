from PyQt5.QtWidgets import QWidget
from sip import wrappertype as pyqtWrapperType
from abc import ABCMeta, abstractmethod


class AbstractMeta(pyqtWrapperType, ABCMeta):
    pass


class Controller(QWidget, metaclass=AbstractMeta):
    
    @abstractmethod
    def notification(self):
        pass


class View(QWidget, metaclass=AbstractMeta):

    def __init__(self, controller: Controller = None) -> None:
        QWidget.__init__(self)
        self._controller = controller

    @property
    def controller(self) -> Controller:
        return self._controller

    @controller.setter
    def controller(self, controller: Controller) -> None:
        self._controller = controller

    @abstractmethod
    def init_UI(*args):
        pass


class Selector(QWidget, metaclass=AbstractMeta):
    
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def state(self):
        pass

    # @abstractmethod
    # def add_observer(self):
    #     pass

    # @abstractmethod
    # def notify(self):
    #     pass