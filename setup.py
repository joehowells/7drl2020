import sys

from cx_Freeze import setup, Executable

build_exe_options = {
    "include_files": ["data"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Two Button Berserker",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, targetName="TwoButtonBerserker")]
)
