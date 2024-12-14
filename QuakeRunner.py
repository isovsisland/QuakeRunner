#!/usr/local/bin/python3

"""
120224
Python 3.12.7
Dev version 5.3
Release version 1.0

QuakeRunner.py - Main windows application.
Support Files: foo.py - various non-tkinter related functions.
               tkfoo.py - custom tkinter class of the tk.Text widget with scrollbars, printing to the Text widget and
                          execution of the instructions to launch the Quake game.
               QuakeFoo.py - various Quake Runner specific functions to process game data.
               rsrc - resource folder.
               |_ qrconfig.json - Quake Runner configuration file with settings for the app.
               |_ qrimage1.png - Refresh button image, ouroborus surrounding the Quake symbol.
               |_ qrimage2.png - Quake Runner image, Quake symbol + title + Quake ranger.
               |_ qrimage3.png - Help button image, Quake symbol with red cross.
               |_ quakerunner.icns - Quake Runner MacOS icon.
               |_ quakerunner.ico - Quake Runner Windows icon.
               |_ quakerunner.png - Quake Runner png file for the tkinter window and dialogs.

Purpose: Python script to assist in the creation of command-line arguments to launch id Software's Quake game with
         fan baseds mods, maps and associated Quake engine options.

"""

import os
import platform

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.filedialog as tfd
import tkinter.messagebox as tmb
import idlelib.tooltip as it

from tkinter.constants import *

import foo
import tkFoo as tf
import QuakeFoo as qf

TITLE = "Quake Runner"
ICNS =  'rsrc/quakerunner.icns'
ICON =  'rsrc/quakerunner.ico'
PNG = 'rsrc/quakerunner.png'
REFRESHBTNPNG = 'rsrc/qrimage1.png'
QUAKERUNNERIMGPNG = 'rsrc/qrimage2.png'
QUAKEHELP = 'rsrc/qrimage3.png'
CONFIGFILE = 'rsrc/qrconfig.json'
MODWDGTKYS = 'dflt_dir', 'engine', 'basedir', 'mods_chkbtn', 'mods_rdobtn', 'skill_chkbtn', 'skill_cbobox', 'maps_chkbtn'  # , 'id1mps_rdobtn', 'games_rdobtn'
COMBOBOXES = 'id1mps_cbobox', 'games_cbobox', 'maps_cbobox', 'readme_cbobox'

