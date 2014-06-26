import pygame


# Any class the renders models to the screen should inherit from View, and
# implement the required methods.
class View():

    BACKGROUND = 1
    FOREGROUND = 2
    OVERLAY = 99

    def __init__(self):
        # We maintain a dictionary mapping a model to the function to call to
        # render said model, as well as the position of where to render it.
        self.visible_models = {}

    def render(self, screen):
        for model in self.visible_models:
            # Find the tuple (renderfunction, position) for the current model.
            # Call the associated render function
            if self.visible_models[model][2] == View.BACKGROUND:
                self.visible_models[model][0](model, screen)

        for model in self.visible_models:
            # Find the tuple (renderfunction, position) for the current model.
            # Call the associated render function
            if self.visible_models[model][2] == View.FOREGROUND:
                self.visible_models[model][0](model, screen,
                                              self.visible_models[model][1])

        pygame.display.flip()

    def add_model(self, model, render_function, position, priority):
        self.visible_models[model] = (render_function, position, priority)

    def remove_model(self, model):
        del self.visible_models[model]

    def set_visible_model_position(self, model, position):
        self.visible_models[model] = (self.visible_models[model][0],
                                      position, self.visible_models[model][2])

    def get_visible_model_position(self, model):
        return self.visible_models[model][1]
