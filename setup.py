"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['imodela.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True,
 'iconfile': 'icon.icns',
'plist': {'CFBundleShortVersionString':'1.0.0',}
}
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
