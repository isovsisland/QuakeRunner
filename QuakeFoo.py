#!/usr/local/bin/python3

"""
111724
Python 3.12.7

QuakeFoo.py - Support functions for Quake Runner.
Functions
    engine_check(filepath) - Check if provided engine is valid executable.
    id1_check(folder) - Check if provided folder has id1 folder and game data.
    game_check(path) - Check if provided folder (mod folder) has game data
    get_game_folders(path) - Uses game_check() to test folder for game data and return list of folders.
    get_maps(path) - Check if provided folder has a maps folder and return a list of bsp files.
    set_config_dflt() - Set Quake Runner defaults if no config file (typicaly new installation"
    get_readme(path) - Get list of text files in the mod folder. The mod folder usually has a file with insturtions.

"""

import os
import foo
import platform

def engine_check(filepath):
    """
    Validate user selection is an executable file for Windows or an app file for mac.
    112824 - Improved detection of Unix exectable files (is_unexe) with macholib, see foo.py.

    :param file: Selected path and file name of the executable.
    :return: BOOL
    """
    path, file = os.path.split(filepath)
    file = file.lower()
    filepath = os.path.join(path, file)
    match platform.system():
        case 'Darwin':
            is_engine = filepath.endswith('.app') and os.path.isdir(filepath) or os.access(filepath, os.X_OK)  # check if selection is app and if selection is a directory
        case 'Windows':
            is_engine = filepath.endswith('.exe') and os.path.isfile(filepath) and os.access(filepath, os.X_OK)
    return is_engine

def id1_check(folder):
    """
    Check if 'id1' folder exists as a subdirectory. Required to run Quake.
    Check for valid game file 'pak0.pak'. Required to run Quake. The remastered 'pak0.pak' does not have a 'pak1.pak' file.
    Check for valid game file 'pak1.pak'. Required to run Quake if 'pak0.pak' is an original release.
    Check for 'maps' folder. Not required to run Quake.
    Check for '*.bsp' files in the maps folder. Also not required. Information is used for id1_maps combobox.

    :param folder: Selected path & folder.
    :return: BOOL dictionary for each category.
    """
    kys = 'id1_folder', 'id1_pak0', 'id1_pak1', 'id1_maps', 'id1_bsp'
    id1 = {ky:False for ky in kys}

    id1_fldr = os.path.join(folder, 'id1')
    id1['id1_folder'] = os.path.isdir(id1_fldr)
    if id1['id1_folder']:
        contents = os.listdir(id1_fldr)
        id1['id1_pak0'] = any('pak0.pak' == c.lower() for c in contents)
        id1['id1_pak1'] = any('pak1.pak' == c.lower() for c in contents)

        id1_maps = os.path.join(id1_fldr, 'maps')
        id1['id1_maps'] = os.path.isdir(id1_maps)
        if id1['id1_maps']:
            contents = os.listdir(id1_maps)
            id1['id1_bsp'] = any('.bsp' in c.lower() for c in contents)
    return id1

def game_check(path):
    """
    Test a single folder for game data in the form of pak0.pak, progs.dat or .bsp files in the maps folder.
    Used primarily as an internal function for the get_game_folders() function.

    :param path: Folder path.
    :return: Results for a given folder.
    """
    game_pak0 = False
    game_progs = False
    game_maps = False
    game_bsp = False

    if os.path.isdir(path):
        contents = os.listdir(path)
        game_pak0 = any('pak0.pak' == c.lower() for c in contents)
        game_progs = any('progs.dat' == c.lower() for c in contents)

        game_maps = os.path.join(path, 'maps')
        if os.path.isdir(game_maps):
            contents = os.listdir(game_maps)
            game_bsp = any('.bsp' in c.lower() for c in contents)

    return game_pak0 or game_progs or game_bsp

def get_game_folders(path):
    """
    Used as the primary function to test a folder for game data in the form of file types, pak0.pak, progs.dat or bsp files in the maps folder.
    Uses the game_check() function

    :param path:
    :return:
    """
    contents = os.listdir(path)
    cwd = os.getcwd()
    os.chdir(path)
    folders = [c for c in contents if os.path.isdir(c) and c != 'id1']
    game_fldrs = [f for f in folders if game_check(f)]
    os.chdir(cwd)

    return game_fldrs

def get_maps(path):
    """
    Get list of bsp files in maps directory of source folder.

    :param path: Source folder ex. /Quake/Engine/id1
    :return: List of maps
    """
    if os.path.exists(path):
        cwd = os.getcwd()
        os.chdir(path)
        if os.path.exists('maps') and os.path.isdir('maps'):
            contents = os.listdir('maps')
            if contents:
                os.chdir('maps')
                maps = [c for c in contents if os.path.isfile(c) and c.endswith('.bsp')]
                os.chdir('..')
            else:
                maps = False
        else:
            maps = False
        os.chdir(cwd)
    else:
        maps = False

    return maps

def set_config_dflt():
    """
    Sets Quake Runner defaults if no config file.

    :return: None
    """
    return {
        "dflt_dir": "",
        "engine": "",
        "basedir": "",
        "mods_chkbtn": True,
        "mods_rdobtn": "games",
        "skill_chkbtn": False,
        "skill_cbobox": "Normal",
        "maps_chkbtn": False
    }

def get_readme(path):
    """
    Get readme text file list.

    :param path: Path to mod folder.
    :return: List of text files.
    """
    if os.path.exists(path):
        contents = os.listdir(path)
        readme = [c for c in contents if c.endswith('.txt')]
        if not readme:
            readme = False
    else:
        readme = False
    return readme


# Test Code #
if __name__ == '__main__':
    engine_no_id1 = r'MacOS or Windows/Test/Path/to_engine/without_id1_folder'
    engine_id1 = r'MacOS or Windows/Test/Path/to_engine/with_id1_folder'
    basedir_no_id1 = r'MacOS or Windows/Test/Path/to_basedir/without_id1_folder'
    basedir_id1 = r'MacOS or Windows/Test/Path/to_basedir/with_id1_folder'

    print("engine no id1:", id1_check(engine_no_id1))
    print("engine with id1:", id1_check(engine_id1))
    print("basedir no id1:", id1_check(basedir_no_id1))
    print("basedir with id1", id1_check(basedir_id1))

    print()
    game_folders = get_game_folders(engine_no_id1)
    print("Engine Game Folder Check no id1", game_folders)
    game_folders = get_game_folders(engine_id1)
    print("Engine Game Folder Check id1", game_folders)
    game_folders = get_game_folders(basedir_no_id1)
    print("Basedir Game Folder Check no id1", game_folders)
    game_folders = get_game_folders(basedir_id1)
    print("Basedir Game Folder Check id1", game_folders)

    print()
    map_folder = os.path.join(engine_no_id1, "id1")
    print("no id1 maps:", get_maps(map_folder))
    map_folder = os.path.join(engine_id1, "id1")
    print("id1 maps:", get_maps(map_folder))

    map_folder = os.path.join(basedir_no_id1, "id1")
    print("id1 maps:", get_maps(map_folder))
    map_folder = os.path.join(basedir_id1, "id1")
    print("id1 maps:", get_maps(map_folder))
