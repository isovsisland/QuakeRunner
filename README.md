# Quake Runner

**Purpose:** A python script for configuring the command-line options to
run Quake on Mac or Windows.

**Test Machines:**

-   MacBook Air with M2 chip & Sonoma 14.6.1
-   HP Envy Laptop & Windows 11 Home 23H2

**Supporting Software (MacOS)**

- IDE: PyCharm 2024.2.4 (Community Edition)
- MarkDown Editor: MacDown Version 0.7.3 (1008.4)
- Image Manipulation: GIMP 2.10.32 (revision 1)
- Image Format Conversion: Image2Icon Version 2.18 (944) Shiny Frog Limited

**Preface:** The inspiration for this script stemmed from the launch
commands needed in such applications as necros compiling GUI and
Trenchbroom. Both programs are used extensively in creating custom maps
and games for the original id Software Quake game, among others. To add
to the inspiration was the frequent sampling of hundreds of fan created mods. While it is a simple matter to create shortcuts on Windows with the commands to launch a mod directly, the MacOS is more difficult. And even then, on either OS, ending up with a ton of shortcuts wasn't practical. This script provides a GUI to select games, maps and add command-line options without much typing or a folder full of shortcuts. The Python script itself, if used directly adapts to the OS (Windows or Mac). Executables are planned for future releases and will be   specific to the OS.

*Mac Screenshot*

![](media/image1.png)

# Features & UI Description

-   **Quake Engine:** Select the path to the Quake engine \*.exe
    (Windows) or \*.app (Mac). The button to the right of the text box
    with the three dots \"\...\" will open the file dialog. 

-   **Base Directory:** Select the path to the folder with id1 game
    data. The button to the right of the text box with the three dots
    \"\...\" will open the folder dialog. For MacOS it is recommended
    that the Quake Engine folder not be used as the Base Directory due
    to issues with QuakeSpasm and how MacOS operates.

*Note <sup>1</sup>: The text boxes are editable, but they are not bound yet to update the command-line. Selection of the directory through the dialog will, however, update the command-line.* 

*Note <sup>2</sup>: An explanation is provided starting in \"Basic
Directory Structure (Mac or Windows)\" to include running mod games and
\*.bsp maps.*

## Mods Section

-   **Use Mods:** Thic checkbox will turn off the mods section and exclude the commands from the command-line. 

-   **id1 Maps:** A dropdown list that can contains user created maps from
    the "maps" folder of the id1 directory.

*Note: For Mac users, as mentioned above, I have found an
issue with using the Quake Engine folder as the Base Directory for the
id1 folder. This is normally the default configuration for Quake, but
Quake was not originally written for the Mac. QuakeSpasm will launch
correctly with the base game but an error occurs when attempting to
locate custom maps in the "maps" folder of the id1 directory. This
feature runs fine if another folder is used independent of the Quake
Engine folder as will be explained later in this documentation.*

-   **Game Mods:** A drop-down list that contains the game folders in the
    Base Directory. The script will test each mod folder and include
    only those folders with "pak" or "progs" files.

-   **Game Maps:** A drop-down list that contains the maps found in the
    selected game folder. The script will test and load only the files
    with the "bsp" extension.

-   **Skill:** A drop-down list of skill levels that can be set prior to
    entering a map or game mod. The user should note that not all maps or
    games allow for a skill level to be set. Consult the map or game
    text file for clarification or set the skill then check via the
    Quake console by pressing "~" and typing "skill". Quake should
    respond with the current setting.

-   **Refresh Button:** The image on the button is of an Ouroboros (snake
    eating its own tail) surrounding the Quake symbol. Clicking the
    button will refresh the id1 Maps; Game Mods; & Game Maps drop-downs.

*Note: I'll often times download mods from Quaddicted
then add them to my folder to try them out. The refresh button will add
the new maps and mods to the list without having to restart Quake
Runner.*

-   **Command:** The text box just above the "Log" section. This is
    the assembled command based on the options selected. The text is
    editable so additional command line options can be entered manually
    such as adding mods like -quoth or -copper or combinations like
    -hypnotic -quoth. The user should consult the text instructions
    provided with the map or mod. This is a nice feature because Quake
    Runner will execute the command independently of the selected
    options. This can also be a problem with any errors that may be
    introduced from manually typing in the command.

