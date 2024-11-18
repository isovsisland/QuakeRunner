#!/usr/bn/env python3
"""
111724
tkFoo.py

Custom tkinter
"""

import os
import subprocess

import tkinter as tk
from audioop import error
from tkinter.constants import *
from PIL import Image, ImageTk

class ScrollBarText():
    def __init__(self):
        super().__init__()
        self.sbText = None

    def scbText(self, parent, title=""):
        frame = tk.LabelFrame(parent, text=title)  # Container for result widget, tk.Text & scrollbars.
        frame.rowconfigure(index=0, weight=1)
        frame.columnconfigure(index=0, weight=1)
        frame.pack(expand=True, fill=BOTH, pady=5, padx=5)

        scby = tk.Scrollbar(frame, orient=VERTICAL)
        scby.grid(row=0, column=1, sticky=NS)

        scbx = tk.Scrollbar(frame, orient=HORIZONTAL)
        scbx.grid(row=1, column=0, sticky=EW)

        self.sbText = tk.Text(frame, wrap=NONE, state=DISABLED, yscrollcommand=scby.set, xscrollcommand=scbx.set)
        self.sbText.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)

        scby['command'] = self.sbText.yview
        scbx['command'] = self.sbText.xview

        return self.sbText

    def publish(self, text, newline=True, cls=False):
        self.sbText['state'] = NORMAL
        if cls: self.sbText.delete('1.0', END)
        if newline: text += '\n'
        self.sbText.insert(END, text)
        self.sbText['state'] = DISABLED
        self.sbText.see(END)

    def run_command(self, cmd_str, cls=False):
        if type(cmd_str) == str:
            cmd_list = cmd_str.split(' ')
        else:
            return TypeError("<class 'str'>")

        self.sbText['state'] = NORMAL
        if cls: self.sbText.delete('1.0', END)

        p = subprocess.Popen(cmd_list, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if stderr:
            self.sbText.insert(END, stderr)
        elif stdout:
            self.sbText.insert(END, stdout)

        self.sbText.insert(END, f"\n *** Process Finished with Exit Code: {p.returncode} ***\n\n")
        self.sbText['state'] = DISABLED
        self.sbText.see(END)

        return p

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


# Test Code #
if __name__ == '__main__':
    class Main(tk.Tk, ScrollBarText):
        def __init__(self):
            super().__init__()
            ScrollBarText.__init__(self)
            self.title("Test Window")

            rootFrame = tk.Frame(self).pack(pady=5, padx=5)

            self.resultText = self.sbText(rootFrame, title=" Test Label Frame ")
            self.publish("Test Text")

            self.mainloop()


    Main()
