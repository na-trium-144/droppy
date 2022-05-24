#!/usr/bin/env python3
import sys
from cx_Freeze import setup, Executable

title = "Droppy"
ver = "1.1"
title_ver = f"{title}_{ver}"

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
options = {
	"build_exe": {
		# "collections","encodings","importlib","pygame"だけ残す
		"excludes": [
			"apport","apt","backports","certifi","cffi","chardet","cryptography","ctypes","curses",
			"distutils","email","html","http","httplib2","idna","json","jwt","keyring","launchpadlib","lazr","logging",
			"numpy","oauthlib","OpenGL","pkg_resources","pydoc_data","psutil","pytz","requests","setuptools","simplejson",
			"tkinter","unittest","urllib","urllib3","wadllib","xml","xmlrpc"
		],
		"include_files": ["music", "res"],
	},
	"bdist_mac": {
		"bundle_name": title,
		"iconfile": "AppIcon.icns",
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
	description=title,
	options=options,
	executables=[
		Executable(
			script="main.py",
			base=base,
			target_name=title,
			copyright="na-trium-144",
			icon="res/icon.ico"
		)
	],
)
