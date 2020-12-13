### troublshooting pygobject
https://stackoverflow.com/questions/1294272/how-do-i-install-pygtk-pygobject-on-windows-with-python-2-6

### if you got import glib.glib_ DLL error
[issue link]
https://stackoverflow.com/questions/3091281/import-gtk-glib-produces-importerror-dll-load-failed

[solution]
install pygtk all in one from 
https://www.gramps-project.org/wiki/index.php?title=Windows_installer#Installation

### pip install pyproj error
[issue]
Proj executable not found. Please set PROJ_DIR variable

[solution]
pip install pyproj==1.9.6

### Install
python2.7 32 bit windows
nsis
*	https://sourceforge.net/projects/nsis/
NSIS AccessControl plug-in
download the zip, and unzip it manually to "C:/progrfam files(86)/nsis/, unicode, and non unicode dlls to ints directories
*	http://nsis.sourceforge.net/AccessControl_plug-in
py2exe - note, before installing set the windows registry as shown below
*	http://www.py2exe.org/
pygtk-all-in-one
*   https://www.gramps-project.org/wiki/index.php?title=Windows_installer#Installation

### add python2 to windows registry 
*	https://stackoverflow.com/questions/27950855/add-python-2-7-6-to-the-windows-registry
reg add HKLM\SOFTWARE\Wow6432Node\Python\PythonCore\2.7\InstallPath /ve /t REG_SZ /d "C:\Python27" /f

## gdal solution
https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
