#!/usr/bin/env python3

"""
110824
QuakeFoo.py

Functions for Quake Runner
"""

import os
import platform


def id_check(path):
    id1 = dict()
    is_engine = False
    is_basedir = False
    opsys = platform.system()

    if opsys == 'Darwin':
        is_engine = path.endswith("app") and os.path.isdir(path)  # check if selection is app and if selection is a directory
    elif opsys == 'Windows':
        is_engine = path.endswith("exe") and os.path.isfile(path)

    if is_engine:
        id_path = os.path.split(path)[0]
    else:
        is_basedir = os.path.isdir(path)
        if is_basedir:
            id_path = path

    if is_engine or is_basedir:
        id_fldr = os.path.join(id_path, "id1")
        maps_fldr = os.path.join(id_fldr, "maps")
        pak_file = os.path.join(id_fldr, "pak0.pak")
        id1['id_valid'] = os.path.isdir(id_fldr) and os.path.isfile(pak_file)
        id1['maps_fldr'] = os.path.isdir(maps_fldr)
    else:
        return False

    return id1

def isQuake_game(path):
        try:
            os.path.isdir(path)
        except OSError as err:
            return err
        else:
            if not path.endswith("app"):
                pak_file = os.path.join(path, "pak0.pak")
                dat_file = os.path.join(path, "progs.dat")
                maps_folder = os.path.join(path, "maps")
                if os.path.exists(maps_folder):
                    contents = os.listdir(maps_folder)
                    bsp_check = any([c for c in contents if ".bsp" in c])

                return os.path.isfile(pak_file) or os.path.isfile(dat_file) or os.path.isdir(maps_folder) and bsp_check
            else:
                return False

def get_games(path):
    try:
        contents = os.listdir(path)
    except OSError as err:
        return err
    else:
        if not path.endswith("app") and contents:
            folders = [c for c in contents if os.path.isdir(os.path.join(path, c)) and c != "id1"]
            if folders:
                return [f for f in folders if isQuake_game(os.path.join(path, f))]
        else:
            return False

def get_maps(path):
    maps_folder = os.path.join(path, "id1")
    maps_folder = os.path.join(maps_folder, "maps")
    if os.path.exists(maps_folder):
        contents = os.listdir(maps_folder)
        bsp_files = [c for c in contents if c.endswith(".bsp")]
        return bsp_files
    else:
        return False

# Test Code #
if __name__ == '__main__':
    engine = r'<path to quake engine>'
    basedir = r'<path to directory with id1 folder and mod games>'

    print("Valid id1 folder in Engine selection:", id_check(engine))
    print("Valid id1 folder in basedir selection:", id_check(basedir))
    print("Does folder contain valid Quake Files (Engine):", isQuake_game(engine))
    print("Does folder contain valid Quake Files (basedir):", isQuake_game(basedir))
    print("Does folder contain valid Quake Files (terra-2022):", isQuake_game(basedir+"//terra-2022"))
    print("List of valid game folders (id1 folder):", get_games(engine))
    print("List of valid game folders (basedir folder):", get_games(basedir))
    print("List of valid maps (basedir folder):", get_maps(basedir))
    print("List of valid maps (terra-2022):", get_maps(basedir+"//terra-2022"))
