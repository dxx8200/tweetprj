import sys
import os
import shutil
import time
import traceback
import distutils.dir_util, distutils.file_util
import errno
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load(os.path.join(os.path.realpath(os.path.dirname(__file__)),'viewer.qml'))

def move_folder(src, dst):
    try:
        if (os.path.normpath(src).lower() == os.path.normpath(dst).lower()): return
        if (os.path.exists(src)):
            shutil.move(src, dst)
    except:
        traceback.print_exc()

def move_file(src, dst):
    try:
        if (os.path.normpath(src).lower() == os.path.normpath(dst).lower()): return
        if (os.path.isfile(src)):
            if (os.path.isfile(dst)): os.remove(dst)
            shutil.copy(src, dst)
            os.remove(src)
    except:
        traceback.print_exc()
    
def remove_file(src):
    try:
        os.remove(src)
    except:
        traceback.print_exc()
    
roots = engine.rootObjects()
roots[0].move_folder.connect(move_folder)
roots[0].move_file.connect(move_file)
roots[0].remove_file.connect(remove_file)

sys.exit(app.exec())