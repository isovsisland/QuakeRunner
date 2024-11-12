#!/usr/bin/env python3

"""
110224
QuakeRunner.py

Assembles commands to launch Quake with a user selected mod (game or map).
"""

import os
import json
import platform

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.filedialog as tfd
import tkinter.messagebox as tmb
from tkinter.constants import *
import idlelib.tooltip as it

import TkFoo as tfoo
import QuakeFoo as qf

TITLE = "Quake Runner"
BTNWIDTH = 1
DFLTDIR = "Documents"
SELECTION = 'engine', 'basedir'
CONFIGFILE = "config.json"
REFRESH_IMG = "Quake Ouroboros.png"
SKILL = "Easy", "Normal", "Hard", "Nightmare"

class Main(tk.Tk, tfoo.ScrollBarText):
    def __init__(self):
        super().__init__()
        tfoo.ScrollBarText.__init__(self)
        self.title(TITLE)
        self.resizable(width=True, height=True)

        self.opsys = platform.system()
        user_path = os.path.expanduser('~')
        self.dflt_dir = os.path.join(user_path, DFLTDIR)

        self.id = False

        self.refresh_img = tfoo.pilImageTk(REFRESH_IMG, 36)

        self.entryStrVar = {s:tk.StringVar() for s in SELECTION}
        self.modOptStrVar = tk.StringVar(value="game_mods")
        self.gameStrVar = tk.StringVar(value="SELECT")
        self.mapStrVar = tk.StringVar(value="SELECT")
        self.modStrVar = tk.StringVar(value='game')
        self.skillStrVar = tk.StringVar(value="Normal")
        self.launchCmdStrVar = tk.StringVar()
        self.modComboBox = dict()
        self.game_list = list()
        self.map_list = list()

        rootFrame = tk.Frame(self)
        rootFrame.pack(expand=True, fill=BOTH, pady=5, padx=5)

        self.menuGroup()
        self.inputGroup(rootFrame)
        self.modComboBox['games'], self.modComboBox['maps'] = self.gameGroup(rootFrame)
        self.commandGroup(rootFrame)
        self.scbText(rootFrame, title=" Log ")
        self.buttonGroup(rootFrame)

        self._setSelections()

        # Set Minimum Size, Center the Window & Start Main Loop #
        self.update_idletasks()  # Update widgets to get accurate sizes.
        win_width = self.winfo_width()
        win_height = self.winfo_height()
        self.minsize(width=win_width, height=win_height)  # Set window minimum size.
        self.eval("tk::PlaceWindow . center")

        self.mainloop()

    def menuGroup(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='File', menu=filemenu)

        filemenu.add_command(label='Save Selections', command=lambda: self.processUI('save'))
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=lambda: self.processUI('quit'))

        editmenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Help', menu=editmenu)

        editmenu.add_command(label='About')  # TODO: Add about dialog
        editmenu.add_separator()
        editmenu.add_command(label='QuakePy Compiler')  # TODO: Add QuakePy Compiler help.
        editmenu.add_command(label='Quake Console Commands')  # TODO: Add Quake console command help.

    def inputGroup(self, parent):
        frame = tfoo.baseFrame(parent)
        frame.columnconfigure(index=1, weight=1)

        engineLabel = tk.Label(frame, text="Quake Engine:")
        engineLabel.grid(row=0, column=0, sticky=E)
        engineEntry = tk.Entry(frame, textvariable=self.entryStrVar['engine'])
        engineEntry.grid(row=0, column=1, sticky=EW, padx=5)
        engineButton = tk.Button(frame, width=BTNWIDTH, text="...", command=lambda: self.selectFile('engine'))
        engineButton.grid(row=0, column=2, sticky=W)
        it.Hovertip(engineButton, text="Get File Dialog")

        basedirLabel = tk.Label(frame, text="Base Directory:")
        basedirLabel.grid(row=1, column=0, sticky=E)
        basedirEntry = tk.Entry(frame, textvariable=self.entryStrVar['basedir'])
        basedirEntry.grid(row=1, column=1, sticky=EW, padx=5)
        basedirButton = tk.Button(frame, width=BTNWIDTH, text="...", command=lambda: self.selectDir('basedir'))
        basedirButton.grid(row=1, column=2, sticky=W, pady=5)
        it.Hovertip(basedirButton, text="Get Folder Dialog")

    def gameGroup(self, parent):
        frame = tfoo.baseFrame(parent)
        frame.columnconfigure(index=0, weight=1)

        gameRadioButton = tk.Radiobutton(frame, text="Game List:", value="game", variable=self.modStrVar, command=lambda: self.launchCommand('game'))
        gameRadioButton.grid(row=0, column=1, sticky=E)
        gameList = ttk.Combobox(frame, textvariable=self.gameStrVar, values=self.game_list)
        gameList.grid(row=0, column=2, sticky=EW, pady=10)
        gameList.bind('<<ComboboxSelected>>', self.launchCommand)

        spacer = tk.Frame(frame)
        spacer.grid(row=0, column=3, sticky=EW, padx=10)

        mapRadioButton = tk.Radiobutton(frame, text="Map List:", value="map", variable=self.modStrVar, command=lambda: self.launchCommand('map'))
        mapRadioButton.grid(row=0, column=4, sticky=E)
        mapList = ttk.Combobox(frame, textvariable=self.mapStrVar, values=self.map_list)
        mapList.grid(row=0, column=5, sticky=EW, pady=10)
        mapList.bind('<<ComboboxSelected>>', self.launchCommand)

        refreshButton = tk.Button(frame, text="R", image=self.refresh_img, command=lambda: self.processUI('refresh'))
        refreshButton.grid(row=0, column=6, sticky=W, padx=5)
        it.Hovertip(refreshButton, text="Refresh Game & Map List")

        return gameList, mapList

    def commandGroup(self, parent):
        frame = tfoo.baseFrame(parent)
        frame.columnconfigure(index=1, weight=1)

        commandLabel = tk.Label(frame, text="Launch Command:")
        commandLabel.grid(row=0, column=0, sticky=E)
        commandEntry = tk.Entry(frame, textvariable=self.launchCmdStrVar)
        commandEntry.grid(row=0, column=1, sticky=EW, pady=15)

    def buttonGroup(self, parent):
        frame = tfoo.baseFrame(parent)
        frame.columnconfigure(index=0, weight=1)

        labels = "Quake", "Quit"
        btn_width = int(max([tkf.Font().measure(text=l) for l in labels])/8.5)  # Measure text to set the width of the button.

        quakeButton = tk.Button(frame, width=btn_width, text=labels[0], command=lambda: self.processUI('quake'))
        quakeButton.grid(row=0, column=0, sticky=E, pady=5, padx=5)

        quitButton = tk.Button(frame, width=btn_width, text=labels[1], command=lambda: self.processUI('quit'))
        quitButton.grid(row=0, column=1, sticky=E)

    def processUI(self, event):
        match event:
            case 'refresh':
                folder = self.entryStrVar['basedir'].get()
                if folder:
                    self._fillComboBox(folder)
                    self.publish("Mod dropdowns have been refreshed.\n", cls=True)
            case 'save':
                selections = self._getSelections()
                if selections:
                    with open(CONFIGFILE, 'w') as out_file:
                        json.dump(obj=selections, fp=out_file, indent=4)
            case 'quake':
                command = self.launchCmdStrVar.get()
                if command:
                    cwd = os.getcwd()
                    cmd = command.split(' ')
                    if self.opsys == 'Darwin':
                        idx = 2
                    elif self.opsys == 'Windows':
                        idx = 0
                    port_path = os.path.split(cmd[idx])
                    os.chdir(port_path[0])
                    cmd[idx] = port_path[1]
                    self.launch(cmd)
                    os.chdir(cwd)
            case 'quit':
                self.destroy()

    def selectDir(self, event):
        folder = tfd.askdirectory(initialdir=self.dflt_dir)
        if folder:
            id_check = qf.id_check(folder)
            if id_check['id_valid']:
                self.entryStrVar[event].set(folder)
                self.publish("id1 Folder detected in Base directory.\n")
                self._fillComboBox(folder)
                if id_check['maps_fldr']:
                    self.modComboBox['maps']['values'] = qf.get_maps(folder)
            else:
                self.publish("id1 Folder not detected in Base directory.\n", cls=True)
            self.launchCommand()

    def selectFile(self, event):
        file_path = tfd.askopenfilename(initialdir=self.dflt_dir)
        if file_path:
            self.entryStrVar[event].set(file_path)
            id_check = qf.id_check(file_path)
            if id_check['id_valid']:
                eng_fldr = os.path.split(file_path)[0]
                self.entryStrVar['basedir'].set(eng_fldr)
                self.publish("id1 Folder detected in Quake engine directory.\n")
                if id_check['maps_fldr']:
                    self.mapStrVar.set(qf.get_games(eng_fldr))
            else:
                self.publish("id1 Folder not detected in Quake engine directory.\n", cls=True)
            self.launchCommand()

    def launchCommand(self, event=None):
        eng, base, game_mod, map_mod = self._getSelections().values()
        match self.modStrVar.get():
            case 'game':
                mod = f"-game {game_mod}"
                self.publish("Game dropdown list selected.\n")
            case 'map':
                mod = f"+map {map_mod}"
                self.publish("Map dropdown list selected.\n")
        if self.opsys == 'Windows':
            self.launchCmdStrVar.set(f'{eng} -basedir {base} {mod}')
        if self.opsys == 'Darwin':
            self.launchCmdStrVar.set(f'open -a {eng} --args -basedir {base} {mod}')

    def _getSelections(self):
        user_selections = {s:self.entryStrVar[s].get() for s in SELECTION}
        user_selections['game'] = self.modComboBox['games'].get()
        user_selections['map'] = self.modComboBox['maps'].get()
        return user_selections

    def _setSelections(self):
        try:
            with open(CONFIGFILE) as in_file:
                selections = json.load(in_file)
        except IOError as err:
            pass
        else:

            if os.path.exists(selections['engine']) and os.path.exists(selections['basedir']):
                self.dflt_dir = os.path.split(selections['basedir'])[0]
                [self.entryStrVar[s].set(selections[s]) for s in SELECTION]
                self._fillComboBox(folder=selections['basedir'])
                self.modComboBox['games'].set(selections['game'])
                self.modComboBox['maps'].set(selections['map'])
                self.launchCommand()

    def _fillComboBox(self, folder):
        self.gameStrVar.set("SELECT")
        self.mapStrVar.set("SELECT")
        self.modComboBox['games']['values'] = qf.get_games(folder)
        self.modComboBox['maps']['values'] = qf.get_maps(folder)

if __name__ == '__main__':
    Main()
