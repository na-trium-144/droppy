#!/usr/bin/env python3
import sys
from cx_Freeze import setup, Executable

title = "Droppy"
ver = "1.0"
title_ver = f"{title}_{ver}"

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
options = {
    "build_exe": {
	    # "packages": [],
	    # "excludes": [],
	    "include_files": ["music", "res"],
    },
    "bdist_mac": {
        "bundle_name": title,
    },
    "bdist_dmg": {
        "volume_label": title_ver,
        "applications_shortcut": True,
    },
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(
	name=title,
	version=ver,
	description="Music Game Droppy",
	options=options,
	executables=[Executable("main.py", base=base)],
)