class Main(tk.Tk, tf.ScrollBarText):
    def __init__(self):
        tf.ScrollBarText.__init__(self)
        super().__init__()
        self.title(TITLE)
        self.resizable(width=True, height=True)

        self.opsys = platform.system()  # OS specific icon for the application.
        match self.opsys:
            case 'Darwin':
                self.iconbitmap(ICNS)
            case 'Windows':
                self.iconbitmap(ICON)

        img = tk.PhotoImage(file=PNG)  # Image icon for the window and dialogs.
        self.iconphoto(True, img)

        self.qr_cfg = foo.readConfig(CONFIGFILE)
        if isinstance(self.qr_cfg, Exception):  # If no config file then use defaults.
            self.qr_cfg = qf.set_config_dflt()

        self.refresh_img = foo.pilImageTk(REFRESHBTNPNG, 36)
        self.help_img = foo.pilImageTk(QUAKEHELP, 36)
        self.quakerunner_img = foo.pilImageTk(QUAKERUNNERIMGPNG, 256)

        self.init_dir = ''  # Set initial directory to empty string for file/folder dialog boxes.
        self.entryStrVar = {ky:tk.StringVar() for ky in ('engine', 'basedir', 'command')}
        self.comboboxStrVar = {ky: tk.StringVar(value='SELECT') for ky in COMBOBOXES}

        # Set widget states, use defaults if no config file #
        self.modChkBtnBoolVar = tk.BooleanVar(value=self.qr_cfg['mods_chkbtn'])
        self.radiobtnStrVar = tk.StringVar(value=self.qr_cfg['mods_rdobtn'])
        self.skillChkBtnBoolVar = tk.BooleanVar(value=self.qr_cfg['skill_chkbtn'])  # Checkbox to activate/deactivate skill dropdown.
        self.skillCbBoxStrVar = tk.StringVar(value=self.qr_cfg['skill_cbobox'])  # Dropdown box for skill selection Easy=0, Normal=1, Hard=2, Nightmare=3
        self.mapChkBtnBoolVar = tk.BooleanVar(value=self.qr_cfg['maps_chkbtn'])

        # Root Widgets. #
        rootMenu = tk.Menu(self)
        rootFrame = tk.Frame(self)
        rootFrame.pack(expand=True, fill=BOTH, pady=5, padx=5)

        # Widget Groups #
        self.menuWidgets(rootMenu)
        self.inputWidgets(rootFrame)
        self.cboboxDict = self.modWidgets(rootFrame)  # keys = 'id1_maps', 'skill_cbobox', 'games', 'map_chkbtn', 'maps'
        self.commandWidgets(rootFrame)
        self.scbText(rootFrame, " Log ")
        self.buttonWidgets(rootFrame)

        self.init_config()

        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        self.minsize(width=w, height=h)
        self.mainloop()

    def init_config(self):
        # Set or get initial directory for file/folder dialogs. #
        if self.qr_cfg['dflt_dir']:
            self.init_dir = self.qr_cfg['dflt_dir']
        else:
            self.publish("Default Directory not set.")
            self.after(500, self.set_dfltdir)

        engine = self.qr_cfg['engine']
        if engine:
            if self.opsys == 'Windows' and engine.endswith('.exe') and os.access(engine, os.X_OK):  # Populate entry only if valid Windows executable
                self.processQuakeEngine(self.qr_cfg['engine'])
            elif self.opsys == 'Darwin' and engine.endswith('.app') and engine.isdir() or self.opsys == 'Darwin' and engine.endswith('') and os.access(engine, os.X_OK):  # Populate entry only if valid Mac executable
                self.processQuakeEngine(self.qr_cfg['engine'])

        basedir = self.qr_cfg['basedir']
        if basedir:
            if self.opsys == 'Windows' and os.path.isdir(basedir):  # Populate entry only if valid Windows directory
                self.processGameFolders(self.qr_cfg['basedir'])
            if self.opsys == 'Darwin' and os.path.isdir(basedir):  # Populate entry only if valid Mac directory
                self.processGameFolders(self.qr_cfg['basedir'])

        self.processModChkBtn()
        self.processRadioBtns()
        self.processSkillChkBtn()
        self.processMapChkBtn()

    def menuWidgets(self, root):
        settings = tk.Menu(root, tearoff=False)
        settings.add_command(label="Save Settings", command=self.saveSettings)
        settings.add_command(label="Default Directory", command=lambda: self.processUI('ask_dfltdir'))

        ui_help = tk.Menu(root, tearoff=False)
        ui_help.add_command(label="About", command=lambda: tmb.showinfo(self, message="Quake Runner\nVersion 1.0"))

        root.add_cascade(label="Settings", menu=settings)
        root.add_cascade(label="Help", menu=ui_help)

        self.config(menu=root)

    def inputWidgets(self, root):
        """
        Widgets for the entry for the Quake engine and base directory.

        :param root: Root Frame of the window.
        :return: None
        """

        frame = tk.Frame(root)
        frame.pack(fill=X)
        frame.columnconfigure(index=1, weight=1)

        w = 1  # Button width.

        r = 0  # Row.
        engineLabel = tk.Label(frame, text="Quake Engine:")
        engineLabel.grid(row=r, column=0, sticky=E)
        engineEntry = tk.Entry(frame, textvariable=self.entryStrVar['engine'])
        engineEntry.grid(row=r, column=1, sticky=EW, padx=5)
        it.Hovertip(engineEntry, text="Path+File to Quake Engine")
        fileButton = tk.Button(frame, width=w, text="...", command=lambda: self.processUI('ask_file'))
        fileButton.grid(row=r, column=2, sticky=W)
        it.Hovertip(fileButton, text="File Selection Dialog")

        r = 1  # Row.
        basedirLabel = tk.Label(frame, text="Base Directory:")
        basedirLabel.grid(row=r, column=0, sticky=E)
        basedirEntry = tk.Entry(frame, textvariable=self.entryStrVar['basedir'])
        basedirEntry.grid(row=r, column=1, sticky=EW, padx=5)
        it.Hovertip(basedirEntry, text="Path to id1 sub-folder & mods")
        folderButton = tk.Button(frame, width=w, text="...", command=lambda: self.processUI('ask_folder'))
        folderButton.grid(row=r, column=2, sticky=W, pady=5)
        it.Hovertip(folderButton, text="Folder Selection Dialog")

    def modWidgets(self, root):
        """
        Widgets for the selection of mod maps or folders, skill level and readme text files.

        :param root: Root frame of the window.
        :return: None
        """

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

        cboboxDict = dict()  # Widgets: 'id1mps_rdobtn', 'id1mps_cbobox', 'skill_cbobox', 'games_rdobtn', 'games_cbobox', 'maps_chkbtn', 'maps_cbobox'
        skill = "Easy", "Normal", "Hard", "Nightmare"

        modChkBtn = tk.Checkbutton(modFrame, text="Use Mods", variable=self.modChkBtnBoolVar, command=self.processModChkBtn)
        modChkBtn.grid(row=0, column=0, sticky=E)
        it.Hovertip(modChkBtn, text="Enable/Disable Mod Options")

        cboboxDict['id1mps_rdobtn'] = tk.Radiobutton(modFrame, text="id1 Maps", value="id1_maps", variable=self.radiobtnStrVar, command=self.processRadioBtns)
        cboboxDict['id1mps_rdobtn'].grid(row=1, column=0, sticky=E)
        it.Hovertip(cboboxDict['id1mps_rdobtn'], text="Enable id1 maps Selections")
        cboboxDict['id1mps_cbobox'] = ttk.Combobox(modFrame, textvariable=self.comboboxStrVar['id1mps_cbobox'])
        cboboxDict['id1mps_cbobox'].grid(row=1, column=1, sticky=EW, pady=5, padx=5)
        cboboxDict['id1mps_cbobox'].bind('<<ComboboxSelected>>', self.buildCommand)
        it.Hovertip(cboboxDict['id1mps_cbobox'], text="id1 maps Dropdown List")

        skillCheckbtn = tk.Checkbutton(modFrame, text="Skill", variable=self.skillChkBtnBoolVar, command=self.processSkillChkBtn)
        skillCheckbtn.grid(row=2, column=0, sticky=E)
        it.Hovertip(skillCheckbtn, text="Enable/Disable Skill Selection")
        cboboxDict['skill_cbobox'] = ttk.Combobox(modFrame, values=skill, textvariable=self.skillCbBoxStrVar)
        cboboxDict['skill_cbobox'].grid(row=2, column=1, sticky=EW, pady=5, padx=5)
        cboboxDict['skill_cbobox'].bind('<<ComboboxSelected>>', self.buildCommand)

        cboboxDict['games_rdobtn'] = tk.Radiobutton(modFrame, text="Game Mods", value='games', variable=self.radiobtnStrVar, command=self.processRadioBtns)
        cboboxDict['games_rdobtn'].grid(row=1, column=2, sticky=E)
        it.Hovertip(cboboxDict['games_rdobtn'], text="Enable mod Selections")
        cboboxDict['games_cbobox'] = ttk.Combobox(modFrame, textvariable=self.comboboxStrVar['games_cbobox'])
        cboboxDict['games_cbobox'].grid(row=1, column=3, sticky=EW, pady=5, padx=5)
        cboboxDict['games_cbobox'].bind('<<ComboboxSelected>>', self.processGameMapCboBox)
        it.Hovertip(cboboxDict['games_cbobox'], text="mod Dropdown List")

        cboboxDict['maps_chkbtn'] = tk.Checkbutton(modFrame, text="Game Maps", variable=self.mapChkBtnBoolVar, command=self.processMapChkBtn)
        cboboxDict['maps_chkbtn'].grid(row=2, column=2, sticky=E)
        it.Hovertip(cboboxDict['maps_chkbtn'], text="Enable/Disable mod maps Selections")
        cboboxDict['maps_cbobox'] = ttk.Combobox(modFrame, textvariable=self.comboboxStrVar['maps_cbobox'])
        cboboxDict['maps_cbobox'].grid(row=2, column=3, sticky=EW, pady=5, padx=5)
        cboboxDict['maps_cbobox'].bind('<<ComboboxSelected>>', self.buildCommand)
        it.Hovertip(cboboxDict['maps_cbobox'], text="mod maps Dropdown List")

        readmeLabel = tk.Label(modFrame, text="Mod Info")
        readmeLabel.grid(row=3, column=2, sticky=E)
        cboboxDict['readme_cbobox'] = ttk.Combobox(modFrame, textvariable=self.comboboxStrVar['readme_cbobox'])
        cboboxDict['readme_cbobox'].grid(row=3, column=3, sticky=EW, pady=5, padx=5)
        it.Hovertip(cboboxDict['readme_cbobox'], text="Read Me File(s)")

        refreshButton = tk.Button(modFrame, text="R", image=self.refresh_img, command=lambda: self.processUI('refresh'))
        refreshButton.grid(row=1, column=4, sticky=EW, rowspan=2, padx=5)
        it.Hovertip(refreshButton, text="Refresh Dropdown Lists")

        #refreshButton.update_idletasks()
        readButton = tk.Button(modFrame, text="Help", image=self.help_img, command=self.readerDialog)
        readButton.grid(row=3, column=4, sticky=EW, pady=5, padx=5)

        return cboboxDict

    def commandWidgets(self, root):
        """
        Widgets for entry of the command (command-line) to launch Quake.

        :param root: Root frame of the window.
        :return: None
        """

        frame = tk.LabelFrame(root, text=" Command ")
        frame.pack(fill=X)
        frame.columnconfigure(index=0, weight=1)

        scbx = ttk.Scrollbar(frame, orient=HORIZONTAL)
        scbx.grid(row=1, column=0, sticky=EW, padx=5)

        r = 0  # Row.
        commandEntry = tk.Entry(frame, textvariable=self.entryStrVar['command'], xscrollcommand=scbx.set)
        commandEntry.grid(row=r, column=0, sticky=EW, padx=5)
        it.Hovertip(commandEntry, text="Commands & Arguments to Run Quake")

        scbx['command'] = commandEntry.xview

    def buttonWidgets(self, root):
        """
        Widgets for the launching QUake or quitting the app.

        :param root: Root frame of the window.
        :return: None
        """

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
        """
        Main processing for the UI.

        :param event: Unique processing of the event.
        :return:
        """
        match event:
            case 'ask_dfltdir':
                dir = tfd.askdirectory(title="Set Quake Runner Default Directory", initialdir=self.init_dir)
                if dir:
                    self.publish(f"Selected default directory: {dir}")
                    self.init_dir = dir
            case 'ask_file':
                file = tfd.askopenfilename(title="Selet Quake Engine", initialdir=self.init_dir)  # Get user selected Quake executable.
                if file and qf.engine_check(file):
                    self.processQuakeEngine(file)
                else:
                    self.entryStrVar['engine'].set('')
                    self.publish("No file selected or is not an executable file.")
            case 'ask_folder':
                folder = tfd.askdirectory(title="Selet Quake Base Directory", initialdir=self.init_dir)  # Get user selected Base Directory
                if folder:
                    self.processGameFolders(folder)
            case 'refresh':
                folder = self.entryStrVar['basedir'].get()
                if folder:
                    for ky in COMBOBOXES:
                        # self.cboboxDict[ky].delete(0, END)
                        self.cboboxDict[ky]['values'] = ''
                        self.cboboxDict[ky].set("SELECT")
                    self.processGameFolders(folder)
                    self.publish("Mod drop-down lists refreshed.")
            case 'run':
                command = self.entryStrVar['command'].get()
                self.run_command(command)
            case 'quit':
                self.checkSettings()
                self.destroy()

    def processQuakeEngine(self, file):
        self.publish(f"Executable or App file detected in {file}.", cls=True)
        self.entryStrVar['engine'].set(file)  # Display selected path & file.
        self.buildCommand()  # Build Quake launch command.
        folder = os.path.split(file)[0]  # Strip folder.
        self.processGameFolders(folder)  # Process folder for Quake game data.

    def processGameFolders(self, folder):
        self.clearComboBoxes()
        resources = qf.id1_check(folder)  # Check folder for id1 game data.
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
                id1_fldr = os.path.join(folder, 'id1')
                id1_maps = qf.get_maps(id1_fldr)  # Get bsp files from id1 map folder
                if id1_maps:
                    self.cboboxDict['id1mps_cbobox']['values'] = id1_maps

            games = qf.get_game_folders(folder)
            if games:
                self.publish("Game folders detected.")
                self.cboboxDict['games_cbobox']['values'] = games  # Load game combobox
        else:
            self.publish(f"id1 Folder not detected in {folder}.")

    def processModChkBtn(self, event=None):
        widgets = 'id1mps_rdobtn', 'id1mps_cbobox', 'games_rdobtn', 'games_cbobox', 'maps_chkbtn', 'maps_cbobox'
        if self.modChkBtnBoolVar.get():
            for widget in widgets:
                self.cboboxDict[widget]['state'] = NORMAL
        else:
            for widget in widgets:
                self.cboboxDict[widget]['state'] = DISABLED
                self.comboboxStrVar['maps_cbobox'].set("SELECT")
                # self.cboboxDict['maps_cbobox'].delete(0, END)
        self.buildCommand()

    def processRadioBtns(self, event=None):
        """
        Update combobox state based on Radiobutton state.

        :return: None
        """
        match self.radiobtnStrVar.get():
            case 'id1_maps':
                self.cboboxDict['id1mps_cbobox']['state'] = NORMAL
                self.cboboxDict['games_cbobox']['state'] = DISABLED
                self.cboboxDict['maps_cbobox']['state'] = DISABLED
                self.cboboxDict['maps_chkbtn']['state'] = DISABLED
                self.comboboxStrVar['games_cbobox'].set("SELECT")
                self.comboboxStrVar['maps_cbobox'].set("SELECT")
                # self.cboboxDict['maps_cbobox'].delete(0, END)
                self.cboboxDict['maps_cbobox']['values'] = ''
            case 'games':
                self.cboboxDict['id1mps_cbobox']['state'] = DISABLED
                self.cboboxDict['games_cbobox']['state'] = NORMAL
                self.cboboxDict['maps_chkbtn']['state'] = NORMAL
                if self.mapChkBtnBoolVar.get():
                    self.cboboxDict['maps_cbobox']['state'] = NORMAL
                self.comboboxStrVar['id1mps_cbobox'].set("SELECT")
        self.buildCommand()

    def processSkillChkBtn(self, event=None):
        if self.skillChkBtnBoolVar.get():
            self.cboboxDict['skill_cbobox']['state'] = NORMAL
        elif not self.skillChkBtnBoolVar.get():
            self.cboboxDict['skill_cbobox']['state'] = DISABLED
        self.buildCommand()

    def processMapChkBtn(self, event=None):
        if self.mapChkBtnBoolVar.get():
            self.cboboxDict['maps_cbobox']['state'] = NORMAL
        else:
            self.cboboxDict['maps_cbobox']['state'] = DISABLED
            self.comboboxStrVar['maps_cbobox'].set('SELECT')
        self.buildCommand()

    def processGameMapCboBox(self, event=None):
        basedir = self.entryStrVar['basedir'].get()
        game = self.comboboxStrVar['games_cbobox'].get()
        if basedir and game and game != 'SELECT':
            path = os.path.join(basedir, game)

            # Fill Readme ComboBox with text files from mod folder. #
            readme = qf.get_readme(path)
            if readme:
                self.cboboxDict['readme_cbobox']['values'] = readme
            else:
                # self.cboboxDict['readme_cbobox'].delete(0, END)
                self.cboboxDict['readme_cbobox']['values'] = ''
            self.comboboxStrVar['readme_cbobox'].set('SELECT')

            # Fill Maps Combobox with the bsp maps form the mod folder. #
            maps = qf.get_maps(path)
            if maps:
                self.cboboxDict['maps_cbobox']['values'] = maps
            else:
                # self.cboboxDict['maps_cbobox'].delete(0, END)
                self.cboboxDict['maps_cbobox']['values'] = ''
            self.comboboxStrVar['maps_cbobox'].set('SELECT')
            self.buildCommand()

    def readerDialog(self):
        """
        Method to display the readme text file contained in the mod folder.

        :return: None
        """

        path = self.entryStrVar['basedir'].get()
        mod_fldr = self.comboboxStrVar['games_cbobox'].get()
        readme = self.comboboxStrVar['readme_cbobox'].get()
        if path and mod_fldr and readme:
            file_path = os.path.join(path, mod_fldr, readme)
            if os.path.isfile(file_path):
                with open(file_path, errors='ignore') as in_file:
                    file_text = in_file.read()

                reader = tk.Toplevel(self)
                reader.title("Mod Help")
                reader.resizable(width=True, height=True)

                readerText = tf.ScrollBarText()
                readerText.scbText(parent=reader, title=" "+readme+" ")

                closeButton = tk.Button(reader, text="Close", command=reader.destroy)
                closeButton.pack(pady=5)

                reader.update_idletasks()
                w = reader.winfo_width()
                h = reader.winfo_height()
                reader.minsize(width=w, height=h)

                readerText.publish(file_text, end=False)

    def set_dfltdir(self):
        """
        Method to set the default directory of the app for the file and folder dialogs.

        :return: None
        """
        tmb.showinfo(title="Default Directory", message="Select the Directory with your Quake Folders & Files")
        dir = tfd.askdirectory(title="Set the Quake Runner Default Directory")
        if dir:
            self.init_dir = dir
            msg = f"Default Directory set to: {dir}. This can be changed in the Settings menu."
            self.publish(msg)
        else:
            self.publish("Use the Settings menu to select a Default Directory.")
            tmb.showwarning(title="WARNING!", message="Default Directory not Set.")

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
            if self.opsys == 'Darwin' and engine.endswith('.app'):  # Mac command prefix. Prefix not required for Windows.
                command = "open -a "

            if engine and os.path.exists(engine):
                command += engine  # Add engine path and executable.
            else:
                self.publish("Issue with executable or app. Please re-enter.")

            if self.opsys == 'Darwin' and engine.endswith('.app'):
                command += " --args"  # Mac executable suffix.

            folder = self.entryStrVar['basedir'].get()
            if folder and os.path.exists(folder):
                command += " -basedir "  # Add base directory (-basedir) command-line argument.
                command += folder  # Add base directory folder path.

            # add skill level
            skill = {ky:val for val, ky in enumerate(("Easy", "Normal", "Hard", "Nightmare"))}
            if self.skillChkBtnBoolVar.get() and engine and basedir:
                skl = self.cboboxDict['skill_cbobox'].get()
                command += f" +skill {skill[skl]}"

            mod_switch = self.modChkBtnBoolVar.get()
            radiobtn_sel = self.radiobtnStrVar.get()
            id1_map = self.cboboxDict['id1mps_cbobox'].get()  # Add user map selection.
            mod_map = self.cboboxDict['maps_cbobox'].get()  # Add user map selection.
            game = self.cboboxDict['games_cbobox'].get()  # Add game selection.
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

    def clearComboBoxes(self):
        for ky in COMBOBOXES:
            # self.cboboxDict[ky].delete(0, END)
            self.cboboxDict[ky]['values'] = ''
            self.comboboxStrVar[ky].set("SELECT")

    def checkSettings(self):
        """
        Check if settings have changed since the start of the app session. If true, notify user and ask to save.
        :return:
        """

        state=0
        if self.qr_cfg['dflt_dir'] == self.init_dir: state=1
        if self.qr_cfg['engine'] == self.entryStrVar['engine'].get(): state+=1   # Quake Engine.
        if self.qr_cfg['basedir'] == self.entryStrVar['basedir'].get(): state+=1  # Base Directory.
        if self.qr_cfg['mods_chkbtn'] == self.modChkBtnBoolVar.get(): state+=1
        if self.qr_cfg['mods_rdobtn'] == self.radiobtnStrVar.get(): state+=1  # Mod radio button -> id_maps or games.
        if self.qr_cfg['skill_chkbtn'] == self.skillChkBtnBoolVar.get(): state+=1  # Skill check button state.
        if self.qr_cfg['skill_cbobox'] == self.skillCbBoxStrVar.get(): state+=1
        if self.qr_cfg['maps_chkbtn'] == self.mapChkBtnBoolVar.get(): state+=1  # Map Check button state.

        if state != 8:
            if tmb.askyesno(title="Save", message="Selection Changes Detected.\nSave Settings?"):
                self.saveSettings()

    def saveSettings(self):
        self.qr_cfg['dflt_dir'] = self.init_dir
        self.qr_cfg['engine'] = self.entryStrVar['engine'].get()  # Quake Engine.
        self.qr_cfg['basedir'] = self.entryStrVar['basedir'].get()  # Base Directory.
        self.qr_cfg['mods_chkbtn'] = self.modChkBtnBoolVar.get()
        self.qr_cfg['mods_rdobtn'] = self.radiobtnStrVar.get()  # Mod radio button -> id_maps or games.
        self.qr_cfg['skill_chkbtn'] = self.skillChkBtnBoolVar.get()  # Skill check button state.
        self.qr_cfg['skill_cbobox'] = self.skillCbBoxStrVar.get()
        self.qr_cfg['maps_chkbtn'] = self.mapChkBtnBoolVar.get()  # Map Check button state.

        status = foo.writeConfig(file=CONFIGFILE, settings=self.qr_cfg)
        if status:
            self.publish("Settings saved.")
        else:
            self.publish(status)


if __name__ == '__main__':
    Main()