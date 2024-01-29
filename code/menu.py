class Menu:
    def __init__(self, widgets):
        self.widgets = widgets

    def handle_input(self, event):
        for widget in self.widgets:
            widget.handle_input(event)

    def draw(self, screen):
        for widget in self.widgets:
            widget.draw(screen)
