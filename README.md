#Quake Runner
Written with Python 3.12 & tkinter.
<pre>
Test Machines:
- MacBook Air with M2 chip & Sonoma 14.6.1
- HP Envy Laptop & Windows 11 Home 23H2
</pre>


##A Python GUI Tool to Execute Quake From Commandline Options

###Features & UI Description
- <b>User Data Field - Quake Engine:</b> Select the path to the Quake engine *.exe (Windows) or *.app (Mac). The button to the right of the text box with the 3 dots "..." will open the file dialog. The file path can also be manually entered.
- <b>User Data Field - Base Directory:</b> Select the path to the folder with id1 game data. The button to the right of the text box with the 3 dots "..." will open the folder dialog.

Note: An explanation is provided starting in "Basic Directory Structure (Mac or Windows)" to include running mod games and *.bsp maps.

- <b>User Selection - Game List:</b> A drop down list of game folders in the Base Directory. The script will test each mod folder and include only those folders with "pak" or "progs" files.
- <b>User Selection - Map List:</b> A drop down list of game maps found in the id1 maps folder. The script will test and load only the files with the "bsp" extension. 
- <b>Refresh Button:</b> An Ouroboros (snake eating its own tail) surrounding the Quake symbol. Refreshes the Game and Map list. 

Note: I'll often times download mods from Quaddicted then add them to my folder to try them out. The refresh button will add the new mod to the list.

- <b>Launch Command:</b> The text box just above the "Log" section that contains the assembled command to launch Quake with the selected game or map. The text is editable so additional command line options can be entered manually.
- <b>Log Window:</b> Provides the status of Quake Runner as options or selections change. It will also display the log output from Quake on Windows OS. A neat feature, to see what Quake was doing while the game was in session. The log contains system information as well captured by the Quake engine.
- <b>Save Settings:</b> In the main menu under "File" is "Save Settings". This saves the user selections then reloads them when Quake Runner is run.

The rest of this document explains two options for a directory structure to run Quake on Mac or Windows. As well as the commandline structure plus options. On Mac, the commandline is much trickier and was the inspiriation for this project.

Quake Runner has been tested with QuakeSpasm, QuakeSpasm-Spiked, vkQuake, vkQuake-RT & IronWail on Windows. For Mac, QuakeSpasm is the only modern port I've found with support for the MacOS.

###Basic Directory Structure (Mac or Windows)

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

To run Quake the user would simply double click the executable or *.app file from the quake engine port folder. Quake, on Windows, will detect the the id1 folder and start normally. Similarly, any mod folders added to the Quake engine port folder can also be launched either via commandline, Quake console or through menu options, if your port is so equipped. IronWail is a port that does a fantastic job of this through its Quake menu.

Note: On Mac, a dialog window will appear after launching the .app to enter in the location of the id1 data file. Its an annoying extra step. Below is the commandline option example for Quake to run on a Mac.

<b>Mac Dialog Window Command Line Option:</b> 

~~~
-basedir /Quake/quake_engine_port_folder
~~~

<b>Directory Structure Example with Mods</b>

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

As mentioned previously, mods and individual maps can be run using the Quake console or menu selections if the port has that option. As an alternative, a direct launch of the mod through the commandline would be structured as follows.

<b>Windows Shortcut or Batch File Example</b>

~~~
C:\Quake\quake_engine_port\quake_engine.exe -game quake_game

or

C:\Quake\quake_engine_port\quake_engine.exe +map quake_map.bsp
~~~

Map variation that includes setting the skill level.

~~~
C:\Quake\quake_engine_port\quake_engine.exe +skill # +map quake_map.bsp

# = 0-3 (Easy, Normal, Hard, Nightmare)

~~~

<b>Mac Dialog Window Command Line Options</b>

~~~
-basedir /Quake/quake_engine_port_folder -game quake_game

or

-basedir /Quake/quake_engine_port_folder +map quake_map.bsp
~~~

Map variation that includes setting the skill level.

~~~
-basedir /Quake/quake_engine_port_folder +skill # +map quake_map.bsp

# = 0-3 (Easy, Normal, Hard, Nightmare)

~~~

