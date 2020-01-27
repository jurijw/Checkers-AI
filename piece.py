import numpy as np


class Piece:
    def __init__(self, pos, white=True, empty=False):
        self.x, self.y = pos
        self.white = white
        self.empty = empty  # Set to True for squares without a piece
        self.crowned = False
        self.selected = False

    def __repr__(self):
        return f"Piece({(self.x, self.y)}, white={self.white}, empty={self.empty})"

    def __str__(self):
        if self.white:
            return f"{(self.x, self.y)}, white, crowned: {self.crowned}"
        else:
            return f"{(self.x, self.y)}, black, crowned: {self.crowned}"

