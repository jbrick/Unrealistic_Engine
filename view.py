import pygame
import model
from eventmanager import*
from abc import ABCMeta


class View():
    __metaclass__ = ABCMeta

    @abstractclass
    def __init__(self, model):
        pass

    @abstractclass
    def render_game(self, game):
        pass

    @abstractclass
    def render_character(self, character):
        pass