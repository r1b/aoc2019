from dataclasses import dataclass
from enum import IntEnum
from typing import List

from PIL import Image as Image_


IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6


class Color(IntEnum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2


@dataclass
class ImageLayer:
    pixels: List[List[int]]

    @classmethod
    def normalize_pixel(cls, p1, p2):
        if p1 == Color.TRANSPARENT:
            return p2
        return p1

    # XXX: This mutates other - sorry god
    def __and__(self, other):
        for i in range(IMAGE_HEIGHT):
            for j in range(IMAGE_WIDTH):
                other[(i,j)] = self.normalize_pixel(self[(i,j)], other[(i,j)])
        return other

    def __getitem__(self, key):
        i, j = key
        return self.pixels[i][j]

    def __setitem__(self, key, value):
        i, j = key
        self.pixels[i][j] = value


@dataclass
class Image:
    layers: List[ImageLayer]

    @classmethod
    def parse(cls, filename):
        current_layers = []
        current_layer = []
        current_strip = []

        for i, pixel in enumerate(open(filename).read().strip()):
            current_strip.append(int(pixel))

            i += 1

            if i != 0:
                if i % IMAGE_WIDTH == 0:
                    current_layer.append(current_strip)
                    current_strip = []
                if i % (IMAGE_WIDTH * IMAGE_HEIGHT) == 0:
                    current_layers.append(ImageLayer(current_layer))
                    current_layer = []

        return cls(current_layers)

    def decode(self):
        normalized_layer = None

        for i in range(len(self.layers) - 1):
            normalized_layer = self.layers[i] & self.layers[i + 1]

        image = Image_.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), "black")
        pixels = image.load()

        for i in range(IMAGE_WIDTH):
            for j in range(IMAGE_HEIGHT):
                # XXX: Lol rows / columns are reversed in our layer
                pixels[i,j] = (255,255,255) if normalized_layer[(j,i)] == 0 else (0,0,0)

        image.show()

Image.parse("input.txt").decode()
