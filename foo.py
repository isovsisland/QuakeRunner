#!/usr/bin/env python3
"""
112024
foo.py

Support functions.
"""
import json
from PIL import Image, ImageTk

def pilImageTk(file, size=None):
    """
    PIL Image manipulation for tkinter.

    :param file: Path & name to image file.
    :param size: int resizes image and maintains size Ratio.
                 tuple(width, height) to specify size.
                 None, does not resize the image.
    :return: PIL Image Object for Tk.
    """
    try:
        image = Image.open(file)
    except OSError as err:
        return err

    if not size:  # Do not resize. Use existing image size
        size = image.size

    elif type(size) == int:
        if image.size[0] == image.size[1]:  # Resize image based on user input.
            size = (size, size)  # Use the same value for width & height.
        elif image.size[0] > image.size[1]:  # Calculate ratio if width > height.
            ratio = image.size[1] / image.size[0]
            size = (size, int(size * ratio))
        elif image.size[0] < image.size[1]:  # Calculate ratio if wdith < height.
            ratio = image.size[0] / image.size[1]
            size = (int(size * ratio), size)

    image = image.resize(size=size, resample=Image.LANCZOS)

    return ImageTk.PhotoImage(image)

def readConfig(file):
    try:
        with open(file) as in_file:
            settings = json.load(in_file)
    except Exception as err:
        return err
    else:
        return settings

def writeConfig(file, settings):
    try:
        with open(file, 'w') as out_file:
            json.dump(fp=out_file, obj=settings, indent=4)
    except OSError as err:
        return err
    else:
        return True

