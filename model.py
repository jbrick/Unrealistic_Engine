import pygame
from eventmanager import *
from abc import ABCMeta


class Model():
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_application(self):
        pass

    @abstractmethod
    def save_game(self, game):
        pass

    @abstractmethod
    def save_character(self, character):
        pass