Another note for Mac users. Python (for Mac) comes with a python launcher that can be associated with python scripts. I have read claims of changing the file extension to "pyw" with the appropriate settings in the lancher will prevent a terminal window from opening alongside the script. I have never been able to get that to work. The terminal window hovering in my dock doing nothing, for me, is quite annoying. The solution is to create an Automator app. The Python script will run as if it were its own executable and without the terminal window. And like a Windows shortcut, the icon can be changed to match your app. I'll include some instructions at the end for Quake Runner.

###Two Folder Directory Structure

I found that as my appetite for mods grew, my folder started getting messy. Luckily, the current set of popular engine ports have command line options that facilitate organization of content into a different folder through the commandline option "-basedir". This allows you to have a folder for your engine(s) and a single folder for game data.

In the example below the game content folder is named "pakmod". That's the actual name I used on my machine but any name will do, just no spaces.

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

###Advanced Commandline Formats

The following command structure models use the directory example above. Of course there are user names and other folders that will need to be included depending on where the Quake folder is placed. Note: Quake is funny about names with spaces; use an underscore if you want to separate words.

<b>Command structure for launching the base Quake game.</b>

~~~
Windows: C:\Quake\quake_engine_port\quake_engine.exe -basedir C:\Quake\pakmod
Mac: open -a /Quake/quake_engine_port/quake_engine.app --args -basedir /Quake/pakmod
~~~

As previously mentioned, for Mac, a separate dialog window will appear for arguments. Through Quake Runner the arguments, specified by "--args" will be passed to the dialog window and you just have to hit the "start" button.

<b>Launching Quake with mods.</b>

~~~
Game Mods
Windows: C:\Quake\quake_engine_port\quake_engine.exe -basedir C:\Quake\pakmod -game quake_game
Mac: open -a /Quake/quake_engine_port/quake_engine.app --args -basedir /Quake/pakmod -game quake_game

Map Mods
Windows: C:\Quake\quake_engine_port\quake_engine.exe -basedir C:\Quake\pakmod +map quake_map.bsp
Mac: open -a /Quake/quake_engine_port/quake_engine.app --args -basedir /Quake/pakmod +map quake_map.bsp

Map Mods + Skill Variation
Windows: C:\Quake\quake_engine_port\quake_engine.exe -basedir C:\Quake\pakmod +skill # +map quake_map.bsp
Mac: open -a /Quake/quake_engine_port/quake_engine.app --args -basedir /Quake/pakmod +skill # +map quake_map.bsp

# =  0-3 (Easy, Normal, Hard, Nightmare)


Mod & Map Variation
Windows: C:\Quake\quake_engine_port\quake_engine.exe -basedir C:\Quake\pakmod -game copper +map quake_map.bsp
Mac: open -a /Quake/quake_engine_port/quake_engine.app --args -basedir /Quake/pakmod -game copper +map quake_map.bsp

~~~

The last example "Mod & Map" is of a map that uses the copper mod but does not supply copper as part of the zip file download. In this example there may be a "maps" folder in the mod or you may need to create one. Consult the installation instructions for the mod.

Quake Runner assembles the commandline structure based on the input then launches Quake. To reiterate, the Launch Command field in Quake Runner is editable so the user can enter any additional commands that are needed and Quake Runner will include them in the command structure it passes to the system.

<b>Mac Automator</b>

For those interested there is a funny little app in the Mac Applicatons folder called "Automator". To create an automator app for Quake Runner follow these instructions.

~~~
1. Click on Automator
2. Select "New Document"
3. Select "Application" & click "Choose" in the lower right.
4. Type "shell" in the search box at the top.
5. Double Click "Run Shell Script". At the top will be the default shell zsh.
6. Delete any commands in the box (my command box has the word "cat" in it).
7. Add the following command: cd /path_to_QuakeRunner 

cd = change directory. If there are spaces in any of the names in the path, quotes will be needed on each end. The quotes can be omitted if there is not.

8. Second line: /path_to_python_executable QuakeRunner.pyw

Example: /usr/local/bin/python3.12 QuakeRunner.pyw

9. Click the play button in the upper right and Quake Runner should appear on your screen.
10. Test out Quake Runner. If everything looks ok then save the Automator app.
~~~

The Automator app can now be used to launch Quake Runner. Have fun playing Quake!