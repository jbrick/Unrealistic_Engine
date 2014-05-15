import pygame
import model
from eventmanager import*
from abc import ABCMeta


class Controller():
    __metaclass__ = ABCMeta

    @abstractclass
    def __init__(self, model):
        pass

    @abstractclass
    def quit_game(self, model):
        pass

    @abstractclass
    def key_input(self):
        pass

    @abstractclass
    def mouse_input(self):
        pass

    def register_listener(self, listener):
        self.listeners[listener] = 1