-   **Log (window)**: Provides the status of Quake Runner as options
    or selections change. It will also display the log output from Quake
    on Windows OS. A neat feature, to see what Quake was doing while the
    game was in session. The log contains system information as well,
    captured by the Quake engine like graphics and memory usage.

-   **Settings (menu option):** In the main menu under "Settings" is
    "Save". This saves the user selections then reloads them when
    Quake Runner is launched.

-   **Quake & Quit (buttons):** Quake runs the command. The user
    should see the familiar Quake demo on Windows while Mac users will
    get the system generated start dialog.

The rest of this document explains two options for a directory structure
to run Quake on Mac or Windows. As well as the command-line structure
plus options.

Quake Runner has been tested with QuakeSpasm, QuakeSpasm-Spiked,
vkQuake, vkQuake-RT & IronWail on Windows. For Mac, QuakeSpasm is the
only modern port I\'ve found with support for the MacOS.

## Basic Directory Structure (Mac or Windows)

~~~
Quake
|_quake_engine_port
  |_quake_engine.exe or quake_engine.app
  |_<other files>
  |_<...>
  |_<...>
  |_<etc.>
  |
  |_id1
    |_maps
    |
    |_pak0.pak
    |_pak1.pak (Note: the Quake remastered pak0 file does not have a pak1.pak)
~~~

To run Quake the user would double click the *.exe or *.app file from
the Quake engine port folder. Quake, on Windows, will detect the id1
folder and start normally. Similarly, any mod folders added to the Quake
engine folder can also be launched either via command-line, Quake
console or through menu options, if your port is so equipped. IronWail
is a port that does a fantastic job of this through its Quake UI.

*Note: On Mac, a dialog window will appear after launching Quake to enter in the location of the id1 data file. Below is screenshot of the window and the command-line option example.*

![](media/image3.png)

## Mac Dialog Window Command Line Option:

*-basedir /Quake/quake_engine_port_folder*

## Directory Structure Example with Mods

~~~
Quake
|_quake_engine_port
  |_quake_engine.exe or quake_engine.app
  |_<other files>
  |_<...>
  |_<...>
  |_<etc.>
  |
  |_id1
  | |_maps
  | | |_quake_map(s).bsp
  | |
  | |_pak0.pak
  | |_pak1.pak (Note: the remastered pak0 file does not have a pak1.pak)
  |
  |_quake_game
    |_maps
    | |_quake_map(s).bsp
    |
    |_pak0.pak or progs.dat
~~~

As mentioned previously, mods and individual maps can be run using the
Quake console or menu selections if the port has that option. As an
alternative, a direct launch of the mod through the command-line would
be structured as follows and is what Quake Runner does through the
selected options.

## Windows Shortcut or Batch File Example

*C:\Quake\quake_engine_port\quake_engine.exe -game quake_game*

or

*C:\Quake\quake_engine_port\quake_engine.exe +map quake_map.bsp*

## Command variation that includes setting the skill level.

*C:\Quake\quake_engine_port\quake_engine.exe +skill # +map
quake_map.bsp*

*# = 0-3 (Easy, Normal, Hard, Nightmare)*

Mac Dialog Window Command Line Options

*-basedir /Quake/base_birectory -game quake_game*

or

*-basedir /Quake/base_diretory +map quake_map.bsp*

## Map variation that includes setting the skill level.

*-basedir /Quake/base_directory +skill # +map quake_map.bsp*

*# = 0-3 (Easy, Normal, Hard, Nightmare)*

*Note: Python for Mac comes with a launcher that
can be associated with python scripts. I have read claims of changing
the file extension to "pyw" with the appropriate settings in the
launcher will prevent a terminal window from opening alongside the
script. I have never been able to get that to work. The solution I found that works is to create an Automator app. The Python script will run as if it were its own executable and without the terminal window. And like a Windows
shortcut, the icon can be changed to match your app. I'll include some
instructions at the end for Quake Runner.*

# Two Folder Directory Structure

I found that as my appetite for mods grew, my folder started getting
messy. Luckily, the current set of popular engine ports have command
line options that facilitate organization of content into a different
folder through the command-line option "-basedir". This allows you to
have a folder for your engine and a separate folder for game data. In
the example below the game content folder is named "pakmod". That's
the actual name I use on my machine but any name will do, just no
spaces.

