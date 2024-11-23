#!/usr/bn/env python3
"""
111724
QuakeFoo.py

Support functions for Quake Runner
"""

import os
import platform

def engine_check(filepath):
    """
    Validate user selection is an executable file for WIndows or an app file for mac.

    :param file: Selected path and file name of the executable.
    :return: BOOL
    """
    path, file = os.path.split(filepath)
    file = file.lower()
    filepath = os.path.join(path, file)
    match platform.system():
        case 'Darwin':
            is_engine = filepath.endswith('.app') and os.path.isdir(filepath)  # check if selection is app and if selection is a directory
        case 'Windows':
            is_engine = filepath.endswith('.exe') and os.path.isfile(filepath)
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

# Test Code #
if __name__ == '__main__':
    engine_no_id1 = r'C:\Users\IT213\Documents\Quake\ironwail-0.8.0-win64'
    engine_id1 = r'C:\Users\IT213\Documents\Quake\quake-rt-1_0_1'
    basedir_no_id1 = r'C:\Users\IT213\Documents\Quake'
    basedir_id1 = r'C:\Users\IT213\Documents\Quake\PAKMOD'

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
