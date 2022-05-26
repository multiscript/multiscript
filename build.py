import platform
import subprocess

subprocess.run(["pyinstaller", "multiscript.spec", "--noconfirm"])

if platform.system() == "Darwin":
    subprocess.run(["dmgbuild", "-s", "multiscript.dmg.py", "Multiscript", "dist/Multiscript.dmg"])
elif platform.system() == "Windows":
    subprocess.run(["C:\Program Files (x86)\Inno Setup 6\iscc.exe", "multiscript.iss"])
