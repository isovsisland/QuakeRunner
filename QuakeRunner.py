#!/usr/bn/env python3
"""
111724
Quake Runner Dev v5

Python tkinter GUI script to automate creation of the command-line argument to launch quake with mods.

TODO: Add text file dialog to read text file (help file) of a selected game mod.
TODO: Add entry box for entering additional mod options such as -hypnotic -quoth to be added to command before -game xxx.
"""

import os
import platform

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.filedialog as tfd

from tkinter.constants import *

import foo
import tkFoo as tf
import QuakeFoo as qf


TITLE = "Quake Runner"
ICNS =  './rsrc/quakerunner.icns'
ICON =  './rsrc/quakerunner.ico'
PNG = './rsrc/quakerunner.png'
REFRESH_IMG = './rsrc/qrimage1.png'
QUAKERUNNER = './rsrc/qrimage2.png'
CONFIGFILE = './rsrc/qrconfig.json'
MODWDGTKYS = 'engine', 'basedir', 'mods_rdobtn', 'id1mps_rdobtn', 'games_rdobtn', 'skill_chkbtn', 'skill_cbobox', 'map_chkbtn'
COMBOBOXES = 'id1mps_cbobox', 'games_cbobox', 'maps_cbobox'

class Main(tk.Tk, tf.ScrollBarText):
    def __init__(self):
        tf.ScrollBarText.__init__(self)
        super().__init__()
        self.title(TITLE)
        self.resizable(width=True, height=True)

        self.opsys = platform.system()  # OS specific icon
        match self.opsys:
            case 'Darwin':
                print("Darwin")
                self.iconbitmap(ICNS)
            case 'Windows':
                self.iconbitmap(ICON)

        user_path = os.path.expanduser('~')
        self.settings = foo.readConfig(CONFIGFILE)
        if isinstance(self.settings, Exception):  # Check for exception from qrconfig.json file.
            # print("Quake Runner Config File Exception:", self.settings)
            self.settings = dict()  # Settings defined in the config file.
            self.settings['dflt_dir'] = 'Documents'
            self.init_dir = os.path.join(user_path, 'Documents')
            self.settings = {ky:'' for ky in MODWDGTKYS}
        else:
            self.init_dir = os.path.join(user_path, self.settings['dflt_dir'])

        self.refresh_img = foo.pilImageTk(REFRESH_IMG, 36)
        self.quakerunner_img = foo.pilImageTk(QUAKERUNNER, 256)

        self.entryStrVar = {ky:tk.StringVar() for ky in ('engine', 'basedir', 'command')}
        self.radiobtnStrVar = tk.StringVar(value='games')
        #self.comboboxStrVar = {ky:tk.StringVar(value='SELECT') for ky in ('id1_maps', 'mod_games', 'mod_maps')}
        self.comboboxStrVar = {ky: tk.StringVar(value='SELECT') for ky in COMBOBOXES}
        self.modChkBtnBoolVar = tk.BooleanVar(value=True)
        self.skillChkBtnBoolVar = tk.BooleanVar(value=False)  # Checkbox to activate/deactivate skill dropdown.
        self.skillCbBoxStrVar = tk.StringVar(value='Normal')  # Dropdown box for skill selection Easy=0, Normal=1, Hard=2, Nightmare=3
        self.mapChkBtnBoolVar = tk.BooleanVar(value=False)

        rootMenu = tk.Menu(self)
        rootFrame = tk.Frame(self)
        rootFrame.pack(expand=True, fill=BOTH, pady=5, padx=5)

        # Widget Groups #
        self.menuGroup(rootMenu)
        self.inputGroup(rootFrame)
        self.modGroupDict = self.modGroup(rootFrame)  # keys = 'id1_maps', 'skill_cbobox', 'games', 'map_chkbtn', 'maps'
        self.commandGroup(rootFrame)
        self.scbText(rootFrame, " Log ")
        self.buttonGroup(rootFrame)

        self.init_config()

        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        self.minsize(width=w, height=h)
        self.mainloop()

    def init_config(self):
        win_exe = self.settings['engine'].endswith('.exe')
        mac_app = self.settings['engine'].endswith('.app')

        if self.settings['engine']:
            if self.opsys == 'Windows' and win_exe:
                self.processQuakeEngine(self.settings['engine'])
            elif self.opsys == 'Darwin' and mac_app:
                self.processQuakeEngine(self.settings['engine'])

        if self.settings['basedir']:
            if self.opsys == 'Windows' and win_exe:
                self.processGameFolders(self.settings['basedir'])
            elif self.opsys == 'Darwin' and mac_app:
                print("process basedir")
                self.processGameFolders(self.settings['basedir'])

        self.modChkBtnBoolVar.set(self.settings['mods_chkbtn'])
        self.radiobtnStrVar.set(self.settings['mods_rdobtn'])  # Mod radio button -> id_maps or games.
        self.skillChkBtnBoolVar.set(self.settings['skill_chkbtn'])  # Skill check button state.
        self.skillCbBoxStrVar.set(self.settings['skill'])
        self.mapChkBtnBoolVar.set(self.settings['maps_chkbtn'])  # Map Check button state.

        self.processRadioBtns()
        self.processMapChkBtn()

    def menuGroup(self, root):
        settings = tk.Menu(root, tearoff=False)
        settings.add_command(label="Save", command=self.saveSettings)

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
        fileButton = tk.Button(frame, width=w, text="...", command=lambda: self.processUI('ask_file'))
        fileButton.grid(row=r, column=2, sticky=W)

        r = 1  # Row.
        basedirLabel = tk.Label(frame, text="Base Directory:")
        basedirLabel.grid(row=r, column=0, sticky=E)
        basedirEntry = tk.Entry(frame, textvariable=self.entryStrVar['basedir'])
        basedirEntry.grid(row=r, column=1, sticky=EW, padx=5)
        folderButton = tk.Button(frame, width=w, text="...", command=lambda: self.processUI('ask_folder'))
        folderButton.grid(row=r, column=2, sticky=W, pady=5)

    def modGroup(self, root):
        frame = tk.Frame(root)
        frame.pack(fill=X)
        frame.columnconfigure(index=6, weight=1)

        imgFrame = tk.Frame(frame)
        imgFrame.grid(row=0, column=0)
        quakeRunnerLabel = tk.Label(imgFrame, image=self.quakerunner_img)  # Quake Runner with Ranger image.
        quakeRunnerLabel.grid(row=0, column=0, padx=5)

        modFrame = tk.LabelFrame(frame, text=" Options ")
        modFrame.grid(row=0, column=1, sticky=N, padx=5)
        modFrame.columnconfigure(index=0, weight=1)

        modGroupDict = dict()  # Widgets: 'id1mps_rdobtn', 'id1mps_cbobox', 'skill_cbobox', 'games_rdobtn', 'games_cbobox', 'maps_chkbtn', 'maps_cbobox'
        skill = "Easy", "Normal", "Hard", "Nightmare"

        modChkBtn = tk.Checkbutton(modFrame, text="Use Mods", variable=self.modChkBtnBoolVar, command=self.processModChkBtn)
        modChkBtn.grid(row=0, column=0, sticky=E)

        modGroupDict['id1mps_rdobtn'] = tk.Radiobutton(modFrame, text="id1 Maps", value="id1_maps", variable=self.radiobtnStrVar, command=self.processRadioBtns)
        modGroupDict['id1mps_rdobtn'].grid(row=1, column=0, sticky=E)
        modGroupDict['id1mps_cbobox'] = ttk.Combobox(modFrame, state=DISABLED, textvariable=self.comboboxStrVar['id1mps_cbobox'])
        modGroupDict['id1mps_cbobox'].grid(row=1, column=1, sticky=EW, pady=5, padx=5)
        modGroupDict['id1mps_cbobox'].bind('<<ComboboxSelected>>', self.buildCommand)

        skillCheckbtn = tk.Checkbutton(modFrame, text="Skill", variable=self.skillChkBtnBoolVar, command=self.buildCommand)
        skillCheckbtn.grid(row=2, column=0, sticky=E)
        modGroupDict['skill_cbobox'] = ttk.Combobox(modFrame, values=skill, textvariable=self.skillCbBoxStrVar)
        modGroupDict['skill_cbobox'].grid(row=2, column=1, sticky=EW, pady=5, padx=5)
        modGroupDict['skill_cbobox'].bind('<<ComboboxSelected>>', self.buildCommand)
        # TODO: Add code to disable combobox when skill checkbox is unchecked. COMPLETE

        modGroupDict['games_rdobtn'] = tk.Radiobutton(modFrame, text="Game Mods", value='games', variable=self.radiobtnStrVar, command=self.processRadioBtns)
        modGroupDict['games_rdobtn'].grid(row=1, column=2, sticky=E)
        modGroupDict['games_cbobox'] = ttk.Combobox(modFrame, textvariable=self.comboboxStrVar['games_cbobox'])
        modGroupDict['games_cbobox'].grid(row=1, column=3, sticky=EW, pady=5, padx=5)
        modGroupDict['games_cbobox'].bind('<<ComboboxSelected>>', self.processGameMapCboBox)

        modGroupDict['maps_chkbtn'] = tk.Checkbutton(modFrame, text="Game Maps", variable=self.mapChkBtnBoolVar, command=self.processMapChkBtn)
        modGroupDict['maps_chkbtn'].grid(row=2, column=2, sticky=E)
        modGroupDict['maps_cbobox'] = ttk.Combobox(modFrame, state=DISABLED, textvariable=self.comboboxStrVar['maps_cbobox'])  # , textvariable=self.mapStrVar, values=self.map_list
        modGroupDict['maps_cbobox'].grid(row=2, column=3, sticky=EW, pady=5, padx=5)
        modGroupDict['maps_cbobox'].bind('<<ComboboxSelected>>', self.buildCommand)

        refreshButton = tk.Button(modFrame, text="R", image=self.refresh_img, command=lambda: self.processUI('refresh'))
        refreshButton.grid(row=1, column=4, sticky=W, rowspan=2, padx=5)

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

    def buttonGroup(self, root):
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

    def processUI(self, event=None):
        match event:
            case 'ask_file':
                file = tfd.askopenfilename(title="Selet File, Quake Engine", initialdir=self.init_dir)  # Get user selected Quake executable.
                if file and qf.engine_check(file):
                    self.processQuakeEngine(file)
                else:
                    self.publish("Quake Engine not detected in selected folder.")
            case 'ask_folder':
                folder = tfd.askdirectory(title="Selet Folder, Base Directory", initialdir=self.init_dir)  # Get user selected Base Directory
                if folder:
                    self.processGameFolders(folder)
            case 'refresh':
                #comboboxes = 'id1mps_cbobox', 'games_cbobox', 'maps_cbobox'
                folder = self.entryStrVar['basedir'].get()
                if folder:
                    for ky in COMBOBOXES:
                        self.modGroupDict[ky].delete(0, END)
                        self.modGroupDict[ky].set("SELECT")
                    self.processGameFolders(folder)
                    self.publish("Mod drop-down lists refreshed.")
            case 'run':
                command = self.entryStrVar['command'].get()
                self.run_command(command)
            case 'quit':
                self.destroy()

    def processQuakeEngine(self, file):
        self.publish("Quake Engine detected.", cls=True)
        self.entryStrVar['engine'].set(file)
        self.buildCommand()
        folder = os.path.split(file)[0]
        self.processGameFolders(folder)

    def processGameFolders(self, folder):
        self.clearComboBoxes()
        resources = qf.id1_check(folder)  # Folder check.
        if resources['id1_folder'] and resources['id1_pak0']:
            self.publish(f"id1 Folder and pak0.pak file detected in {folder}.")
            self.entryStrVar['basedir'].set(folder)
            self.buildCommand()
            if resources['id1_pak1']:
                self.publish("pak1.pak File detected. Note: The original release of Quake requires this file.")
            else:
                self.publish("pak1.pak File Not detected. Note: The remastered release of Quake does not require this file.")
            if resources['id1_maps']:
                self.publish("maps Folder detected.")
            if resources['id1_bsp']:
                self.publish("bsp Files detected.")
                # TODO: Populate id1 maps dropdown.
                id1_fldr = os.path.join(folder, 'id1')
                id1_maps = qf.get_maps(id1_fldr)  # Get bsp files from id1 map folder
                if id1_maps:
                    self.modGroupDict['id1mps_cbobox']['values'] = id1_maps

            games = qf.get_game_folders(folder)
            if games:
                self.publish("Game folders detected.")
                # TODO: Populate game dropdown.
                self.modGroupDict['games_cbobox']['values'] = games  # Load game combobox
        else:
            self.publish(f"id1 Folder not detected in {folder}.")

    def processModChkBtn(self):
        widgets = 'id1mps_rdobtn', 'id1mps_cbobox', 'games_rdobtn', 'games_cbobox', 'maps_chkbtn', 'maps_cbobox'
        if self.modChkBtnBoolVar.get():
            for widget in widgets:
                self.modGroupDict[widget]['state'] = NORMAL
        else:
            for widget in widgets:
                self.modGroupDict[widget]['state'] = DISABLED
                self.comboboxStrVar['maps_cbobox'].set("SELECT")
                #self.modGroupDict['maps_cbobox'].delete(0, END)
        self.buildCommand

    def processRadioBtns(self):
        """
        Update combobox state based on Radiobutton state.
        :return: None
        """
        match self.radiobtnStrVar.get():
            case 'id1_maps':
                self.modGroupDict['id1mps_cbobox']['state'] = NORMAL
                self.modGroupDict['games_cbobox']['state'] = DISABLED
                self.modGroupDict['maps_cbobox']['state'] = DISABLED
                self.modGroupDict['maps_chkbtn']['state'] = DISABLED
                self.comboboxStrVar['games_cbobox'].set("SELECT")
                self.comboboxStrVar['maps_cbobox'].set("SELECT")
                self.modGroupDict['maps_cbobox'].delete(0, END)

            case 'games':
                self.modGroupDict['id1mps_cbobox']['state'] = DISABLED
                self.modGroupDict['games_cbobox']['state'] = NORMAL
                self.modGroupDict['maps_chkbtn']['state'] = NORMAL
                if self.mapChkBtnBoolVar.get():
                    self.modGroupDict['maps_cbobox']['state'] = NORMAL
                self.comboboxStrVar['id1mps_cbobox'].set("SELECT")
        self.buildCommand()

    def processSkillChkBtn(self):
        if self.skillChkBtnBoolVar.get():
            self.modGroupDict['skill_cbobox']['state'] = NORMAL
        elif not self.skillChkBtnBoolVar.get():
            self.modGroupDict['skill_cbobox']['state'] = DISABLED

    def processMapChkBtn(self):
        if self.mapChkBtnBoolVar.get():
            self.modGroupDict['maps_cbobox']['state'] = NORMAL
        #elif not self.skillChkBtnBoolVar.get():
        else:
            self.modGroupDict['maps_cbobox']['state'] = DISABLED
            self.comboboxStrVar['maps_cbobox'].set('SELECT')
        self.buildCommand()

    def processGameMapCboBox(self, event=None):
        basedir = self.entryStrVar['basedir'].get()
        game = self.comboboxStrVar['games_cbobox'].get()
        if basedir and game and game != 'SELECT':
            path = os.path.join(basedir, game)
            maps = qf.get_maps(path)
            if maps:
                self.modGroupDict['maps_cbobox']['values'] = maps
            else:
                #self.modGroupDict['maps_cbobox']['values'] = ''
                self.modGroupDict['maps_cbobox'].delete(0,END)
                self.comboboxStrVar['maps_cbobox'].set('SELECT')
            self.buildCommand()

    def buildCommand(self, event=None):
        """
        Build the command to launch Quake. The code below is written in sequence for the correct order of commads.
        :param event: Required for the bind widget. Not used, set default to none.
        :return: None
        """
        command = str()
        engine = self.entryStrVar['engine'].get()
        basedir = self.entryStrVar['basedir'].get()

        if  engine and basedir:
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
            if self.skillChkBtnBoolVar.get() and engine and basedir:
                skl = self.modGroupDict['skill_cbobox'].get()
                command += f" +skill {skill[skl]}"

            mod_switch = self.modChkBtnBoolVar.get()
            radiobtn_sel = self.radiobtnStrVar.get()
            id1_map = self.modGroupDict['id1mps_cbobox'].get()  # Add user map selection.
            mod_map = self.modGroupDict['maps_cbobox'].get()  # Add user map selection.
            game = self.modGroupDict['games_cbobox'].get()  # Add game selection.
            if mod_switch:
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

    def saveSettings(self):
        self.settings['dflt_dir'] = os.path.split(self.init_dir)[1]
        self.settings['engine'] = self.entryStrVar['engine'].get()  # Quake Engine.
        self.settings['basedir'] = self.entryStrVar['basedir'].get()  # Base Directory.
        self.settings['mod_chkbtn'] = self.modChkBtnBoolVar.get()
        self.settings['mod_rdobtn'] = self.radiobtnStrVar.get()  # Mod radio button -> id_maps or games.
        self.settings['skill_chkbtn'] = self.skillChkBtnBoolVar.get()  # Skill check button state.
        self.settings['skill_cbobox'] = self.skillCbBoxStrVar.get()
        self.settings['map_chkbtn'] = self.mapChkBtnBoolVar.get()  # Map Check button state.

        status = foo.writeConfig(file=CONFIGFILE, settings=self.settings)
        if status:
            self.publish("Settings saved.")
        else:
            self.publish(status)

    def clearComboBoxes(self):
        for ky in COMBOBOXES:
            self.modGroupDict[ky].delete(0, END)
            self.comboboxStrVar[ky].set("SELECT")


if __name__ == '__main__':
    Main()