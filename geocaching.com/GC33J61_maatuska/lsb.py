#!/usr/bin/env python3

from PIL import Image

im = Image.open('s4.png')
px = im.load()

for x in range(im.width):
    for y in range(im.height):
      px[x,y] = tuple([(((c & 3) << 6) & 255) for c in px[x,y]])

im.save('result.png')
