import pygame
from sets import Set


# Any class the renders models to the screen should inherit from View, and 
# implement the required methods.
class View():

    def __init__(self):
        # We maintain a dictionary mapping a model to the function to call to
        # render said model, as well as the position of where to render it.
        self.visible_models = {}

    @staticmethod
    def render_character(character, position, screen):
        raise NotImplementedError("Please Implement this method")

    def render(self, screen):
        for model in self.visible_models:
            # Find the tuple (renderfunction, position) for the current model.
            # Call the associated render function
            self.visible_models[model][0](model, self.visible_models[model][1], screen)
        pygame.display.flip()

    def add_model(self, model, render_function, position):
        self.visible_models[model] = (render_function, position)

    def remove_model(self, model):
        del self.visible_models[model]

    def set_visible_model_position(self, model, position):
        self.visible_models[model] = (self.visible_models[model][0], position)

    def get_visible_model_position(self, model):
        return self.visible_models[model][1]