~~~
Quake
|_quake_engine_port
| |_quake_engine.exe or quake_engine.app
| |_<other files>
| |_<...>
| |_<...>
| |_<etc.>
|
|_pakmod
  |_id1
  | |_maps
  | | |_quake_map(s).bsp
  | |
  | |_pak0.pak
  | |_pak1.pak (Note: the remastered pak0 file does not have a pak1.pak)
  |
  |_quake_game
    |_maps
    | |_quake_map(s).bsp
    |
    |_pak0.pak or progs.dat
~~~

## Advanced Command-line Formats

The following command-line models use the directory example above.
Of course, there are user names and other folders that will need to be
included depending on where the Quake folder is placed.

*Note: Quake is funny about names with spaces; use an underscore if you want to separate words.*

## Command structure for launching the base Quake game.

-   **Windows:** *C:\Quake\quake_engine_port\quake_engine.exe
    -basedir C:\Quake\pakmod*

-   **Mac:** *open -a /Quake/quake_engine_port/quake_engine.app --args
    -basedir /Quake/pakmod*

As previously mentioned, for Mac, a separate dialog window will appear
for arguments. Through Quake Runner the arguments, specified by
"--args" will be passed to the dialog window and you just have to hit
the "start" button.

## Running Quake with mods.

**Game Mods**

-   **Windows:** *C:\Quake\quake_engine_port\quake_engine.exe
    -basedir C:\Quake\pakmod -game quake_game*

-   **Mac:** *open -a /Quake/quake_engine_port/quake_engine.app --args
    -basedir /Quake/pakmod -game quake_game*

**Map Mods**

-   **Windows:** *C:\Quake\quake_engine_port\quake_engine.exe
    -basedir C:\Quake\pakmod +map quake_map.bsp*

-   **Mac:** *open -a /Quake/quake_engine_port/quake_engine.app --args
    -basedir /Quake/pakmod +map quake_map.bsp*

**Map Mods + Skill Variation**

-   **Windows:** *C:\Quake\quake_engine_port\quake_engine.exe
    -basedir C:\Quake\\pakmod +skill # +map quake_map.bsp*

-   **Mac:** *open -a /Quake/quake_engine_port/quake_engine.app --args
    -basedir /Quake/pakmod +skill # +map quake_map.bsp*

*# = 0-3 (Easy, Normal, Hard, Nightmare)*

**Mod & Game Variation**

-   **Windows:** *C:\\Quake\\quake_engine_port\\quake_engine.exe
    -basedir C:\\Quake\\pakmod -hypnotic -quoth -game quake_game_folder*

-   **Mac:** *open -a /Quake/quake_engine_port/quake_engine.app \--args
    -basedir /Quake/pakmod -hypnotic -quoth -game quake_game_folder*

**Mod & Map Variation**

-   **Windows:** *C:\Quake\quake_engine_port\quake_engine.exe
    -basedir C:\Quake\pakmod -game copper +map quake_map.bsp*

-   **Mac:** *open -a /Quake/quake_engine_port/quake_engine.app --args
    -basedir /Quake/pakmod -game copper +map quake_map.bsp*

In the last example "Mod & Map Variation", is of a map that uses the copper mod but does not supply copper as part of the zip file download. The "maps" folder is in the folder of the mod game, similar to how there is a "maps" folder inside the id1 folder.

Quake Runner assembles the command-line structure based on the input
then launches Quake. To reiterate, the Command field in Quake
Runner is editable so the user can enter any additional commands that
are needed and Quake Runner will include them in the command structure
it passes to the system.

## Mac Automator

There is a funny little app in the Mac Applications folder called
"Automator". To create an automator app for Quake Runner follow these
instructions.

~~~
1. Click on Automator
2. Select "New Document"
3. Select "Application" & click "Choose" in the lower right.
4. Type "shell" in the search box at the top.
5. Double Click "Run Shell Script". At the top will be the default shell zsh.
6. Delete any commands in the box (my command box has the word "cat" in it).
7. Add the following command: cd path_to_QuakeRunner

cd = change directory. If there are spaces in any of the names in the path, quotes will be needed on each end. The quotes can be omitted if there is not.

8. Second line: /path_to_python_executable Main.pyw

Example: /usr/local/bin/python3.12 Main.pyw

9. Click the play button in the upper right and Quake Runner should appear on your screen.
10. The next time you want to run Quake Runner just double click the app.
~~~

![](media/image2.png)

This document attempts to provide credit to the individuals and organizations, open source or proprietary, in which software and information was directly used in creating the content for this project. In addition, the goal is to make this information as accurate as possible, either through my own research or experience. Please contact me if you have any concerns. Have fun playing Quake!
