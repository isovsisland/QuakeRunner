#!/usr/bn/env python3
"""
111724
Quake Runner

Python tkinter GUI script to automate creation of the command-line argument to launch quake with mods.

TODO: Add text file dialog to read text file (help file) of a selected game mod.
TODO: Add entry box for entering additional mod options such as -hypnotic -quoth to be added to command before -game xxx.
"""

import os
import json
import platform

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.filedialog as tfd

from tkinter.constants import *

import QuakeFoo as qf

import tkFoo as tf

TITLE = "Quake Runner"
REFRESH_IMG = 'qrimage1.png'
QUAKERUNNER = 'qrimage2.png'
CONFIGFILE = 'qrconfig.json'

class Main(tk.Tk, tf.ScrollBarText):
    def __init__(self):
        tf.ScrollBarText.__init__(self)
        super().__init__()
        self.title(TITLE)
        self.resizable(width=True, height=True)

        self.opsys = platform.system()
        self.init_dir = str()  # Initial directory for file/folder dialog.
        self.quake = {ky:False for ky in ('engine', 'id1_folder', 'id1_pak0', 'id1_pak1', 'id1_maps', 'id1_bsp')}
        self.refresh_img = tf.pilImageTk(REFRESH_IMG, 36)
        self.quakerunner_img = tf.pilImageTk(QUAKERUNNER, 256)

        self.entryStrVar = {ky:tk.StringVar() for ky in ('engine', 'basedir', 'command')}
        self.radiobtnStrVar = tk.StringVar(value='games')
        self.comboboxStrVar = {ky:tk.StringVar(value='SELECT') for ky in ('id1_maps', 'games', 'maps')}
        self.skillChkBtnBoolVar = tk.BooleanVar(value=False)  # Checkbox to activate/deactivate skill dropdown.
        self.skillCbBoxStrVar = tk.StringVar(value='Normal')  # Dropdown box for skill selection Easy=0, Normal=1, Hard=2, Nightmare=3
        self.mapChkBtnBoolVar = tk.BooleanVar(value=False)

        rootMenu = tk.Menu(self)
        rootFrame = tk.Frame(self)
        rootFrame.pack(expand=True, fill=BOTH, pady=5, padx=5)

        # Widget Groups #
        self.menuGroup(rootMenu)
        self.inputGroup(rootFrame)
        self.modGroupDict = self.modGroup(rootFrame)  # keys = 'id1_maps', 'skill', 'games', 'map_chkbtn', 'maps'
        self.commandGroup(rootFrame)
        self.scbText(rootFrame, " Log ")
        self.processGroup(rootFrame)

        self.initConfig()  # Initialize config settings.

        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        self.minsize(width=w, height=h)
        self.mainloop()

    def menuGroup(self, root):
        settings = tk.Menu(root, tearoff=False)
        settings.add_command(label="Save", command=self.saveUserSettings)

        ui_help = tk.Menu(root, tearoff=False)
        ui_help.add_command(label="About")

        root.add_cascade(label="Settings", menu=settings)
        root.add_cascade(label="Help", menu=ui_help)

        self.config(menu=root)

    def inputGroup(self, root):
        frame = tk.Frame(root)
        frame.pack(fill=X)
        frame.columnconfigure(index=1, weight=1)

        w = 1  # Button width.

        r = 0  # Row.
        engineLabel = tk.Label(frame, text="Quake Engine:")
        engineLabel.grid(row=r, column=0, sticky=E)
        engineEntry = tk.Entry(frame, textvariable=self.entryStrVar['engine'])
        engineEntry.grid(row=r, column=1, sticky=EW, padx=5)
        fileButton = tk.Button(frame, width=w, text="...", command=self.askFile)
        fileButton.grid(row=r, column=2, sticky=W)

        r = 1  # Row.
        basedirLabel = tk.Label(frame, text="Base Directory:")
        basedirLabel.grid(row=r, column=0, sticky=E)
        basedirEntry = tk.Entry(frame, textvariable=self.entryStrVar['basedir'])
        basedirEntry.grid(row=r, column=1, sticky=EW, padx=5)
        folderButton = tk.Button(frame, width=w, text="...", command=self.askFolder)
        folderButton.grid(row=r, column=2, sticky=W, pady=5)

    def modGroup(self, root):
        frame = tk.Frame(root)
        frame.pack(fill=X)
        frame.columnconfigure(index=6, weight=1)

        imgFrame = tk.Frame(frame)
        imgFrame.grid(row=0, column=0)
        quakeRunnerLabel = tk.Label(imgFrame, image=self.quakerunner_img)  # Quake Runner with Ranger image.
        quakeRunnerLabel.grid(row=0, column=0, padx=5)

        modFrame = tk.LabelFrame(frame, text=" Mods ")
        modFrame.grid(row=0, column=1, sticky=N, padx=5)
        modFrame.columnconfigure(index=0, weight=1)

        modGroupDict = dict()  # Comboboxes 'id1_maps', 'skill', 'games', 'map_chkbtn', 'maps'
        skill = "Easy", "Normal", "Hard", "Nightmare"

        id1MapRadioBtn = tk.Radiobutton(modFrame, text="id1 Maps", value="id1_maps", variable=self.radiobtnStrVar, command=self.comboboxState)
        id1MapRadioBtn.grid(row=0, column=1, sticky=E)
        modGroupDict['id1_maps'] = ttk.Combobox(modFrame, state=DISABLED, textvariable=self.comboboxStrVar['id1_maps'])
        modGroupDict['id1_maps'].grid(row=0, column=2, sticky=EW, pady=5, padx=5)
        modGroupDict['id1_maps'].bind('<<ComboboxSelected>>', self.fillModComboBoxes)

        skillCheckbutton = tk.Checkbutton(modFrame, text="Skill", variable=self.skillChkBtnBoolVar, command=self.comboboxState)
        skillCheckbutton.grid(row=1, column=1, sticky=E)
        modGroupDict['skill'] = ttk.Combobox(modFrame, state=DISABLED, values=skill, textvariable=self.skillCbBoxStrVar)
        modGroupDict['skill'].grid(row=1, column=2, sticky=EW, pady=5, padx=5)
        modGroupDict['skill'].bind('<<ComboboxSelected>>', self.updateCMDEntry)
        # TODO: Add code to disable combobox when skill checkbox is unchecked.

        gameRadioBtn = tk.Radiobutton(modFrame, text="Games", value='games', variable=self.radiobtnStrVar, command=self.comboboxState)
        gameRadioBtn.grid(row=0, column=3, sticky=E)
        modGroupDict['games'] = ttk.Combobox(modFrame, textvariable=self.comboboxStrVar['games'])
        modGroupDict['games'].grid(row=0, column=4, sticky=EW, pady=5, padx=5)
        modGroupDict['games'].bind('<<ComboboxSelected>>', self.fillModComboBoxes)

        modGroupDict['map_chkbtn'] = tk.Checkbutton(modFrame, text="Map", variable=self.mapChkBtnBoolVar, command=self.comboboxState)
        modGroupDict['map_chkbtn'].grid(row=1, column=3, sticky=E)
        modGroupDict['maps'] = ttk.Combobox(modFrame, textvariable=self.comboboxStrVar['maps'])  # , textvariable=self.mapStrVar, values=self.map_list
        modGroupDict['maps'].grid(row=1, column=4, sticky=EW, pady=5, padx=5)
        modGroupDict['maps'].bind('<<ComboboxSelected>>', self.updateCMDEntry)  #

        refreshButton = tk.Button(modFrame, text="R", image=self.refresh_img, command=lambda: self.processUI('refresh'))
        refreshButton.grid(row=0, column=5, sticky=W, rowspan=2, padx=5)

        return modGroupDict

    def commandGroup(self, root):
        frame = tk.LabelFrame(root, text=" Command ")
        frame.pack(fill=X)
        frame.columnconfigure(index=0, weight=1)

        scbx = ttk.Scrollbar(frame, orient=HORIZONTAL)
        scbx.grid(row=1, column=0, sticky=EW, padx=5)

        r = 0  # Row.
        commandEntry = tk.Entry(frame, textvariable=self.entryStrVar['command'], xscrollcommand=scbx.set)
        commandEntry.grid(row=r, column=0, sticky=EW, padx=5)

        scbx['command'] = commandEntry.xview

    def processGroup(self, root):
        frame = tk.Frame(root)
        frame.pack(fill=X)
        frame.columnconfigure(index=0, weight=1)

        names = "Quake", "Quit"
        w = int(max([tkf.Font().measure(name) for name in names])/8)

        r = 0  # Row.
        quakeButton = tk.Button(frame, width=w, text=names[0], command=lambda: self.processUI('run'))
        quakeButton.grid(row=r, column=1, sticky=E, padx=5, pady=5)
        quitButton = tk.Button(frame, width=w, text=names[1], command=lambda: self.processUI('quit'))
        quitButton.grid(row=r, column=2, sticky=E, padx=5, pady=5)

    def initConfig(self):
        with open(CONFIGFILE) as in_file:
            settings = json.load(in_file)

        user_path = os.path.expanduser('~')
        self.init_dir = os.path.join(user_path, settings['dflt_dir'])

        if settings['engine']:
            self.entryStrVar['engine'].set(settings['engine'])
        if settings['basedir']:
            self.entryStrVar['basedir'].set(settings['basedir'])

        # TODO: Add radio & checkbox settings.

        if settings['engine'] and settings['basedir']:
            self.fillModComboBoxes()

    def processUI(self, event=None):
        match event:
            case 'refresh':
                folder = self.entryStrVar['basedir'].get()
                if folder:
                    #[self.modGroupDict[ky].delete(0,END) for ky in ('id1_maps', 'games', 'maps')]
                    for ky in ('id1_maps', 'games', 'maps'):
                        self.modGroupDict[ky].delete(0, END)
                        self.modGroupDict[ky].set('SELECT')
                    self.fillModComboBoxes(folder)
                    self.publish("Mod drop-down lists refreshed.")
            case 'run':
                command = self.entryStrVar['command'].get()
                self.run_command(command)
            case 'quit':
                self.destroy()

    def askFile(self):
        file = tfd.askopenfilename(title="Selet File, Quake Engine", initialdir=self.init_dir)  # Get user selected Quake executable.
        if file:
            self.quake['engine'] = qf.engine_check(file)  # Validate Quake engine Mac or Windows as executable.
            if self.quake['engine']:
                self.entryStrVar['engine'].set(file)  # Update UI Quake Engine with path/file string.
                folder = os.path.split(file)[0]  # Get path, strip executable file from string.
                self.quake = self.quake | qf.id1_check(folder)  # Create union between dictionaries (merge data).
                if self.quake['id1_folder'] and self.quake['id1_pak0']:  # Process engine directory as basedir if valid.
                    self.publish("id1 Folder detected in Quake Engine directory.")
                    self.entryStrVar['basedir'].set(folder)  # Update UI Base Directory with path string.
                    if self.opsys == 'Darwin':
                        self.publish("MacOS detected. A separate Base Directory is needed to load id1 mod maps.")
                    elif self.opsys == 'Windows':
                        self.publish("Windows detected.")
                    if qf.get_game_folders(folder):  # Check if mod game folders exist.
                        self.publish("Mod game folders detected in Quake Engine directory.")
                    else:
                        self.publish("Mod game folders not detected in Quake Engine directory.")
                    if self.quake['id1_bsp']:  # Check if mod maps exist.
                        self.publish("Mod maps detected in id1 folder.")
                        self.fillModComboBoxes()  # Update UI comboboxes , id1_maps, games, (game) maps
                    else:
                        self.publish("Mod maps not detected id1 folder.")
                else:
                    self.publish("id1 Folder not detected in Quake Engine directory.")
                    self.publish("id1 Folder needed in Base Directory to run Quake.")
                self.updateCMDEntry()

    def askFolder(self):
        folder = tfd.askdirectory(title="Selet Folder, Base Directory", initialdir=self.init_dir)  # Get user selected Base Directory
        if folder:
            self.entryStrVar['basedir'].set(folder)  # Update UI Base Directory with path string.
            self.publish("id1 Folder detected in Base Directory.")
            games = qf.get_game_folders(folder)
            if games:  # Check if mod game folders exist.
                self.publish("Mod game folders detected in Base Directory.")
                self.fillModComboBoxes()  # Update UI comboboxes , id1_maps, games, (game) maps
            else:
                self.publish("Mod game folders not detected in Base Directory.")
            self.updateCMDEntry()
        else:
            self.publish("id1 Folder not detected in Base Directory.")
            self.publish("id1 Folder needed in Base Directory to run Quake.")

    def fillModComboBoxes(self, event=None):
        basedir = self.entryStrVar['basedir'].get()

        id1_fldr = os.path.join(basedir, 'id1')
        id1_maps = qf.get_maps(id1_fldr)  # Get bsp files from id1 map folder
        if id1_maps:
            self.modGroupDict['id1_maps']['values'] = id1_maps

        games = qf.get_game_folders(basedir)
        if games:
            self.modGroupDict['games']['values'] = games

        game = self.comboboxStrVar['games'].get()
        if game and game != 'SELECT':
            path = os.path.join(basedir, game)
            print(path)
            self.modGroupDict['maps']['values'] = qf.get_maps(path)

        self.publish("Mod dropdown selections updated.")
        self.updateCMDEntry()

    def comboboxState(self):
        """
        Update combobox state based on Radiobutton state.
        :return: None
        """
        match self.radiobtnStrVar.get():
            case 'id1_maps':
                self.modGroupDict['id1_maps']['state'] = NORMAL
                self.modGroupDict['games']['state'] = DISABLED
                self.modGroupDict['maps']['state'] = DISABLED
                self.modGroupDict['map_chkbtn']['state'] = DISABLED
            case 'games':
                self.modGroupDict['id1_maps']['state'] = DISABLED
                self.modGroupDict['games']['state'] = NORMAL
                self.modGroupDict['maps']['state'] = NORMAL
                self.modGroupDict['map_chkbtn']['state'] = NORMAL

        if self.skillChkBtnBoolVar.get():
            self.modGroupDict['skill']['state'] = NORMAL
        elif not self.skillChkBtnBoolVar.get():
            self.modGroupDict['skill']['state'] = DISABLED
        self.updateCMDEntry()

    def updateCMDEntry(self, event=None):
        """
        Build the command to launch Quake. The code below is written in sequence for the correct order of commads.
        :param event: Required for the bind widget. Not used, set default to none.
        :return: None
        """
        command = str()

        if self.quake['engine']:
            engine = self.entryStrVar['engine'].get()
            if self.opsys == 'Darwin':  # Mac command prefix. Prefix not required for Windows.
                command = "open -a "

            if engine and os.path.exists(engine):
                command += engine  # Add engine path and executable.
            else:
                self.publish("Quake Engine issue. Please re-enter.")

            if self.opsys == 'Darwin' and engine:
                command += " --args"  # Mac executable suffix.

        folder = self.entryStrVar['basedir'].get()
        if folder and os.path.exists(folder):
            command += " -basedir "  # Add base directory (-basedir) command-line argument.
            command += folder  # Add base directory folder path.

        # add skill level
        skill = {ky:val for val, ky in enumerate(("Easy", "Normal", "Hard", "Nightmare"))}
        if self.skillChkBtnBoolVar.get() and self.quake['engine']:
            skl = self.modGroupDict['skill'].get()
            command += f" +skill {skill[skl]}"

        radiobtn_sel = self.radiobtnStrVar.get()
        id1_map = self.modGroupDict['id1_maps'].get()  # Add user map selection.
        mod_map = self.modGroupDict['maps'].get()  # Add user map selection.
        game = self.modGroupDict['games'].get()  # Add game selection.
        match radiobtn_sel:  # Add map or game command-line argument.
            case 'id1_maps':
                if id1_map and id1_map != 'SELECT':
                    command += f" +map {id1_map}"
            case 'games':
                if game and game != 'SELECT':
                    command += f" -game {game}"
                if self.mapChkBtnBoolVar.get() and mod_map and mod_map != 'SELECT':
                    command += f" +map {mod_map}"

        self.entryStrVar['command'].set(command)

    def saveUserSettings(self):
        settings = dict()
        settings['dflt_dir'] = 'Documents'
        settings['engine'] = self.entryStrVar['engine'].get()
        settings['basedir'] = self.entryStrVar['basedir'].get()

        settings['id1map_game_radbtn_state'] = self.radiobtnStrVar.get()  # Radiobutton control for id1_map & game/game map comboboxes.
        settings['skill_chkbtn_state'] = self.skillChkBtnBoolVar.get()  # Skill checkbutton state.
        settings['map_chkbtn_state'] = self.mapChkBtnBoolVar.get()  # Game map checkbutton state.

        with open('qrconfig.json', 'w') as out_file:
            json.dump(fp=out_file, obj=settings, indent=4)


if __name__ == '__main__':
    Main()