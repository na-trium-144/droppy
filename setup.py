#!/usr/bin/env python3
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
	# "packages": [],
	# "excludes": [],
	"include_files": ["music", "res"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(
	name="Droppy",
	version="1.0b",
	description="Music Game Droppy",
	options={"build_exe": build_exe_options},
	executables=[Executable("main.py", base=base)],
)
