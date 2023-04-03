import sys
import os
import shutil
import distutils.dir_util, distutils.file_util
import errno
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('viewer.qml')

def move_folder(src, dst):
    try:
        if (os.path.normpath(src).lower() == os.path.normpath(dst).lower()): return
        if (os.path.exists(src)):
            distutils.dir_util.copy_tree(src, dst)
            shutil.rmtree(src)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            try:
                if (os.path.exists(dst)): os.remove(dst)
                shutil.copy(src, dst)
                shutil.rmtree(src)
            except:
                pass
    except:
        pass

def move_file(src, dst):
    try:
        if (os.path.normpath(src).lower() == os.path.normpath(dst).lower()): return
        if (os.path.isfile(src)):
            if (os.path.isfile(dst)): os.remove(dst)
            shutil.copy(src, dst)
            os.remove(src)
    except:
        pass
    
def remove_file(src):
    try:
        os.remove(src)
    except:
        pass
    
roots = engine.rootObjects()
roots[0].move_folder.connect(move_folder)
roots[0].move_file.connect(move_file)
roots[0].remove_file.connect(remove_file)

sys.exit(app.exec())