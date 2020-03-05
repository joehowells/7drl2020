import sys

from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files": ["data"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="7drl2020",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
