import sys
from cx_Freeze import setup, Executable

import pygame
import os
from random import choice, randint


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
icon = "icon.ico"


if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "VirusAttack",
        version = "1.0",
        description = "Jogo Estilo Space Invaders!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("virusattack.py", base=base, icon=icon)])