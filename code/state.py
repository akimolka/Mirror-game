import enum


class State(enum.Enum):
    draw_mirrors = 0
    define_start = 1
    define_finish = 2
    choose_direction = 3
    animation = 4
    victory = 5

    def next(self):
        v = self.value + 1
        if v > 5:
            raise ValueError('Enumeration ended')
        return State(v)
