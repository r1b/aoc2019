from dataclasses import dataclass
from typing import List


IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6


@dataclass
class ImageLayer:
    pixels: List[List[int]]

    def __init__(self, pixels=None):
        self.pixels = pixels or []

    def count_color(self, color):
        count = 0

        for strip in self.pixels:
            for pixel in strip:
                if pixel == color:
                    count += 1

        return count


@dataclass
class Image:
    layers: List[ImageLayer]


def parse_image(filename):
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

    image = Image(current_layers)
    _, layer = sorted(
        ((layer.count_color(0), layer) for layer in image.layers), key=lambda x: x[0]
    )[0]

    return layer.count_color(1) * layer.count_color(2)


print(parse_image("input.txt"))
